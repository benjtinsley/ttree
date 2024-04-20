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

    # Public functions
    def store_task(self, talent_node, task_name, current_time) -> None:
        """
        Stores a task in the Talent Node.
        @param: task_name: Name of the task to store.
        @param: current_time: Time when the task was stored.
        """
        talent_node.recent_task_map[current_time] = task_name
        talent_node.last_access = current_time
        # TODO: need to check for relearn, ie it's been too long since current_time and last current_time
    
        # if the recent task map is full, convert the tasks to nodes
        if len(talent_node.recent_task_map) >=  talent_node.max_tasks:
            # but first, check for burnout
            step = 1
            total_in_order = 0
            previous_time = list(talent_node.recent_task_map.keys())[0]
            for creation_time in range(1, len(talent_node.recent_task_map.keys())):
                # if these tasks were added in sequence, we need to know
                if creation_time - previous_time == step:
                    total_in_order += 1

                previous_time = creation_time
            
            if total_in_order >= self.burnout_limit:
                # if more tasks were added in sequence than allowed, 
                # this talent node is burnt out
                talent_node.is_burnout = True
            else:
                # variety is the spice of life
                # TODO: make this more comprehensive?
                talent_node.is_burnout = False

            talent_node._convert_tasks_to_nodes()

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
            # if the task is not in the recent task map, we need to search the tree, starting from the head
            return self._recall_task_from_tree(self.task_head, task_name, access_time)

    # Private functions   
    def _convert_tasks_to_nodes(self):
        # convert the recent tasks to task nodes
        for creation_time, task in self.recent_task_map.items():
            task_node = TaskNode(task, creation_time, self.is_burnout)
            self._add_task_node(task_node)

        # clear the recent task map now that they are converted to nodes
        self.recent_task_map.clear()

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

    def _add_task_node(self, new_task_node) -> None:
        """
        Adds a node to the Task Node tree.
        @param: new_task_node: Task Node to add.
        """
        if self.is_burnout:
            self._insert_unbalanced_task_node(new_task_node, self.task_head)
        else:    
            self._insert_balanced_task_node(new_task_node, self.task_head)
        return
    
    def _recall_task_from_tree(self, task_node, task_name, access_time) -> bool:
        """
        Recalls a task from the Task Node tree.
        @param: task_node: Node to start the search from.
        @param: task_name: Name of the task to recall.
        @param: access_time: Time when the task was accessed.
        """
        # if the task is in the tree, we need to update the access time
        if task_node.task_name == task_name:
            # if the task is burnt out, we need to reset it
            task_node.is_burnt = False
            self._update_task_node_access_time(task_node, access_time)
            # promote this one to the top of the tree
            self._promote_task_node_to_head(task_node)
            # and heapify the tree, excluding burnt out nodes
            self._heapify_task_nodes(task_node)
            return True
        else:
            # if the task is not in the tree, we need to search the children
            if task_node.left_child:
                return self._recall_task_from_tree(task_node.left_child, task_name, access_time)
            if task_node.right_child:
                return self._recall_task_from_tree(task_node.right_child, task_name, access_time)
        return False
    
    def _update_task_node_access_time(self, task_node, access_time) -> None:
        """
        Updates the last access time of the task.
        @param: task_node: Task Node to update.
        @param: access_time: Time when the task was accessed.
        """
        task_node.last_access_time = access_time
    
    def _promote_task_node_to_head(self, task_node) -> None:
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
            self._swap_task_node_content(task_node, task_node.parent)
        
        return self._promote_task_node_to_head(task_node.parent)

    def _insert_unbalanced_task_node(self, task_node, current_node) -> None:
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
            return
        
        # if there are children, we need to go deeper
        return self._insert_unbalanced_task_node(task_node, current_node.right_child)

    def _insert_balanced_task_node(self, task_node, root_node):
        """
        Inserts a Task Node into the tree in a balanced manner, top to bottom, left to right
        @param: task_node: Task Node to insert.
        @param: root_node: Root node to start the search
        """
        # if there is no head, make this the head
        if self.task_head is None:
            self.task_head = task_node
            return
        
        # if there is no left child, make this the left child
        if not root_node.left_child:
            root_node.left_child = task_node
            return
        
        # if there is no right child, make this the right child
        if not root_node.right_child:
            root_node.right_child = task_node
            return

        # if there are children, we need to go deeper
        left_position = self._insert_balanced_task_node(task_node, root_node.left_child)
        right_position = self._insert_balanced_task_node(task_node, root_node.right_child)

        return left_position or right_position


    def _heapify_task_nodes(self, task_node=None):
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
            self._swap_task_node_content(task_node, largest)
            # Recursively heapify the affected subtree
            self._heapify_task_nodes(largest)

    def _swap_task_node_content(self, node1, node2):
        """
        Swaps the content of two task nodes.
        @param: node1: First node to swap.
        @param: node2: Second node to swap.
        """
        node1.task_name, node2.task_name = node2.task_name, node1.task_name
        node1.creation_time, node2.creation_time = node2.creation_time, node1.creation_time
        node1.last_access_time, node2.last_access_time = node2.last_access_time, node1.last_access_time
        node1.is_burnt, node2.is_burnt = node2.is_burnt, node1.is_burnt

