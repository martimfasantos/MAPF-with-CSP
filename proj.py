import sys
import pymzn
import subprocess
from subprocess import check_output


def print_output(output):
    output = "".join(chr(x) for x in output)
    output = output.split("\n")[3:-3]
    for i, o in enumerate(output):
        o = o[3:].split(", ")

        print(f"i={i} ", end="")
        for j, a in enumerate(o):
            print(f"{j+1}:{a} ", end="")

        print()


def skip_comments(file):
    line = file.readline()
    while line and line[0] == "#":
        line = file.readline()

    return line


def read_graph(graph):
    with open(graph) as input_graph:
        n_vertices = int(skip_comments(input_graph))
        n_edges = int(skip_comments(input_graph))

        # define adjs where free_adjs[i] is a set of the free adjacencies for the vertex i+1
        adjs = [set() for _ in range(n_vertices)]

        line = skip_comments(input_graph)
        while line:
            edge = [int(x) for x in line.strip().split()]

            adjs[edge[0]-1].add(edge[1])
            adjs[edge[1]-1].add(edge[0])

            line = skip_comments(input_graph)

    return n_vertices, n_edges, adjs


def read_scen(scen):
    with open(scen) as input_scen:
        n_agents = int(skip_comments(input_scen))

        # handle START
        line = skip_comments(input_scen)

        start_pos = [None] * n_agents
        line = skip_comments(input_scen)
        while line and "GOAL" not in line:
            i, a = line.strip().split()
            start_pos[int(i) - 1] = int(a)

            line = skip_comments(input_scen)

        # handle STOP
        line = skip_comments(input_scen)
        goal_pos = [None] * n_agents
        while line:
            i, a = line.strip().split()
            goal_pos[int(i) - 1] = int(a)

            line = skip_comments(input_scen)

        return n_agents, start_pos, goal_pos


def bfs(adjs, start, goal):
    visited = []
    queue = [start]

    if start == goal:
        return visited

    while queue:
        node = queue.pop(0)
        if node not in visited:
            visited.append(node)
            for adj in adjs[node-1]:
                if adj == goal:
                    visited.append(adj)
                    return visited
                if adj not in visited:
                    queue.append(adj)


def calc_minspan(start_pos, goal_pos, adjs):
    min_makespan = 2
    for start, goal in zip(start_pos, goal_pos):
        path_size = len(bfs(adjs, start, goal))
        if path_size > min_makespan:
            min_makespan = path_size

    return min_makespan


def main(graph, scen):

    n_vertices, n_edges, adjs = read_graph(graph)
    # print(n_vertices)
    # print(n_edges)
    # print(edges)
    # print(adjs)

    n_agents, start_pos, goal_pos = read_scen(scen)
    # print("$$$$$$")
    # print(start_pos)
    # print(goal_pos)
    # print("$$$$$$")
    # print(n_agents)
    # print(agents)

    # calculate min makespan using BFS
    makespan = calc_minspan(start_pos, goal_pos, adjs)

    data = {'n_vertices': n_vertices,
            'n_edges': n_edges,
            'adj': adjs,
            'n_agents': n_agents,
            'start': start_pos,
            'goal': goal_pos
            }

    output = b"UNSATISFIABLE"
    while b"UNSATISFIABLE" in output and makespan < 100:

        data['makespan'] = makespan

        with open("data.dzn", "w") as _:
            pymzn.dict2dzn(data, fout='./data.dzn')

        # ver aqui se devemos mudar o solver / o gui fez e ajudou
        sp = subprocess.Popen(['minizinc', '--solver', 'Gecode', 'mapf.mzn', 'data.dzn'],
                              stdout=subprocess.PIPE,  stderr=subprocess.PIPE)

        output = sp.stdout.read()

        makespan += 1

    print_output(output)


if __name__ == '__main__':
    graph = sys.argv[1]
    scen = sys.argv[2]

    main(graph, scen)
