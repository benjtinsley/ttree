# Notes, next steps, etc
## Current task
- [x] test relearn -> total nodes is returning raised to the power of 3
- [x] test burnout toggle off -> __insert_balanced_task_node is getting max recursion depth
- [x] test burnout - burnout never being set to true -> recent_task_map not storing all values -> ~time not being updated~ lost_talents cant be found
- [x] build burnout breakout
- [x] set burnout

## Running things to do
- [ ] determine what conditions cause mastery
- [ ] __convert_tasks_to_nodes: 3rd party function to handle rank increase & promotion
- [ ] talent node shifting has the tendency to duplicate nodes
- [ ] Promote talent nodes based on rank & move cut off nodes to lost_memory
- [x] How mastery (if built) affects burnout? (see below [Random thoughts](#random-thoughts) - burnout can't happen in that talent node)
- [ ] Visualization
- [x] Build methods for quicker access to task nodes in tests? (internal functions)
- [x] Figure out why add talent nodes is duplicating nodes when shifting
- [x] determine how relearn is calculated
- [x] determine how burnout is dealt and how it is removed in talentnode
- [x] brush up tests to pass
- [x] circular dependency pulling TalentNode class into task_node.py. should TalentNode own all the talent node functionality as well? refactor in order because I can't set or get the task_head in the current layout

## Random thoughts
- Mastery allows new tasks to be immediately converted into talent nodes, without the need for the map, bypassing burnout and relearn
- Relearn interval between tasks is 2 * total talent nodes - 1
