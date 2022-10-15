from minizinc import Instance, Model, Solver

START = 0
GOAL = 1

def main():
    with open('input_graph.txt', "r") as input_graph:

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

    with open('input_scen.txt', "r") as input_scen:

        n_agents = int(input_scen.readline())

        positions = input_scen.read()
        positions = positions.split("\n")[:-1]
        # remove START: and GOAL:
        positions = positions[1:n_agents+1] + positions[n_agents+2:]
        # parse positions to lists of two integers
        positions = [pos.split() for pos in positions]        
        positions = [[int(pos[j]) for j in range(2)] for pos in positions]
        # define agents where agents[i] is [current_pos, goal_pos] for the agent i+1
        agents = [[] for _ in range(n_agents)]
        for pos in positions:
            agents[pos[0]-1].append(pos[1])
        # # remove initial positions from free_adj since there is a agent in those positions
        # for start, _ in agents:
        #     for adj in free_adjs:
        #         adj.discard(start)
                
        input_scen.close()

    # # Load n-Queens model from file
    # mapf = Model("./mapf.mzn")
    # # Find the MiniZinc solver configuration for Gecode
    # gecode = Solver.lookup("gecode")
    # # Create an Instance of the n-Queens model for Gecode
    # instance = Instance(gecode, mapf)
    # # Assign 4 to n
    # # instance["n_vertices"] = n_vertices
    # instance["n_agents"] = n_agents

    # result = instance.solve()
    # # Output the array q
    # print(result["solution"])

    print(n_agents)
    print(agents)

    print(bfs(adjs, agents[0]))
    print(bfs(adjs, agents[1]))
    print(bfs(adjs, agents[2]))

def bfs(adjs, agent):

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
    main()

#print(free_adjs)

# # Load n-Queens model from file
# nqueens = Model("./nqueens.mzn")
# # Find the MiniZinc solver configuration for Gecode
# gecode = Solver.lookup("gecode")
# # Create an Instance of the n-Queens model for Gecode
# instance = Instance(gecode, nqueens)
# # Assign 4 to n
# instance["n"] = 4
# result = instance.solve()
# # Output the array q
# print(result["q"])