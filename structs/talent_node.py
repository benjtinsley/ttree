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
            # if the task is not in the recent task map, we need to search the tree, starting from the head
            return self._recall_task_from_tree(self.task_head, task_name, access_time)
        
    def _convert_tasks_to_nodes(self):
        print(f"Converting tasks to Task Nodes for Talent Node '{self.name}'.")
        # convert the recent tasks to task nodes
        for creation_time, task in self.recent_task_map.items():
            task_node = TaskNode(task, creation_time, self.is_burnout)
            self._add_task_node(task_node)

        self.recent_task_map.clear()

        # promote this node if it's not burnt out
        if not self.is_burnout:
            # update the rank and the max_tasks, we've learned something!
            self.rank += 1
            self.max_tasks += 1
            # every other time we learn something, we increase the burnout limit
            if self.max_tasks % 2 != 0:
                self.burnout_limit += 1



    # Public functions
    def _add_task_node(self, new_task_node) -> None:
        """
        Adds a node to the Task Node tree.
        @param: new_task_node: Task Node to add.
        """
        if self.is_burnout:
            self._insert_unbalanced_task_node(new_task_node, TalentNode.task_head)
        else:    
            self._insert_balanced_task_node(new_task_node, TalentNode.task_head)
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
            self._promote_task_node_to_head(task_node)
            task_node._heapify()
            return True
        else:
            # if the task is not in the tree, we need to search the children
            if task_node.left_child:
                return self._recall_task_from_tree(task_node.left_child, task_name, access_time)
            if task_node.right_child:
                return self._recall_task_from_tree(task_node.right_child, task_name, access_time)
        return False
    
    # Private functions
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
            self._swap_node_content(task_node, task_node.parent)
        
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
        if TalentNode.task_head is None:
            TalentNode.task_head = task_node
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
        left_position = self._insert_balanced(task_node, root_node.left_child)
        right_position = self._insert_balanced(task_node, root_node.right_child)

        return left_position or right_position


    def _heapify(self, node=None):
        """
        Balances the Task Node tree for all non-burnt out nodes in a
        max heap fashion based on last access time.
        @param: node: Node to start the heapify process from.
        """
        if node is None:
            node = TalentNode.task_head

        # Skip heapify for burnt out nodes or if node doesn't exist
        if node is None or node.is_burnt:
            return  

        largest = node

        if node.left_child and not node.left_child.is_burnt and node.left_child.last_access_time > node.last_access_time:
            largest = node.left_child
        if node.right_child and not node.right_child.is_burnt and node.right_child.last_access_time > largest.last_access_time:
            largest = node.right_child

        if largest != node:
            # Perform a swap
            self._swap_node_content(node, largest)
            # Recursively heapify the affected subtree
            self._heapify(largest)

    def _swap_node_content(self, node2):
        """
        Swaps the content of two nodes.
        @param: node2: Second node to swap.
        """
        self.task_name, node2.task_name = node2.task_name, self.task_name
        self.creation_time, node2.creation_time = node2.creation_time, self.creation_time
        self.last_access_time, node2.last_access_time = node2.last_access_time, self.last_access_time
        self.is_burnt, node2.is_burnt = node2.is_burnt, self.is_burnt

