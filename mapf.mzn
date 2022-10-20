include "globals.mzn";
include "nosets.mzn";

% -----------------------%
% Variables from python
% -----------------------%

% Graph
int: makespan;
int: n_vertices;
set of int: VERTICES = 1..n_vertices;
int: n_edges;
set of int: DISTANCES = -1..n_edges+1;
array[VERTICES] of set of VERTICES: adj;

% Agents
int: n_agents;
array[1..n_agents] of VERTICES: start;
array[1..n_agents] of VERTICES: goal;
array[VERTICES, VERTICES] of DISTANCES: min_d;

% position of each agent in a timestamp e.g. t0 = [agent1_pos, agent2_pos, agent3_pos]
array[1..makespan, 1..n_agents] of var VERTICES: ts_pos;

%-----------------------------------------

include "alldifferent.mzn";

constraint forall(p in 1..n_agents)( 
                  ts_pos[1, p] = start[p]
                            /\
                  ts_pos[makespan, p] = goal[p]
                 );

% Still possible to reach goal of every vertex
constraint forall(t in 1..makespan, p in 1..n_agents)(makespan-t >= min_d[goal[p], ts_pos[t,p]] );

% function var int: count(array [int] of var int: x, var int: y)
constraint forall (t in 1..makespan-1, p in 1..n_agents)(count(row(ts_pos, t), ts_pos[t+1, p]) <= 1);

% All agents in different vertex
constraint forall(t in 1..makespan)(alldifferent([ts_pos[t, p] | p in 1..n_agents]));

% 
constraint forall (t in 1..makespan-1, p in 1..n_agents, a in 1..n_agents)(
                      if (a != p) then 
                        ts_pos[t+1,p] != ts_pos[t,a] endif);

% No repeated ts
constraint forall(t in 1..makespan)(alldifferent(row(ts_pos, t)));

% Possible movements           
constraint forall(t in 1..makespan-1, p in 1..n_agents)(
                    ts_pos[t+1,p] in adj[ts_pos[t,p]]     
                                \/
                    ts_pos[t+1,p] = ts_pos[t,p]
                  );
                  
% Cannot intersect another agent or go to occupied pos
constraint forall(t in 1..makespan-1, p in 1..n_agents)(
                  ts_pos[t+1, p] = ts_pos[t, p] 
                              \/  
                  not exists(a in 1..n_agents)(ts_pos[t+1,p] = ts_pos[t,a])
                  );

% int_search(ts_pos, dom_w_deg, indomain_min)
solve :: int_search(ts_pos, input_order, indomain_min)
      satisfy;
