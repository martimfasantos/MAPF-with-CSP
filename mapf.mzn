include "globals.mzn"; 
include "alldifferent.mzn";
% Variables from python

% Graph
int: n_vertices;
int: n_edges;
array[1..n_vertices] of set of 1..n_vertices: adj;

% Agents
int: n_agents;
% agents[i] = [START, GOAL]
array[1..n_agents,1..2] of int: agents;

array[1..n_agents] of var 1..n_vertices: curr_pos = [ (i in 1..n_agents)(agents[i][1]) ];
array[1..n_agents] of var 1..n_vertices: next_pos;

% use makespan aka tempo maximo the variable to target minimize

% todas as posicoes tem de ser diferentes
constraint alldifferent(next_pos);

% so se podem mexer para casas ao lado
constraint forall(i in 1..n_agents)(next_pos[i] in adj[ curr_pos[i] ]);

% o ultimo estado tem de ser igual ao objetivo
constraint forall(i in 1..n_agents)(next_pos[i] = agents[i][2] );

% constraint forall(i in 1..n_agents)(abs(next_pos[i]-row(agents,2)[2]) <= abs(curr_pos[i]-row(agents,2)[2]));

% solve minimize makespan;

solve satisfy;