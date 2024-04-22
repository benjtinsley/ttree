import math
from structs.talent_node import TalentNode

class TTree:
    def __init__(self):
        # Track total actions or time across the entire T Tree
        self.time = 0  
        self.total_nodes = 0
        self.lost_talents = []
        # The head node is an infinite rank Talent Node that is unreachable and unknown
        # TODO: should this be a different kind of node that can scale?
        self.head = TalentNode(name=None, rank=math.inf) 
    
    # Public functions
    def add_task(self, task_name: str, talent_name: str) -> None:
        # first, try to find the talent node
        talent_node = self._find_talent_node(talent_name, self.head)

        # if the talent node is not found, we need to add it
        if not talent_node:
            talent_node = self.__add_talent_node(talent_name, self.head)
            # and increment the total number of nodes
            self.total_nodes += 1

        # grab the starting rank of the talent node for comparison later
        starting_rank = talent_node.rank
        current_time = self.capture_flowing_time()
        talent_node.store_task(talent_node, task_name, current_time, self.total_nodes)

        # add this node to the left most position at this depth
        left_most_uncle = self.__get_left_most_talent_node_at_rank(self.head, talent_node.parent.rank)
        self.__shift_talent_nodes_right(talent_node, left_most_uncle)

        # the talent node's rank may have been updated, in store_task
        # if so, a promotion is in order
        if talent_node.rank > starting_rank:
            # self.__promote_talent_node()
            pass
        
        return

    def access_task(self, task_name: str, talent_name: str) -> None:
        """
        Accesses a task in the T Tree. The side-effect is shifting 
        this Talent Node to the left-most position at its depth.
        @param: task_name: Name of the task to access.
        @param: talent_name: Name of the talent to access.
        """
        talent_node = self._find_talent_node(talent_name, self.head)
        # note that we look up the task and update the time here
        # this means if this task is not found, it burns time for us
        current_time = self.capture_flowing_time()
        # if the talent node is not found, we can't access the task.
        # this means the talent node was added to lost_talents or was never added!
        if not talent_node:
            return
        
        task_found = talent_node.recall_task(talent_node.task_head, task_name, current_time)
        
        if task_found:
            # TODO: shift not working quite like we want it to
            # move this node to the left most position at this depth
            # left_most_uncle = self.__get_left_most_talent_node_at_rank(self.head, talent_node.parent.rank)
            # self.__shift_talent_nodes_right(talent_node, left_most_uncle)
            pass

    def capture_flowing_time(self, is_flowing = True) -> int:
        """
        Gets the current time of the T Tree then increments if time is expected to flow.
        @param: is_flowing: Boolean to determine if time should flow.
        @return: Current time.
        """
        current_time = self.time
        if is_flowing:
            self.__update_time() 
        return current_time
    

    def die(self) -> None:
        """
        Destroys T Tree.
        """
        pass
    
    # Private functions
    def __get_right_sibling(self, left_sibling_node: TalentNode) -> TalentNode:
        """
        Gets the right sibling of a Talent Node.
        @param: sibling_node: Node to start the search from.
        @return: Right sibling of the root node if found, None otherwise.
        """
        parent_node = left_sibling_node.parent
        
        # if there is no parent node, somehow we have lost our way
        if not parent_node:
            return None
        
        # if the left sibling is the left child of the parent,
        # then the right sibling is the right child of the parent
        if left_sibling_node == parent_node.left_child:
            return parent_node.right_child
        
        # otherwise, we need to find the grandparent node
        else:
            grandparent_node = parent_node.parent
            return grandparent_node.right_child.left_child
    

    def __shift_talent_nodes_right(self, new_node: TalentNode, root_node: TalentNode) -> None:
        """
        Shifts all Talent Nodes to the right starting from the left node.
        @param: new_node: The new node to this parent we will be adding as the left child
        @param: root_node: Root node to start the search from.
        """
        # the new node was already added to the root node's left when added to the tree
        if root_node.left_child == new_node:
            return

        # pick up the left child and set it to the sent_node
        sent_node = root_node.left_child
        # place the new_node in the left child's old spot
        root_node.left_child = new_node
        # pick up the right child and set it to the sent_node
        temp_node = root_node.right_child
        # place the sent_node in the right child's old spot
        root_node.right_child = sent_node
        # set the new_node as the left child of the sent_node
        sent_node = temp_node

        # now set the parents on the set nodes
        root_node.left_child.parent = root_node
        root_node.right_child.parent = root_node
    
        # if somewhere along the way we picked up a None node, 
        # we should stop shifting
        if not sent_node:
            return

        # find the parent's sibling...
        uncle_node = self.__get_right_sibling(root_node)
        
        if uncle_node:
            # ...and recurse
            return self.__shift_talent_nodes_right(sent_node, uncle_node)
        else:
            # we have reached the end of the tree
            # and must lose this talent
            self.lost_talents.append(sent_node)
            self.total_nodes -= 1
        
        return

    def __update_time(self) -> None:
        """
        Increments the time of the T Tree.
        """
        self.time += 1

    def __add_talent_node(self, talent_name: str, root_node: TalentNode) -> TalentNode:
        """
        Adds a new Talent Node to the T Tree.
        @param: talent_name: Name of the Talent Node to add.
        @param: root_node: Root node to start the search from.
        @return: Talent Node that was added.
        """
        # if this root node has no children, we can insert here
        if root_node.left_child == None:
            talent_node = TalentNode(name=talent_name)
            root_node.left_child = talent_node
            talent_node.parent = root_node
            return talent_node

        # if this root node has a child with the same starting rank, we can insert here
        if root_node.left_child.rank == 0:
            # first, create a new node
            talent_node = TalentNode(name=talent_name)
            talent_node.parent = root_node
            # then, add it to the left most position (most recently accessed) 
            # and shift all the other nodes to the right
            self.__shift_talent_nodes_right(talent_node, root_node)
            return talent_node
        
        
        # otherwise, we need to keep searching down the left side of the tree
        return self.__add_talent_node(talent_name, root_node.left_child)
        
    def __promote_talent_node(self, promoted_node) -> None:
        """
        Promotes a Talent Node up the T Tree.
        Be careful! If promoted too early, there's a risk of losing talents
        @param: promoted_node: Node to promote.
        """

        old_rank = promoted_node.rank - 1
        old_parent = promoted_node.parent
        old_left_child = promoted_node.left_child
        old_right_child = promoted_node.right_child
        

    def __get_left_most_talent_node_at_rank(self, talent_node: TalentNode, rank: int) -> TalentNode:
        """
        Gets the left most Talent Node at a given rank.
        @param: talent_node: Node to start the search from.
        @param: rank: Rank to search for.
        @return: Left most Talent Node at the given rank.
        """
        # search down the left side of the talent tree until we find the rank
        if talent_node.rank == rank:
            return talent_node
        
        # if there is a left child, search down the left side
        if talent_node.left_child:
            return self.__get_left_most_talent_node_at_rank(talent_node.left_child, rank)

    # Internal functions
    def _count_total_talents(self, root_node, count=0) -> int:
        """
        Counts the total number of talents in the T Tree.
        @param: count: Total number of talents.
        @return: Total number of talents.
        """
        # base case: if we are at a leaf node, return the count
        if not root_node:
            return 0
        
        # if it's the head node, do not count it
        if root_node is self.head:
            left_count = self._count_total_talents(root_node.left_child)
            right_count = self._count_total_talents(root_node.right_child)
            return left_count + right_count
        else:
            # otherwise, count this node and recurse down the tree
            left_count = self._count_total_talents(root_node.left_child)
            right_count = self._count_total_talents(root_node.right_child)
            return 1 + left_count + right_count

    def _find_talent_node(self, talent_name: str, root_node: TalentNode) -> TalentNode:
        """
        Finds a Talent Node in the T Tree.
        @param: talent_name: Name of the Talent Node to find.
        @param: root_node: Root node to start the search from.
        @return: Talent Node if found, None otherwise.
        """
        # Base case: if we are at a leaf node, return None
        if not root_node:
            return None
        
        # Search the tree in-order, favoring where we are and then the left side
        if root_node.name == talent_name:
            return root_node
        
        # Recursively search the left and right subtrees
        left_result = self._find_talent_node(talent_name, root_node.left_child)
        right_result = self._find_talent_node(talent_name, root_node.right_child)

        # Return the result of the search
        return left_result or right_result