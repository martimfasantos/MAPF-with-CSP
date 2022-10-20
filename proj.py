import sys
from tracemalloc import start
import pymzn
import subprocess


UNSAT = b"UNSATISFIABLE"
SOLVER = 'Chuffed'  # Chuffed / Gecode

def main(graph, scen):

    # read given files and assert variables
    n_vertices, n_edges, adjs = read_graph(graph)
    n_agents, start_pos, goal_pos = read_scen(scen)

    global INF
    INF = n_edges+1

    # calculate every min distance using BFS
    min_d = calc_min_vertex_dist(n_vertices, adjs, goal_pos)

    print(min_d)

    # calculate min makespan using BFS
    makespan = calc_min_makespan(start_pos, goal_pos, min_d)

    # make the timetable matrix
    # timetable = make_timetable(n_vertices, adjs)

    data = {'n_vertices': n_vertices,
            'n_edges': n_edges,
            'adj': adjs,
            'n_agents': n_agents,
            'start': start_pos,
            'goal': goal_pos,
            'min_d': min_d
            }

    # probably JUMP will be 1 after optimized (USAT is detected faster)
    global JUMP
    JUMP = min(round(max((n_agents / n_vertices)**2 * 5, 1) + n_agents/20), 3)
    print("JUMP:")
    print(JUMP)

    output = UNSAT
    if n_vertices > 200:
        global SOLVER
        SOLVER = 'Gecode'

    # print(SOLVER)
    while UNSAT in output and makespan < 1000:

        output = check_solution(SOLVER, data, makespan)
        print("------")
        print(makespan)
        print("------")

        makespan += JUMP

    output = check_lower_makespan(output, SOLVER, data, makespan - JUMP)
    print_output(output)


def print_output(output):
    output = "".join(chr(x) for x in output)
    output = output.split("\n")[1:-3]
    for i, o in enumerate(output):
        o = o[3:].split(", ")

        print(f"i={i} ", end="")
        for j, a in enumerate(o):
            print(f"{j+1}:{a.strip()} ", end="")
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
        _ = skip_comments(input_scen)
        line = skip_comments(input_scen)

        start_pos = [None] * n_agents
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
        return []

    while queue:
        node = queue.pop(0)
        if node not in visited:
            if node != start:
                visited.append(node)
            for adj in adjs[node-1]:
                if adj == goal:
                    visited.append(adj)
                    return visited
                if adj not in visited:
                    queue.append(adj)


def calc_min_vertex_dist(n_vertices, adjs, goal_pos):
    d = [[-1] * n_vertices for _ in range(1, n_vertices+1)]

    for goal in goal_pos:
        for vertex in range(1, n_vertices+1):
            path = bfs(adjs, goal, vertex)
            # path = nx.shortest_path()
            if path != None:
                path_length = len(path)
            else:
                path_length = INF
            d[goal-1][vertex-1] = path_length

    return d


def calc_min_makespan(start_pos, goal_pos, min_d):
    min_makespan = 2
    for s, g in zip(start_pos, goal_pos):
        if min_d[g-1][s-1] > min_makespan:
            min_makespan = min_d[g-1][s-1]
    return min_makespan


def check_solution(solver, data, makespan):
    data['makespan'] = makespan

    with open("data.dzn", "w") as _:
        pymzn.dict2dzn(data, fout='./data.dzn')

    # change solver?
    sp = subprocess.Popen(['minizinc', '--solver', solver, 'mapf.mzn', 'data.dzn'],
                          stdout=subprocess.PIPE,  stderr=subprocess.PIPE)

    return sp.stdout.read()


def check_lower_makespan(output, SOLVER, data, makespan):

    lower_makespan = makespan
    while UNSAT not in output and lower_makespan > makespan - JUMP:
        new_output = output
        lower_makespan -= 1
        output = check_solution(SOLVER, data, lower_makespan)

    return new_output


if __name__ == '__main__':
    graph = sys.argv[1]
    scen = sys.argv[2]

    main(graph, scen)
