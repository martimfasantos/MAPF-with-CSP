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

% position of each agent in a timestamp e.g. t0 = [agent1_pos, agent2_pos, agent3_pos]
array[1..makespan, 1..n_agents] of var 1..n_vertices: ts_pos;

%-----------------------------------------

include "alldifferent.mzn";

constraint forall(p in 1..n_agents)( 
                  ts_pos[1, p] = start[p]
                            /\
                  ts_pos[makespan, p] = goal[p]
                 );

constraint forall(t in 1..makespan)(alldifferent([ts_pos[t, p] | p in 1..n_agents]));

% possible movements           
constraint forall(t in 1..makespan-1, p in 1..n_agents)( 
                  ts_pos[t+1,p] in adj[ts_pos[t,p]]     
                                \/
                  ts_pos[t+1,p] = ts_pos[t,p]
                  );

% No repeated time steps
% constraint forall(t in 1..makespan)(alldifferent(row(ts_pos, t)));

% if reached goal, stop at goal pos
% constraint forall(t in 2..makespan)( 
%                 forall(p in 1..n_agents)(
%                     if(ts_pos[t-1,p] = goal[p]) then ts_pos[t,p] = ts_pos[t-1, p] endif
%                     ));

% *REGRA IMPORTANTE:* 
% se quando numa determinada posicao ja nao for possivel 
% chegar ao fim com o resto dos timestemps que falta, cancelar logo

constraint forall(t in 1..makespan-1, p in 1..n_agents)(
                  ts_pos[t+1, p] = ts_pos[t, p] 
                              \/  
                  not exists(a in 1..n_agents)(ts_pos[t+1,p] = ts_pos[t,a])
                  );

solve satisfy;

%output ["The resulting values are \(ts_pos).\n"];