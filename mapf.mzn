include "globals.mzn";
include "nosets.mzn";

% -----------------------%
% Variables from python
% -----------------------%

% Graph
int: makespan;
int: n_vertices;
int: n_edges;
set of int: VERTICES = 1..n_vertices;
set of int: TIMESTAMPS = 1..makespan;
set of int: TIMESTAMPSMINUS1 = 1..makespan-1;
set of int: DISTANCES = -1..n_edges+1;
array[VERTICES] of set of VERTICES: adj;

% Agents
int: n_agents;
set of int: AGENTS = 1..n_agents;
array[AGENTS] of VERTICES: start;
array[AGENTS] of VERTICES: goal;
array[AGENTS, VERTICES] of DISTANCES: min_d;

% position of each agent in a timestamp e.g. t0 = [agent1_pos, agent2_pos, agent3_pos]
array[TIMESTAMPS, AGENTS] of var VERTICES: ts_pos;

%-----------------------------------------

include "alldifferent.mzn";

% Define start and goal  postiions
constraint forall(p in AGENTS)( 
                  ts_pos[1, p] = start[p]
                            /\
                  ts_pos[makespan, p] = goal[p]
                 );

% Still possible to reach goal of every vertex
constraint forall(t in TIMESTAMPS, p in AGENTS)(makespan >= t + min_d[p, ts_pos[t,p]]);

% count number of repeated positions (max 1 per positions -> same agent)
constraint forall (t in TIMESTAMPSMINUS1, p in AGENTS)(count(row(ts_pos, t), ts_pos[t+1, p]) <= 1);

% All agents in different vertex
constraint forall(t in TIMESTAMPS)(alldifferent([ts_pos[t, p] | p in AGENTS]));

% Agent cannot move to a previous occupied pos (follow another agent)
constraint forall(t in TIMESTAMPSMINUS1, p in AGENTS, a in AGENTS)(
                  if (a != p) then 
                      ts_pos[t+1,p] != ts_pos[t,a] 
                  endif
                  );

% No repeated timestamps
constraint forall(t in TIMESTAMPS)(alldifferent(row(ts_pos, t)));

% Possible movements for agents          
constraint forall(t in TIMESTAMPSMINUS1, p in AGENTS)(
                  ts_pos[t+1,p] in adj[ts_pos[t,p]]     
                              \/
                  ts_pos[t+1,p] = ts_pos[t,p]
                  );
                  
% Cannot intersect another agent or go to occupied pos
constraint forall(t in TIMESTAMPSMINUS1, p in AGENTS)(
                  ts_pos[t+1, p] = ts_pos[t, p] 
                              \/  
                  not exists(a in AGENTS)(ts_pos[t+1,p] = ts_pos[t,a])
                  );

solve :: int_search(row(ts_pos, 1) ++ row(ts_pos, makespan) ++ [ts_pos[t,p] | t in 2..makespan-1, p in AGENTS],
                      input_order, indomain_min)
      satisfy;