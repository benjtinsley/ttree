from structs.task_node import TaskNode

class TalentNode:
    """
    Represents a Talent Node in the T-Tree.
    These are the nodes that hold the tasks.
    They are oriented as the highest rank at the top of the tree
    and the most recently accessed at the left of the tree.
    @param: name: Name of the Talent Node.
    @param: burnout_limit: Number of sequential allowed tasks before burnout.
    @param: max_tasks: Maximum number of tasks allowed before converting to nodes.
    @param: rank: Rank of the Talent Node.
    """
    def __init__(self, name, burnout_limit = 2, max_tasks = 5, rank = 0):
        self.parent = None
        self.left_child = None
        self.right_child = None
        self.name = name
        self.recent_task_map = {}
        self.is_burnout = False
        self.is_mastered = False # TODO: make this apparent by rank and burnout limit
        self.task_head = None
        self.last_access = -1 # TODO: incorporate more thoroughly
        self.rank = rank
        self.burnout_limit = burnout_limit # Start with a low burnout limit, but will grow
        self.max_tasks = max_tasks # Start with a low max tasks limit, but will grow

    # Public functions
    def store_task(self, talent_node, task_name: str, current_time: int, total_nodes: int) -> None:
        """
        Stores a task in the Talent Node.
        @param: task_name: Name of the task to store.
        @param: current_time: Time when the task was stored.
        @param: total_nodes: Total number of Talent Nodes in the tree.
        """
        # as long as we have an item in the recent task map, we need to see
        # if it's been too long since the last task
        if len(talent_node.recent_task_map) > 0:
            # get the last time a task was added
            last_time = list(talent_node.recent_task_map.keys())[-1]
            # if the time between the last task and this task is greater than the total nodes * 2
            if current_time - last_time >= total_nodes * 2:
                # we've forgotten everything, start over
                talent_node.recent_task_map.clear()
                return

        talent_node.recent_task_map[current_time] = task_name
        talent_node.last_access = current_time
    
        # if the recent task map is full, convert the tasks to nodes
        if len(talent_node.recent_task_map) >=  talent_node.max_tasks:
            # but first, check for burnout
            total_in_order = 0
            # use step to check for sequential tasks
            step = 1
            # get the keys in order
            keys = list(talent_node.recent_task_map.keys())
            # get the first key
            previous_time = keys[0]
            # check the rest of the keys
            for this_time in keys[1:]: 
                # if these tasks were added in sequence, we need to know
                if this_time - previous_time == step:
                    total_in_order += 1

                previous_time = this_time
            
            if total_in_order >= self.burnout_limit:
                # if more tasks were added in sequence than allowed, 
                # this talent node is burnt out
                talent_node.is_burnout = True
            else:
                # variety is the spice of life
                # TODO: make this more comprehensive?
                talent_node.is_burnout = False

            self.__convert_tasks_to_nodes(talent_node.recent_task_map)

        # TODO: update access rank & move up the tree if needed (will this require a left and right root?)
        # TODO: move to left most node at depth and shift the rest down

    def recall_task(self, task_head: TaskNode, task_name: str, current_time: int) -> bool:
        """
        Searches for a task in the Talent Node, first by checking the recent task map,
        then by searching the Task Node tree.
        @param: task_head: Head of the Task Node tree for this Talent.
        @param: task_name: Name of the task to recall.
        @param: current_time: New time stamp to set the access time to.
        @return: True if the task was found, False otherwise.
        """
        # first check the recent task map
        if self.__recall_task_from_map(task_name, current_time):
            return True
        # if the task wasn't found in the recent task map, search the tree
        return self.__recall_task_from_tree(task_head, task_name, current_time)

    # Private functions 
    def __recall_task_from_map(self, task_name: str, current_time: int) -> bool:
        """
        Recalls a task from the Task Node tree.
        @param: task_name: Name of the task to recall.
        @param: current_time: New time stamp to set the access time to.
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
                self.recent_task_map[key_to_move] = current_time
                return True
        else:
            # if the task is not in the recent task map, we need to search the tree, starting from the head
            return self.__recall_task_from_tree(self.task_head, task_name, current_time)

    def __recall_task_from_tree(self, task_node: TaskNode, task_name: str, current_time: int) -> bool:
        """
        Recalls a task from the Task Node tree.
        @param: task_node: Node to start the search from.
        @param: task_name: Name of the task to recall.
        @param: current_time: Time when the task was accessed.
        """
        # there's no task tree to search
        if task_node is None:
            return False
        # if the task is in the tree, we need to update the access time
        if task_node.task_name == task_name:
            # if the task is burnt out, we need to reset it
            task_node.is_burnt = False
            self.__update_task_node_access_time(task_node, current_time)
            # promote this one to the top of the tree
            self.__promote_task_node_to_head(task_node)
            # and heapify the tree, excluding burnt out nodes
            self.__heapify_task_nodes(task_node)
            return True
        else:
            # if the task is not in the tree, we need to search the children
            if task_node.left_child:
                return self.__recall_task_from_tree(task_node.left_child, task_name, current_time)
            if task_node.right_child:
                return self.__recall_task_from_tree(task_node.right_child, task_name, current_time)
        return False
    
    def __convert_tasks_to_nodes(self, task_map: dict) -> None:
        """
        Converts the recent tasks to Task Nodes.
        @param: task_map: Map of tasks to convert.
        """
        # convert the recent tasks to task nodes
        for creation_time, task in task_map.items():
            task_node = TaskNode(task, creation_time, self.is_burnout)
            self.__add_task_node(task_node)

        # clear the recent task map now that they are converted to nodes
        task_map.clear()

        # increase the features if it's not burnt out
        if not self.is_burnout:
            # update the rank and the max_tasks, we've learned something! 
            # this will make it easier to learn more
            self.max_tasks += 1
            # every other time we learn something, we increase the burnout limit
            if self.max_tasks % 2 != 0:
                self.burnout_limit += 1
        
        # update the rank of this node
        self.rank += 1
        # TODO: function to handle rank increase & promotion?

    def __add_task_node(self, new_task_node: TaskNode) -> None:
        """
        Adds a node to the Task Node tree.
        @param: new_task_node: Task Node to add.
        """
        if self.is_burnout:
            self.__insert_unbalanced_task_node(new_task_node, self.task_head)
        else:    
            self.__insert_balanced_task_node(new_task_node, self.task_head)
        return
    
    def __update_task_node_access_time(self, task_node: TaskNode, access_time: int) -> None:
        """
        Updates the last access time of the task.
        @param: task_node: Task Node to update.
        @param: access_time: Time when the task was accessed.
        """
        task_node.last_access_time = access_time
    
    def __promote_task_node_to_head(self, task_node: TaskNode) -> None:
        """
        Promotes a Task Node up the tree.
        This allows us to favor the most recently accessed tasks
        but also fix unbalanced trees, one task at a time.
        @param: task_node: Task Node to promote.
        """
        # if this node has no parent, we have reached the top of the tree
        if not task_node.parent:
            return
        else:
            self.__swap_task_node_content(task_node, task_node.parent)
        
        return self.__promote_task_node_to_head(task_node.parent)

    def __insert_unbalanced_task_node(self, task_node: TaskNode, current_node: int) -> None:
        """
        Inserts a Task Node into the tree on the far right side, out of balance.
        @param: task_node: Task Node to insert.
        @param: current_node: Current node to check for children.
        """
        # if there is no head, make this the head
        if self.task_head is None:
            self.task_head = task_node
            return
        
        # we only search down the right side of the tree if we are burnt out
        if not current_node.right_child:
            current_node.right_child = task_node
            task_node.parent = current_node
            return
        
        # if there are children, we need to go deeper
        return self.__insert_unbalanced_task_node(task_node, current_node.right_child)

    def __insert_balanced_task_node(self, task_node: TaskNode, root_node: int) -> bool:
        """
        Inserts a Task Node into the tree in a balanced manner, top to bottom, left to right
        @param: task_node: Task Node to insert.
        @param: root_node: Root node to start the search
        """
        # if there is no head, make this the head
        if self.task_head is None:
            self.task_head = task_node
            return True

        # if the head is burnt out, we need to make this the head
        if self.task_head.is_burnt:
            # this check shouldn't be necessary, but just a good reminder
            # that balanced tree insertions are only for non-burnt out nodes
            if not task_node.is_burnt:
                # make this the head
                self.task_head.parent = task_node
                task_node.right_child = self.task_head
                self.task_head = task_node
                return True
        
        # if there is no left child, make this the left child
        if root_node.left_child is None:
            root_node.left_child = task_node
            task_node.parent = root_node
            return True
        
        # if there is no right child, make this the right child
        if root_node.right_child is None:
            root_node.right_child = task_node
            task_node.parent = root_node
            return True

        # if there are children, we need to go deeper
        left_position = self.__insert_balanced_task_node(task_node, root_node.left_child)
        
        # we don't want to go down the right side if we find a burnt out node
        if not root_node.right_child.is_burnt:
            right_position = self.__insert_balanced_task_node(task_node, root_node.right_child)
        
        return left_position or right_position


    def __heapify_task_nodes(self, task_node: TaskNode = None) -> None:
        """
        Balances the Task Node tree for all non-burnt out nodes in a
        max heap fashion based on last access time.
        @param: node: Node to start the heapify process from.
        """
        if task_node is None:
            task_node = self.task_head

        # Skip heapify for burnt out nodes or if node doesn't exist
        if task_node is None or task_node.is_burnt:
            return  

        largest = task_node

        if task_node.left_child and not task_node.left_child.is_burnt and task_node.left_child.last_access_time > task_node.last_access_time:
            largest = task_node.left_child
        if task_node.right_child and not task_node.right_child.is_burnt and task_node.right_child.last_access_time > largest.last_access_time:
            largest = task_node.right_child

        if largest != task_node:
            # Perform a swap
            self.__swap_task_node_content(task_node, largest)
            # Recursively heapify the affected subtree
            self.__heapify_task_nodes(largest)

    def __swap_task_node_content(self, node1: TaskNode, node2: TaskNode) -> None:
        """
        Swaps the content of two task nodes.
        @param: node1: First node to swap.
        @param: node2: Second node to swap.
        """
        node1.task_name, node2.task_name = node2.task_name, node1.task_name
        node1.creation_time, node2.creation_time = node2.creation_time, node1.creation_time
        node1.last_access_time, node2.last_access_time = node2.last_access_time, node1.last_access_time
        node1.is_burnt, node2.is_burnt = node2.is_burnt, node1.is_burnt

    # Internal functions
    def _find_task_node(self, task_name: str, task_node: TaskNode) -> TaskNode:
        """
        Finds a Task Node in the tree. Used in testing. Maybe useful for debugging.
        @param: task_name: Name of the task to find.
        @param: task_node: Node to start the search
        @return: Task Node if found, None otherwise.
        """
        if task_node.task_name == task_name:
            return task_node
        else:
            if task_node.left_child:
                return self._find_task_node(task_name, task_node.left_child)
            if task_node.right_child:
                return self._find_task_node(task_name, task_node.right_child)
        return None
