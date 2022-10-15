include "globals.mzn"; 
% Variables from python

% Graph
int: n_vertices = 5;
int: n_edges = 4;
set of int: VERTEX = 1..n_vertices;
set of int: EDGES = 1..n_vertices;
array[VERTEX] of set of EDGES: adj = [{2}, {1, 3, 5}, {2, 4}, {3}, {2}];

% Agents
int: n_agents = 3;
% agents[i] = [START, GOAL]
array[1..n_agents,1..2] of int: agents = [|1, 5
                                          |2, 2
                                          |5, 1|];

array[1..n_agents] of var 1..n_vertices: curr_pos = [1,2,5];
array[1..n_agents] of var 1..n_vertices: next_pos;

include "alldifferent.mzn";

constraint alldifferent(next_pos);
constraint forall(i in 1..n_agents)(next_pos[i] in adj[i]);
% constraint forall(i in 1..n_agents)(abs(next_pos[i]-row(agents,2)[2]) <= abs(curr_pos[i]-row(agents,2)[2]));

solve satisfy;