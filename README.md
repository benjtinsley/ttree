# T Tree data structure

>
> All my little plans and schemes, lost like some forgotten dreams. Seems that all I really was doing was waiting for you.
> 
> John Lennon, _Real Love_

The T Tree data structure aims to blend human cognitive behaviors with data management, emulating learning, memory, focus, and the satisfaction that comes along with skill mastery. This readme discusses the T Tree’s framework, its invariants and unique constraints, and potential interdisciplinary applications. I've also included a narrative about my thought process as to why I wanted to build this in the first place.

## Table of Contents
1. [Invariants](#invariants)
   - [Data Structures](#data-structures)
     - [T Tree](#t-tree)
     - [Talent Nodes](#talent-nodes)
     - [Task Nodes](#task-nodes)
   - [Actions](#actions)
     - [add_task()](#add_task)
     - [access_task()](#access_task)
     - [die()](#die)
1. [Example](#example)
1. [Tests](#tests)
1. [Potential Applications](#potential-applications)
1. [Narrative](#narrative)
1. [Weird Thoughts and Places My Brain Went](#weird-thoughts-and-places-my-brain-went)


## Invariants
### Data Structures
The __T Tree__ is comprised of 2 data structures: __Talent Nodes__ and __Task Nodes__, both of which are structured into binary trees, but with different properties.

#### T Tree
Every Talent Node is initialized with the following properties. Type denoted in parenthesis:
- __head__: Pointer to an uncountable and unknown head with no name and rank of infinity, from which all Talent Nodes come (_Talent Node_)
- __time__: The current time of the T Tree (_integer_)
- __total_nodes__: The total Talent Nodes in the T Tree (_integer_)
- __lost_talents__: A list of all Talent Nodes that must be cut from the tree, but cannot be totally removed (_list: Talent Node_)

#### Talent Nodes
Every Talent Node is initialized with the following properties. Type denoted in parenthesis:
- __name__: The name of the talent (_string_)
- __rank__: The current rank (_integer_)
- __last_access__: The time value in which the last access to this node happened (_integer_)
- __parent__: Pointer to the parent (_Talent Node_)
- __child_left__: Pointer to the left child (_Talent Node_)
- __child_right__: Pointer to the right child (_Talent Node_)
- __recent_task_map__: Key value mapping of recent tasks added to this talent as the time it was added and name of task (_int, string_)
- __max_tasks__: Number of tasks that can be added to the recent_task_map before they are all converted to Task Nodes (_int_)
- __task_head__: Pointer to the head of the Task Nodes (_Task Node_)
- __burnout_limit__: How the greatest delta between sequential key values in tasks that can be added to this talent before it is burnt out (_integer_)
- __is_burnout__: Flag if this talent is burnt out or not (_boolean_)
- __is_mastered__: Flag denoting if this talent has been mastered (_boolean_)

#### Task Nodes
Every Talent Node is initialized with the following properties. Type denoted in parenthesis:
- __task_name__: The name of the task (_string_)
- __child_left__: Pointer to the left child (_Task Node_)
- __child_right__: Pointer to the right child (_Task Node_)
- __parent__: Pointer to the parent (_Task Node_)
- __creation_time__: Time when the task was created (_integer_)
- __last_access_time__: Last time the task was accessed, initially set to creation time (_integer_)
- __is_burnt__: Flag indicating if the Task Node was created or last accessed while the parent Talent Node was burnt out (_boolean_)

### Actions
The T Tree only has two front end actions, __add_task()__ and __access_task()__. The steps of which are defined:

#### add_task(task_name: _string_=required, talent_name: _string_=optional) -> _void_
1. Using pre-order recursive search, the tree fetches the Talent Node associated with `talent_name` given.
    - If no talent node is found, a new talent node with rank 0 is created, and the number of total nodes is incremented.
1. The current time of the tree is incremented.
1. The talent node is then shifted to the left most position at its rank, denoting it has been accessed the most recently.
    - If shifting it to the leftmost position creates too many nodes at this level (ie, the talent node is added to rank 0 and rank 0 is currently full), the right most node is cast to the Lost Talents list to make way for this new, exciting talent and the total number of nodes is decremented.
1. The task is then added to the node as the final position in the Recent Task Map with the current time as its key and `task_name` as its value.
    - If the current time minus the time of the last item in the Recent Task Map is less than double the total nodes in the tree, the Recent Task Map is cleared out, denoting it's been too long since the last item was added, and everything must be relearned.
    - If the difference between any two time values for items in the Recent Task Map is less than the Burnout Limit on this Talent Node, the Is Burnout flag is set to true, otherwise it is set to false.
1. If the length of the Recent Task Map is equal to the Max Tasks on this Talent Node, the items in the Recent Task Map are converted to Task Nodes and the Talent Node rank is increased by 1.
    - If Is Burnout is set to true, the Task Nodes are added in order as the right child of the right most Task Node in the tree. Each Task Node is initialized with Is Burnt set to true.
    - If Is Burnout is set to false, the Task Nodes are added in order as the first open position when traversing the tree top to bottom, left to right.
    - In both cases, the Creation Time and the Last Access Time are both set to the current time.
    
##### Talent Node Promotion
1. If the Talent Node Rank increased in the last step, the Talent Node is promoted, meaning it joins the Talent Nodes of the new rank at their depth, if they exist, or is put onto a new depth all alone.
    - If the rank of the parent node is the same as the Talent Node rank, it means that the Talent Node will removed from its current rank depth and added into its parent's rank depth. In this case, there is a potential for sending nodes to the Lost Talents list at these levels, relative to the Talent Node:
        - Parent Rank
        - Child Rank
    - If the rank of the parent node is not the same as the Talent Node rank, it means that the Talent node will be removed from its current rank depth and put on a new depth between its parent's depth and its former depth. In this case, there is a potential for sending nodes to the Lost Talents list at these levels, relative to the Talent Node:
        - Current Rank
        - Child Rank
1. The Talent Node is inserted to the left-most position at the new rank depth. Nodes that can no longer fit in the tree, due to lack of bonds will be cast to the Lost Talents list, along with any recursive child Talent Nodes they may have.


#### access_task(task_name: _string_=optional, talent_name: _string_=optional) -> _boolean_
1. Using pre-order recursive search, the tree fetches the Talent Node associated with `talent_name` given.
1. The current time of the tree is incremented.
    - If no Talent Node of the given node was found (perhaps this Talent Node was placed in the Lost Talents list?) the function __returns false__.
1. The task is sought out in the Talent Node. First, the Recent Task Map is searched for the `task_name`.
    - If the task is found, __return true__.
1. The Task Nodes are searched via in-order search from the Task Head.
    - If no Task Head exists, or no Task Node exists with the matching `task_name`, __return false__.
    - If a Task Node exists with the matching `task_name`, it updates the Last Access Time on the matching Task Node.
1. The Task Node tree is then converted to a max heap by the Last Access Time, only for the Task Nodes where Is Burnt is set to false. The Task Nodes where Is Burnt is set to true are put at the end of the heap. Finally, it __returns true__.


There is a third and lesser used action, `die()` which allows all Talent Nodes and Task Nodes to be removed from memory.


#### die(node: _TalentNode_, show_life: _boolean_=optional) -> void
It begins at the Head Node of the T Tree, and recursively searches for each of the Talent Node children, doing the following:
1. Delete the Tasks in the Recent Task Map
1. Recursively delete the Task Nodes starting with the task_head.
1. Delete the Talent Node
1. Go through each item in the Lost Talents list and repeat steps 1 and 2 for each Talent Node there.

If `show_life` is set to True, each Talent Node Name and task name will be printed into the console before it is deleted.

## Example
(Recommended to read this at [README.md](/README.md) with the file explorer turned off (command/control + B).

Let's show an example of adding tasks to a Talent Node to update its rank. Given the tree below, we can see the Talent Nodes D, E, F & G at the bottom at rank 0, Talent Nodes B and C above them at rank 2, above them is rank 4 Talent Node A, and at the top is a nameless Talent Node at rank infinity. The purpose of it is to ensure more than 1 node can be added to the tree, by offering a left and right position for the first 2 nodes. It's mysterious that it has to work like this.
```ascii

                                 Talent Nodes

┌─  ──  ──  ──  ──  ──  ──  ──  ──  ┳━━━┓
 Rank ∞                             ┃   ┃
 ──  ──  ──  ──  ──  ──  ──  ──  ──┌┻━━━┛
                                   │
                                   │
┌─  ──  ──  ──  ──  ──  ──  ──  ─┳━┻━┓
 Rank 4                          ┃ A ┃
 ──  ──  ──  ──  ──  ──  ──  ──┌─┻━━━┻┐
                               │      │
┌─  ──  ──  ──  ──  ──  ┳━━━┳──┘──  ──└──┳━━━┓
│Rank 2                 ┃ B ┃            ┃ C ┃
└  ──  ──  ──  ──  ── ┌─┻━━━┻┐ ──  ──  ┬─┻━━━┻─┐
┌─  ──  ──  ──  ──┏━━━┫ ──  ─╋━━━┳ ┏━━━┫──  ── ┣━━━┓
│Rank 0           ┃ D ┃      ┃ E ┃ ┃ F ┃       ┃ G ┃
└  ──  ──  ──  ── ┗━━━┛──  ──┗━━━┛ ┻━━━┻─  ──  ┻━━━┛
```

Now, we want to add 4 tasks to Talent Node C, which is currently at rank 2:

```ascii
┌──────────────────────┐
│add_task('1', 'C')    │          Talent Nodes
│add_task('2', 'C')    │
│add_task('3', 'C')    │             ┏━━━┓
│add_task('4', 'C')    │             ┃   ┃
└──────────────────────┘            ┌┻━━━┛
                                    │
                                    │
                                  ┏━┻━┓
                                  ┃ A ┃
                                ┌─┻━━━┻┐
                                │      │
                         ┏━━━┳──┘      └──┳━━━┓
                         ┃ B ┃            ┃ C ┃
                       ┌─┻━━━┻┐         ┌─┻━━━┻─┐
                   ┏━━━┫      ┣━━━┓ ┏━━━┫       ┣━━━┓
                   ┃ D ┃      ┃ E ┃ ┃ F ┃       ┃ G ┃
                   ┗━━━┛      ┗━━━┛ ┗━━━┛       ┗━━━┛
```

When adding the first task, it recursively searches the tree for Talent Node "C" by first checking the head, then A, then B, D, E and finally C.

```ascii
┌──────────────────────┐
│add_task('1', 'C')    │─ ─ ─ ┐   Talent Nodes
└──────────────────────┘
                              └ ─ ─ ▶┏━━━┓
                                     ┃   ┃
                                    ┌┻━━━┛
                                   ─│
                                  │ │
                                  ▼━┻━┓
                           ┌ ─ ─ ─┃ A ┃
                                ┌─┻━━━┻┐
                           ▼    │      │
                         ┏━━━┳──┘      └──┳━━━┓
                      ─ ─┃ B ┃   ─ ─ ─ ─ ▶┃ C ┃
                     ▼ ┌─┻━━━┻┐ │       ┌─┻━━━┻─┐
                   ┏━━━┫      ┣━━━┓ ┏━━━┫       ┣━━━┓
                   ┃ D ┃      ┃ E ┃ ┃ F ┃       ┃ G ┃
                   ┗━━━┛      ┗━━━┛ ┗━━━┛       ┗━━━┛
                     │          ▲
                                │
                     └ ─ ─ ─ ─ ─
```
We will update the time:
```ascii
┌──────────────────────┐
│add_task('1', 'C')    │          Talent Nodes
└──────────────────────┘
                                     ┏━━━┓
┌──────────────────────────┐         ┃   ┃
│ ttree.current_time += 1  │        ┌┻━━━┛
└──────────────────────────┘        │
                                    │
                                  ┏━┻━┓
                                  ┃ A ┃
                                ┌─┻━━━┻┐
                                │      │
                         ┏━━━┳──┘      └──┳━━━┓
                         ┃ B ┃            ┃"C"┃
                       ┌─┻━━━┻┐         ┌─┻━━━┻─┐
                   ┏━━━┫      ┣━━━┓ ┏━━━┫       ┣━━━┓
                   ┃ D ┃      ┃ E ┃ ┃ F ┃       ┃ G ┃
                   ┗━━━┛      ┗━━━┛ ┗━━━┛       ┗━━━┛
```

We unhook it from its current bonds:
```ascii
┌──────────────────────┐
│add_task('1', 'C')    │          Talent Nodes
└──────────────────────┘
                                     ┏━━━┓
                                     ┃   ┃
                                    ┌┻━━━┛
                                    │
                                    │
                                  ┏━┻━┓
                                  ┃ A ┃
                                ┌─┻━━━┛
                                │
                         ┏━━━┳──┘         ┏━━━┓
                         ┃ B ┃            ┃"C"┃
                       ┌─┻━━━┻┐           ┗━━━┛
                   ┏━━━┫      ┣━━━┓ ┏━━━┓       ┏━━━┓
                   ┃ D ┃      ┃ E ┃ ┃ F ┃       ┃ G ┃
                   ┗━━━┛      ┗━━━┛ ┗━━━┛       ┗━━━┛
```
...and move it to the left-most position at this rank, shifting any other nodes to the right:
```ascii
┌──────────────────────┐
│add_task('1', 'C')    │          Talent Nodes
└──────────────────────┘
                                     ┏━━━┓
                                     ┃   ┃
                                    ┌┻━━━┛
                                    │
                                    │
                                  ┏━┻━┓
                                  ┃ A ┃
                                ┌─┻━━━┻┐
                                │      │
                         ┏━━━┳──┘      └──┳━━━┓
                         ┃"C"┃            ┃ B ┃
                       ┌─┻━━━┻┐         ┌─┻━━━┻─┐
                   ┏━━━┫      ┣━━━┓ ┏━━━┫       ┣━━━┓
                   ┃ D ┃      ┃ E ┃ ┃ F ┃       ┃ G ┃
                   ┗━━━┛      ┗━━━┛ ┗━━━┛       ┗━━━┛
```
Now we look into the Recent Task Map of Talent C and add it with the current time as the key:

```ascii
┌──────────────────────┐
│add_task('1', 'C')    │          Talent Nodes
└──────────────────────┘                                 ┌──────────────────────────────┐
                                     ┏━━━┓               │       Recent Task Map        │▓
                                     ┃   ┃               │                              │▓
                                    ┌┻━━━┛               │          {42: '1'}           │▓
                                    │                ┌ ▶ │                              │▓
                                    │             ┌ ─    │                              │▓
                                  ┏━┻━┓        ┌ ─       │         Max Tasks: 5         │▓
                                  ┃ A ┃     ┌ ─          └──────────────────────────────┘▓
                                ┌─┻━━━┻┐ ┌ ─              ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
                                │     ─│─
                         ┏━━━┳──┘┌ ─ ┘ └──┳━━━┓
                         ┃"C"┃─ ─         ┃ B ┃
                       ┌─┻━━━┻┐         ┌─┻━━━┻─┐
                   ┏━━━┫      ┣━━━┓ ┏━━━┫       ┣━━━┓
                   ┃ D ┃      ┃ E ┃ ┃ F ┃       ┃ G ┃
                   ┗━━━┛      ┗━━━┛ ┗━━━┛       ┗━━━┛
```
Now when we add the next task, the tree doesn't have to be traversed as thoroughly in order to find our desired Talent Node. Let's go ahead and add the next task to the tree:

```ascii
┌──────────────────────┐
│add_task('1', 'C')▤   │          Talent Nodes
│add_task('2', 'C')    │─ ─ ─ ┐                          ┌──────────────────────────────┐
└──────────────────────┘       ─ ─ ─▶┏━━━┓               │       Recent Task Map        │▓
                                     ┃   ┃               │                              │▓
                                    ┌┻━━━┛               │      {42: '1', 43: '2'}      │▓
                                   ─│                ┌ ▶ │                              │▓
                                  │ │             ┌ ─    │                              │▓
                                  ▼━┻━┓        ┌ ─       │         Max Tasks: 5         │▓
                           ┌ ─ ─ ─┃ A ┃     ┌ ─          └──────────────────────────────┘▓
                                ┌─┻━━━┻┐ ┌ ─              ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
                           ▼    │     ─│─
                         ┏━━━┳──┘┌ ─ ┘ └──┳━━━┓
                         ┃"C"┃─ ─         ┃ B ┃
                       ┌─┻━━━┻┐         ┌─┻━━━┻─┐
                   ┏━━━┫      ┣━━━┓ ┏━━━┫       ┣━━━┓
                   ┃ D ┃      ┃ E ┃ ┃ F ┃       ┃ G ┃
                   ┗━━━┛      ┗━━━┛ ┗━━━┛       ┗━━━┛
```
Now, let's show how it would look with all the specified tasks added to Talent Node C:
```ascii
┌──────────────────────┐
│add_task('1', 'C')▤   │          Talent Nodes
│add_task('2', 'C')▤   │                                 ┌──────────────────────────────┐
│add_task('3', 'C')▤   │─ ─ ─ ─ ─ ─ ▶┏━━━┓               │       Recent Task Map        │▓
│add_task('4', 'C')▤   │             ┃   ┃               │                              │▓
└──────────────────────┘            ┌┻━━━┛               │ {42: '1', 43: '2', 44: '3',  │▓
                                   ─│                ┌ ▶ │           45: '4'}           │▓
                                  │ │             ┌ ─    │                              │▓
                                  ▼━┻━┓        ┌ ─       │                              │▓
                           ┌ ─ ─ ─┃ A ┃     ┌ ─          │         Max Tasks: 5         │▓
                                ┌─┻━━━┻┐ ┌ ─             └──────────────────────────────┘▓
                           ▼    │     ─│─                 ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
                         ┏━━━┳──┘┌ ─ ┘ └──┳━━━┓
                         ┃"C"┃─ ─         ┃ B ┃
                       ┌─┻━━━┻┐         ┌─┻━━━┻─┐
                   ┏━━━┫      ┣━━━┓ ┏━━━┫       ┣━━━┓
                   ┃ D ┃      ┃ E ┃ ┃ F ┃       ┃ G ┃
                   ┗━━━┛      ┗━━━┛ ┗━━━┛       ┗━━━┛
```
Beautiful. Now the fun starts. Let's add one more task to Talent Node C:
```ascii
┌──────────────────────┐
│add_task('5', 'C')    │─ ─ ─ ┐   Talent Nodes
└──────────────────────┘                                 ┌──────────────────────────────┐
                              └ ─ ─ ▶┏━━━┓               │       Recent Task Map        │▓
                                     ┃   ┃               │                              │▓
                                    ┌┻━━━┛               │ {42: '1', 43: '2', 44: '3',  │▓
                                   ─│                ┌ ▶ │      45: '4', 46: '5'}       │▓
                                  │ │             ┌ ─    │ ──┐                          │▓
                                  ▼━┻━┓        ┌ ─       │   └──┐                    │  │▓
                           ┌ ─ ─ ─┃ A ┃     ┌ ─          │      └▶ Max Tasks: 5    ┌─┘  │▓
                                ┌─┻━━━┻┐ ┌ ─             │       Burnout Limit: 2 ◀┘    │▓
                           ▼    │     ─│─                └──────────────────────────────┘▓
                         ┏━━━┳──┘┌ ─ ┘ └──┳━━━┓           ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
                         ┃"C"┃─ ─         ┃ B ┃
                       ┌─┻━━━┻┐         ┌─┻━━━┻─┐
                   ┏━━━┫      ┣━━━┓ ┏━━━┫       ┣━━━┓
                   ┃ D ┃      ┃ E ┃ ┃ F ┃       ┃ G ┃
                   ┗━━━┛      ┗━━━┛ ┗━━━┛       ┗━━━┛
```
A few checks are made here:
1. We see that the Max Tasks now equals the total amount of tasks in the Recent Task Map
1. We check the Burnout Limit, which is 2. This means that when looping through all the nodes in the Recent Task Map, the difference between key of one task and the key of the next task in the list must be at least the Burnout Limit at least once in the list. Unfortunately for us, all these tasks were added in sequential order, so the greatest difference between any two nodes in order is 1.

Therefore, this Talent Node is burnt out. We need to now convert these tasks to Task Nodes, but since this node is burnt out, they will be added in a non-efficient manner. There are already Task Nodes in this Talent Node, because it is at rank 2, meaning the Recent Task Map has been converted to Task Nodes twice already. All the tasks in this Recent Task Map will be added to the right most position in the tree, relative to the Task Head. They will be saved along with their creation time and time they were last accessed as well as a flag marking this specific Task Node was added when the Talent Node was burnt out. For the purpose of space, we will only show the task name in the tree:

```ascii
                                                    ┌───────────┐
               Talent Nodes                         │C Task Head│
                                                    └─────▲▲────┘
                  ┏━━━┓                      ┌ ▶         ╱  ╲
                  ┃   ┃                   ┌ ─           ╱    ╲
                 ┌┻━━━┛                ┌ ─             ╱      ╲
                 │                  ┌ ─               ╱        ╲
                 │               ┌ ─                 ╱          ╲
               ┏━┻━┓          ┌ ─                   ╱            ╲
               ┃ A ┃       ─ ─                     ╱              ╲
             ┌─┻━━━┻┐ ┌ ─ ┘                       ╱                ╲
             │     ─│─                           ╱                  ╲
      ┏━━━┳──┘┌ ─ ┘ └──┳━━━┓                    ╱ ┌─────────────────┐╲
      ┃"C"┃─ ─         ┃ B ┃                   ╱  │                 │ ╲
    ┌─┻━━━┻┐         ┌─┻━━━┻─┐                ╱   │ (Balanced Tree) │  ╲
┏━━━┫      ┣━━━┓ ┏━━━┫       ┣━━━┓           ╱    │                 │   ╲
┃ D ┃      ┃ E ┃ ┃ F ┃       ┃ G ┃          ╱     └─────────────────┘    ╲
┗━━━┛      ┗━━━┛ ┗━━━┛       ┗━━━┛         ───────────────────────────────┐
                                                                          │
                                                                        ┏━┻━┓
                                                                        ┃'1'┃
                                                                        ┗━━┳┛
                                                                           └─┐
                                                                             │
                                                                           ┏━━━┓
                                                                           ┃'2'┃
                                                                           ┗━━┳┛
                                                                              └─┐
                                                                                │
                                                                              ┏━━━┓
                                                                              ┃'3'┃
                                                                              ┗━━┳┛
                                                                                 └─┐
                                                                                   │
                                                                                 ┏━━━┓
                                                                                 ┃'4'┃
                                                                                 ┗━━┳┛
                                                                                    └─┐
                                                                                      │
                                                                                    ┏━━━┓
                                                                                    ┃'5'┃
                                                                                    ┗━━━┛
```

Yikes! How inefficient and ugly! I bet you had to scroll down to see it all. Note that the only way to bring these Task Nodes back into a balanced tree is to access them again individually, which will update its last access time and set the burnt out flag to false. The Task Node tree will then max heapify itself for all nodes with the burnt out flag set to false by the last accessed time.

Ok that was fun! But we aren't done. We need to handle the rank and promotion of this node. 

We now clear out the Recent Task Map and increment the rank for Talent Node C, which now puts it at rank 3. 
```ascii
               Talent Nodes
                                      ┌──────────────────────────────┐
                  ┏━━━┓               │       Recent Task Map        │▓
                  ┃   ┃               │                              │▓
                 ┌┻━━━┛               │              {}              │▓
                 │                ┌ ▶ │                              │▓
                 │             ┌ ─    │                              │▓
               ┏━┻━┓        ┌ ─       │         Max Tasks: 5         │▓
               ┃ A ┃     ┌ ─          │       Burnout Limit: 2       │▓
             ┌─┻━━━┻┐ ┌ ─             │          Rank: +=1           │▓
             │     ─│─                └──────────────────────────────┘▓
      ┏━━━┳──┘┌ ─ ┘ └──┳━━━┓           ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
      ┃"C"┃─ ─         ┃ B ┃
    ┌─┻━━━┻┐         ┌─┻━━━┻─┐
┏━━━┫      ┣━━━┓ ┏━━━┫       ┣━━━┓
┃ D ┃      ┃ E ┃ ┃ F ┃       ┃ G ┃
┗━━━┛      ┗━━━┛ ┗━━━┛       ┗━━━┛
```
Just as a reminder, this was our starting ranks. So what do you think happens next?
```ascii
                                 Talent Nodes

┌─  ──  ──  ──  ──  ──  ──  ──  ──  ┳━━━┓
 Rank ∞                             ┃   ┃
 ──  ──  ──  ──  ──  ──  ──  ──  ──┌┻━━━┛
                                   │
                                   │
┌─  ──  ──  ──  ──  ──  ──  ──  ─┳━┻━┓
 Rank 4                          ┃ A ┃
 ──  ──  ──  ──  ──  ──  ──  ──┌─┻━━━┻┐
                               │      │
┌─  ──  ──  ──  ──  ──  ┳━━━┳──┘──  ──└──┳━━━┓
│Rank 2                 ┃"C"┃            ┃ B ┃
└  ──  ──  ──  ──  ── ┌─┻━━━┻┐ ──  ──  ┬─┻━━━┻─┐
┌─  ──  ──  ──  ──┏━━━┫ ──  ─╋━━━┳ ┏━━━┫──  ── ┣━━━┓
│Rank 0           ┃ D ┃      ┃ E ┃ ┃ F ┃       ┃ G ┃
└  ──  ──  ──  ── ┗━━━┛──  ──┗━━━┛ ┻━━━┻─  ──  ┻━━━┛
```
What we do first is check to see if Talent Node C's parent rank is the same rank. If it is, we know we will be inserting Talent Node C into the same rank as its parent, making it a sibling. Since it is not the same rank, as 4 != 3, we know that Talent Node C will keep its parent, but inherit its siblings as children.

Since Talent Node C only has a single sibling at rank 2, Talent Node B, it will inherit a new left child in Talent Node B, but will not have any other children.

However, in doing so, there aren't enough parents for all the nodes in rank 0 to stay in the tree. Unfortunately Talent Nodes F and G must be lost from the tree, but they aren't gone, just added to the Lost Talents list. They will never be accessible again, but will persist in memory.

Therefore, the final tree structure, with ranks will be as follows:

```ascii
                                  Talent Nodes

┌─  ──  ──  ──  ──  ──  ──  ──  ──  ─┳━━━┓
│Rank ∞                              ┃   ┃
└  ──  ──  ──  ──  ──  ──  ──  ──  ─┬┻━━━┛
                                    │
                                    │
┌─  ──  ──  ──  ──  ──  ──  ──  ──┏━┻━┓
│Rank 4                           ┃ A ┃
└  ──  ──  ──  ──  ──  ──  ──  ─┬─┻━━━┛
                                │
┌─  ──  ──  ──  ──  ──  ─┳━━━┳──┘
│Rank 3                  ┃"C"┃
└  ──  ──  ──  ──  ──  ┬─┻━━━┛          ┌──────────────────────────────┐
┌─  ──  ──  ──  ── ┏━━━┫                │            T Tree            │▓
│Rank 2            ┃ B ┃                │                              │▓
└  ──  ──  ──  ──┌─┻━━━┻─┐              │    Lost Talents: [ F, G ]    │▓
┌─  ──  ──  ─┳━━━╋  ──  ─╋━━━┓          └──────────────────────────────┘▓
│Rank 0      ┃ D ┃       ┃ E ┃           ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
└  ──  ──  ──┗━━━┛ ──  ──┗━━━┛
```
[ All Diagrams Created with [Monodraw](https://monodraw.helftone.com/) ]

## Tests

This repo uses pytest. You can view the tests in the /test directory. To run the test suite, simply run 

```bash
pip install -r requirements.txt # installs rich and colorama for better test formatting
python3 -m tests
```

It will generate the following results:

```bash
  Class            Test                                          Result  
 ─────────────────────────────────────────────────────────────────────── 
  TestTTree        test_add_single_talent                        PASS    
  TestTTree        test_add_three_talents_with_lost_node         PASS    
  TestTTree        test_add_two_talents                          PASS    
  TestTTree        test_kill_tree                                PASS    
  TestTTree        test_promote_talent_in_gapped_balanced_tree   PASS    
  TestTTree        test_promote_talent_in_robust_balanced_tree   PASS    
  TestTTree        test_time                                     PASS    
  TestTalentNode   test_check_talent_node_exists                 PASS    
  TestTalentNode   test_is_burnout_toggleable                    PASS    
  TestTalentNode   test_relearn                                  PASS    
  TestTalentNode   test_time_function_retrieval                  PASS    
```

## Potential Applications
The T Tree’s cognitive emulation lends itself to several applications: educational software that optimizes learning with cognitive patterns, to ensure mastery of knowledge in a short amount of time; cognitive science for visualizing and treating memory-related disorders, where researchers and doctors can create a virtual representation of a patient’s memory to diagnose exceptions in their cognition; and game development, where character progression strategies can significantly impact performance, leading to faster and more powerful actions if the progressions are done in a deliberate clustered manner, or less responsive, weaker actions if the progressions are done with too much or too little focus. This structure offers a framework for studying balanced task engagement and the cognitive aspects of learning and recovery as it relates to human endeavor. 

## Narrative
This was my final project for CU's CSPB 2270 Data Structures in spring 2024. This class offered me something on a deeper level than I think any class or topic has ever had for me. Each week, we were given a puzzle to solve in the form of a toy data structure with their strict invariants, and we were set off to build out the features that allowed the tests to pass. Not to mention, the lectures were extremely succinct and quick to watch. I could spend less than hour watching the weekly lectures and be on my way, with a compass and a basic idea of where I needed to go.

The BTrees week, for me, reached a tipping point. That assignment consumed me in a way that I never anticipated. All I wanted to do was work on it. I'm the type of person who gets more enjoyment out of something by going my own way, versus following someone else's instructions. I'd much rather turn in something wrong than something I didn't have to think to complete. Therefore, the BTrees assignment gave me many paths to explore to make it feel like an adventure. Lots of late nights. Many moments where I had to force myself away from the computer just so I could eat or see my family. It consumed me.

I turned in the BTrees assignment incomplete. I left off the remove function, but still ended up with a score with well over 100% and I promised I'd come back to the assignment over spring break or some other time when I had a lighter schedule. But the further time passed from BTrees, the more I thought about what happened to me during that project and the less I liked it. Computer Science attracts problem solvers and certain problems can consume people. It's genuinely fun to solve these problems for them and being consumed by the problem feels good and right. But something bothered me about that - during the BTrees assignment, I was being trained to think like a computer. Ultimately, it didn't matter what the bigger picture for the problem was, or the greater application (efficient storage?), it was that I was given a hard problem and step by step, I could solve that.

A question started to bother me - could there be a problem that attracted me based on it's difficulty, in which the application was unethical? Could my desire to solve problems be used as a way to do evil things by other people? These questions seemed a bit dramatic, but it bothered me and for the rest of the class, I kept the assignments at arm's length. They were still fun but I wouldn't allow myself to be consumed by them. My life was my life, after all. I wasn't a computer.

But still, the idea of data structures seemed powerful to me. It was a way to create a universe of rules in which amazing things were possible.

The week after the BTrees, we studied ADTs, which was interesting to me. It felt like a recap of everything we had studied up to that point, but set it all under an umbrella. We didn't have to worry about how it worked, just that it behaved in a way that was expected. During the lectures, my mind started to wander and I scribbled down some "Custom ADTs", as I defined them:
- ADT of ADTs where the inner ADT is known only when looked at via timestamp for entry/exit from queue - as a way to track emotions.
- ADT of population features that reveal outcomes due to feature contraints, as in, a way to predict wars or cultural phenomena.
- ADT of attributes that automatically increment if accessed or decrement if unaccessed - for traits/growth.

These had my gears grinding in the background for some time as I continued the course. By the time the final project was announced, I had already gotten quite far in my mind on the third ADT. Perhaps it can increment but cannot decrement? Which structure would best be suited for this? Graph? Hash Table? Tree? What if there were more than one dimension to the denote the proficiency? I kept a running log of my thoughts on my dry erase board and it continued to haunt me. It felt like it was writing itself and all I had to do was put my attention to it for a little longer and it would reveal something else to me. The rules were all already there, I just had to write them down.

I would define myself as a jack-of-all-trades type person. Mastery, for whatever reason, is very difficult for me, and I often change gears before going deeper. It seemed that every time I thought about this emerging data structure, it revealed something to me about myself and how I view my own talents. Promoting talents, which in the real world is spending more time doing something is an opportunity cost. By spending time with one thing, it cuts you off from spending time with something else. Perhaps the reason why mastery was difficult for me is there are things I don't want to get rid of. Perhaps there are things I don't want to lose. It's easier to lose something flighty and temporal than lose something large amounts of time have been invested in, so I opt for the former because I'm afraid of losing the latter. As the John Lennon quote at the beginning states, perhaps I mire in the plans and schemes because I think I haven't found the Thing<sup>TM</sup> that will promote itself to the top yet.

This class focused on efficient getting, setting, deleting and editing of information. This is an important thing to learn, but I also believe that efficiency shouldn't always be the goal in life. Efficiency is selfish and ruthless. It bypasses all other desires to accomplish the goal in as little time as possible. Optimum, on the other hand, takes many things into account to accomplish in a wholistic approach. After all, if I were to ask you to imagine the most efficient workday as you could imagine and the most optimal workday you could imagine, I think the former would have you feeling frazzled and burnt out, while the latter would leave you feeling accomplished and satisfied.

I like to think that this data structure forces optimalization. It forces a benevolent maintainer, someone who decides if a task is really worth adding because it could potentially lose other tasks. Other data structures focus on keeping everything and putting it wherever, but callously deleting it when it's no longer needed. The T Tree forces us to consider, is this really worth my time? At the end of the day, I'd love to show a computer the limitations of human memory, so that we can both potentially make it more optimal. 

I know what you are probably thinking. T Tree already exists as a data structure. Sure it does, but I think my name fits better, and here's why:
- It's made up of **T**alent Nodes and **T**ask Nodes
- My last name is **T**insley
and
- It reflects the T-shaped skills, which is a necessary constraint of this data structure: very few Talents can have the depth of the highest ranked one, but many Talents can spread out horizontally underneath it.

## Weird Thoughts and Places My Brain Went
- Should Talent Nodes in the Lost Talent list be preserved? Although inaccessible, would it imply some sort of reincarnation or past life?
- Would it make sense for the God Node ie the Talent Node head to be infinitely scalable so that there's no limit to the amount of initial Talents one can add, but once one gets promoted, all but 3 are lost? Converseley, if possible, having a way for someone to multiple maxed out Talents at the top.
- Mastery, which was never touched on, should bypass burnout and the relearn scenario, or at least minimize the effects of both.
- As humans, we like to orient ourselves in pyramid shaped structures, with less people at the top than the bottom. However, after working through this, I've found that promotion in this structure shape is highly inefficient at best and ruthless at worst. Someone can be promoted to a level that someone else already has, but it's either to create a harder communication pattern for the person on top to all the other people, or it will thrust someone out, or it will give someone "nothing to do" ie, no child nodes. Or it will create a bottleneck and the organization will potentially have to lose many divisions to accomodate. Is there a more optimal structure for humans to arrange ourselves in to ensure a more efficient flow of power, communication and responsibility?
- Should there be a randomized `final_time` on the T Tree that forces `die()` when the current time reaches it?
- Check out [/notes_stack.md](/notes_stack.md) to view more stream of consciousness thoughts and unrealized desires for this project.
