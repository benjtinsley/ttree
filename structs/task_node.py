from structs.talent_node import TalentNode

class TaskNode:
    def __init__(self, task_name, creation_time, is_burnt):
        self.task_name = task_name  # Name or description of the task
        self.creation_time = creation_time  # Time when the task was created
        self.last_access_time = creation_time  # Last time the task was accessed, initially set to creation time
        self.is_burnt = is_burnt  # Flag indicating if the Task Node is burnt out
        self.left_child = None  # Pointer to the left child Task Node
        self.right_child = None  # Pointer to the right child Task Node
        self.parent = None  # Pointer to the parent Task Node
    
    # Public functions
    def add_child(self, child_node) -> None:
        """
        Adds a child node to the Task Node tree.
        @param: is_burnout: Flag indicating if the Talent Node is burnt out.
        @param: child_node: Child Task Node to add.
        """
        if self.is_burnt:
            self._insert_unbalanced_task_node(child_node, TalentNode.task_head)
        else:    
            self._insert_balanced_task_node(child_node, TalentNode.task_head)
        return
    
    def recall_task_from_tree(self, task_name, access_time) -> bool:
        """
        Recalls a task from the Task Node tree.
        @param: task_name: Name of the task to recall.
        @param: access_time: Time when the task was accessed.
        """
        # if the task is in the tree, we need to update the access time
        if self.task_name == task_name:
            # if the task is burnt out, we need to reset it
            self.is_burnt = False
            self._update_access_time(access_time)
            self._promote_to_head()
            self._heapify()
            return True
        else:
            # if the task is not in the tree, we need to search the children
            if self.left_child:
                return self.left_child.recall_task_from_tree(task_name, access_time)
            if self.right_child:
                return self.right_child.recall_task_from_tree(task_name, access_time)
        return False
    
    # Private functions
    def _update_access_time(self, access_time) -> None:
        """
        Updates the last access time of the task.
        @param: access_time: Time when the task was accessed.
        """
        self.last_access_time = access_time
    
    def _promote_to_head(self) -> None:
        """
        Promotes a Task Node up the tree.
        This allows us to favor the most recently accessed tasks
        but also fix unbalanced trees, one task at a time.
        """
        # if this node has no parent, we have reached the top of the tree
        if not self.parent:
            return
        else:
            self._swap_node_content(self.parent)
        
        return self._promote_to_head(self.parent)

    def _insert_unbalanced_task_node(self, task_node, current_node) -> None:
        """
        Inserts a Task Node into the tree on the far right side, out of balance.
        @param: task_node: Task Node to insert.
        @param: current_node: Current node to check for children.
        """
        # if there is no head, make this the head
        if TalentNode.task_head is None:
            TalentNode.task_head = task_node
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

        if node is None or node.is_burnt:
            return  # Skip heapify for burnt out nodes or if node doesn't exist

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

        
