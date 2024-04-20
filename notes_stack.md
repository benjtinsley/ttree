# Notes, next steps, etc
## Current task
- [ ] test burnout
- [x] build burnout breakout
- [x] set burnout

## Running things to do
- [ ] Promote talent nodes based on rank & move cut off nodes to lost_memory
- [ ] How mastery (if built) affects burnout?
- [ ] Visualization
- [ ] Build methods for quicker access to task nodes in tests?
- [x] Figure out why add talent nodes is duplicating nodes when shifting
- [ ] determine how relearn is calculated
- [ ] determine how burnout is dealt and how it is removed in talentnode
- [x] brush up tests to pass
- [x] circular dependency pulling TalentNode class into task_node.py. should TalentNode own all the talent node functionality as well? refactor in order because I can't set or get the task_head in the current layout

## Random thoughts
- Mastery allows new tasks to be immediately converted into talent nodes, without the need for the map
- Relearn interval between tasks is 2 * total talent nodes - 1
