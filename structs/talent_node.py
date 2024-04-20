from structs.task_node import TaskNode

class TalentNode:
    def __init__(self, name, burnout_limit = 2, max_tasks = 5, rank = 0):
        self.name = name
        self.parent = None
        self.left_child = None
        self.right_child = None
        self.recent_task_map = {}
        self.is_burnout = False
        self.is_mastered = False # TODO: make this apparent by rank and burnout limit
        self.task_head = None
        self.last_access = 0
        self.rank = rank
        self.burnout_limit = burnout_limit # Start with a low burnout limit, but will grow
        self.max_tasks = max_tasks # Start with a low max tasks limit, but will grow

    def store_task(self, task_name, current_time) -> None:
        """
        Stores a task in the Talent Node.
        @param: task_name: Name of the task to store.
        @param: current_time: Time when the task was stored.
        """
        self.recent_task_map[current_time] = task_name
        self.last_access = current_time
        # TODO: need to check for relearn, ie it's been too long since current_time and last current_time
        # TODO: check to check for burnout, ie too frequent between tasks in list
        if len(self.recent_task_map) >=  self.max_tasks:
            self.convert_tasks_to_nodes()

        # TODO: update access rank & move up the tree if needed (will this require a left and right root?)
        # TODO: move to left most node at depth and shift the rest down

    def recall_task_from_map(self, task_name, access_time) -> bool:
        """
        Recalls a task from the Task Node tree.
        @param: task_name: Name of the task to recall.
        @param: access_time: New time stamp to set the access time to.
        """
        if task_name in self.recent_task_map.values():
            key_to_move = None
            for creation_time, task in self.recent_task_map.items():
                if task == task_name:
                    key_to_move = creation_time
                    break
                
            if key_to_move:
                # if the task is in the recent task map, we need to update the access time
                del self.recent_task_map[key_to_move]
                # reinsert it at the end of the list with the new access time
                self.recent_task_map[key_to_move] = access_time
                return True
        else:
            # if the task is not in the recent task map, we need to search the tree
            return TaskNode.recall_task_from_tree(task_name, access_time)
        
    def _convert_tasks_to_nodes(self):
        print(f"Converting tasks to Task Nodes for Talent Node '{self.name}'.")
        # convert the recent tasks to task nodes
        for creation_time, task in self.recent_task_map.items():
            task_node = TaskNode(task, creation_time, self.is_burnout)
            TaskNode.add_child(self.is_burnout, task_node)

        self.recent_task_map.clear()

        # promote this node if it's not burnt out
        if not self.is_burnout:
            # update the rank and the max_tasks, we've learned something!
            self.rank += 1
            self.max_tasks += 1
            # every other time we learn something, we increase the burnout limit
            if self.max_tasks % 2 != 0:
                self.burnout_limit += 1
