from minizinc import Instance, Model, Solver
import pymzn
import subprocess
from subprocess import check_output

START = 0
GOAL = 1


def print_output(output):
    output = "".join(chr(x) for x in output)
    output = output.split("\n")[3:-3]
    for i, o in enumerate(output):
        o = o[3:].split(", ")

        print(f"i={i} ", end="")
        for j, a in enumerate(o):
            print(f"{j+1}:{a} ", end="")

        print()


def main(graph, scen):
    with open(graph, "r") as input_graph:

        n_vertices = int(input_graph.readline())
        n_edges = int(input_graph.readline())

        edges = input_graph.read()
        edges = edges.split("\n")[:-1]
        # parse edges to lists of two integers
        edges = [edge.split() for edge in edges]
        edges = [[int(edge[j]) for j in range(2)] for edge in edges]
        # define adjs where free_adjs[i] is a set of the free adjacencies for the vertex i+1
        adjs = [set() for _ in range(n_vertices)]
        for edge in edges:
            adjs[edge[0]-1].add(edge[1])
            adjs[edge[1]-1].add(edge[0])

        input_graph.close()

    print(n_vertices)
    print(n_edges)
    print(edges)
    print(adjs)

    with open(scen, "r") as input_scen:

        n_agents = int(input_scen.readline())

        positions = input_scen.read()
        positions = positions.split("\n")[:-1]

        # remove START: and GOAL:
        positions = positions[1:n_agents+1] + positions[n_agents+2:]

        # parse positions to lists of two integers
        positions = [pos.split() for pos in positions]
        positions = [[int(pos[j]) for j in range(2)] for pos in positions]

        # define start and goal vectors
        start_pos = [None] * (n_agents+1)
        goal_pos = [None] * (n_agents+1)

        for i in range(n_agents):
            start_pos[positions[i][0]] = positions[i][1]
        for i in range(n_agents, len(positions)):
            goal_pos[positions[i][0]] = positions[i][1]

        print("$$$$$$")
        print(start_pos)
        print(goal_pos)
        print("$$$$$$")

        # define agents where agents[i] is [current_pos, goal_pos] for the agent i+1
        agents = [[] for _ in range(n_agents)]
        for pos in positions:
            agents[pos[0]-1].append(pos[1])

        input_scen.close()

    print(n_agents)
    print(agents)

    # calculate min makespan using BFS
    min_makespan = 2
    for a in agents:
        path_size = len(bfs(adjs, a))
        if path_size > min_makespan:
            min_makespan = path_size

    print("-------------")
    print(min_makespan)
    print("-------------")

    # Load minzinc model
    #model = Model("./mapf.mzn")

    # Mininc config for geocode
    # solver = Solver.lookup("gecode")

    # Create an Instance of the model
    # instance = Instance(solver, model)

    # graph variables
    #instance["n_vertices"] = n_vertices
    #instance["n_edges"] = n_edges
    #instance["adj"] = adjs

    # agents variables
    #instance["n_agents"] = n_agents
    #instance["start"] = start_pos[1:]
    #instance["goal"] = goal_pos[1:]

    #instance["makespan"] = makespan
    #result = instance.solve()

    data = {'n_vertices': n_vertices,
            'n_edges': n_edges,
            'adj': adjs,
            'n_agents': n_agents,
            'start': start_pos[1:],
            'goal': goal_pos[1:]
            }

    makespan = min_makespan
    output = b"UNSATISFIABLE"
    while b"UNSATISFIABLE" in output and makespan < 100:

        data['makespan'] = makespan

        with open("data.dzn", "w") as _:
            pymzn.dict2dzn(data, fout='./data.dzn')

        # output = check_output(["minizinc", "-c", "--solver", "Gecode", "mapf.mzn", "data.dzn", "|", "minizinc", "--ozn-file", "mapf.ozn"])
        # print(output)
        sp = subprocess.Popen(['minizinc', '--solver', 'Gecode', 'mapf.mzn', 'data.dzn'],
                              stdout=subprocess.PIPE,  stderr=subprocess.PIPE)

        output = sp.stdout.read()

        makespan += 1

    print_output(output)


def bfs(adjs, agent):

    global START
    global GOAL

    visited = []
    queue = [agent[START]]

    if agent[START] == agent[GOAL]:
        return visited

    while queue:
        node = queue.pop(0)
        if node not in visited:
            visited.append(node)
            for adj in adjs[node-1]:
                if adj == agent[GOAL]:
                    visited.append(adj)
                    return visited
                if adj not in visited:
                    queue.append(adj)


if __name__ == '__main__':
    graph = "input_graph.txt"
    scen = "input_scen.txt"

    main(graph, scen)
