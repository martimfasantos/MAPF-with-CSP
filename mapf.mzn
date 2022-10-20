include "globals.mzn";
include "nosets.mzn";

% -----------------------%
% Variables from python
% -----------------------%

% Graph
int: makespan;
int: n_vertices;
int: n_edges;
array[1..n_vertices] of set of 1..n_vertices: adj;

% Agents
int: n_agents;
array[1..n_agents] of 1..n_vertices: start;
array[1..n_agents] of 1..n_vertices: goal;
array[1..n_vertices, 1..n_vertices] of -1..n_edges+1: min_d;

% position of each agent in a timestamp e.g. t0 = [agent1_pos, agent2_pos, agent3_pos]
array[1..makespan, 1..n_agents] of var 1..n_vertices: ts_pos;

%-----------------------------------------

include "alldifferent.mzn";

constraint forall(p in 1..n_agents)( 
                  ts_pos[1, p] = start[p]
                            /\
                  ts_pos[makespan, p] = goal[p]
                 );

% Still possible to reach goal of every vertex
constraint forall(t in 1..makespan, p in 1..n_agents)(makespan-t >= min_d[goal[p], ts_pos[t,p]] );

% All agents in different vertex
constraint forall(t in 1..makespan)(alldifferent([ts_pos[t, p] | p in 1..n_agents]));

% 
constraint forall (t in 1..n_agents, p in 1..n_agents, a in 1..n_agents)(if (a != p) then ts_pos[t+1,p] != ts_pos[t,a] endif);

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
