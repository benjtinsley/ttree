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
    
    def __get_talent_node_list_at_rank(self, rank: int,  root: TalentNode=None, node_list: list=None) -> list:
        """
        Gets all Talent Nodes at a given rank using an in order recursive search.
        @param: rank: Rank to search for.
        @return: List of Talent Nodes at the given rank from left to right.
        """
        # initialize the search from the head node
        if root is None:
            root = self.head
            node_list = []

        # if we are at the rank, add this node to the list
        if root.rank == rank:
            return node_list.append(root)
        
        # if there is a left child, search down the left side
        if root.left_child:
            self.__get_talent_node_list_at_rank(rank, root.left_child, node_list)
        
        # if there is a right child, search down the right side
        if root.right_child:
            self.__get_talent_node_list_at_rank(rank, root.right_child, node_list)

        return node_list
    
    def __push_subtree_to_lost_talents(self, node: TalentNode) -> None:
        """
        Recursively pushes a subtree to the lost talents array.
        This is a sad function.
        @param: node: Node to start the push from.
        """
        # if there are no more nodes to push, return
        if node is None:
            return
        
        # dissolve the bonds that once held this node to the tree
        node.parent = None

        if node.parent.left_child == node:
            node.parent.left_child = None
        else:
            node.parent.right_child = None

        # push the node to the lost talents
        self.lost_talents.append(node)
        # we lost a good one
        self.total_nodes -= 1

        # recurse
        self.__push_subtree_to_lost_talents(node.left_child)
        self.__push_subtree_to_lost_talents(node.right_child)

        return

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
            # and must lose this talent and its children
            self.__push_subtree_to_lost_talents(sent_node)
        
        return
    
    def __shift_talent_nodes_left(self, node_list: list, new_parent_node: TalentNode, new_left_child: TalentNode, new_right_child: TalentNode) -> None:
        """
        Recursively shifts a list of nodes to the left until
        there are no more parents to shift to, then it adds the remaining
        nodes to the lost_talents array along with their subtrees
        @param: node_list: List of nodes to shift left
        @param: new_parent_node: Parent node to shift to
        @param: new_left_child: Initial left node to work with
        @param: new_right_child: Initial right node to work with
        """
        # if there are no more nodes to shift, return
        if not node_list:
            return
        
        node = node_list.pop(0)
        next_left_child = node.left_child
        next_right_child = node.right_child

        # there's no more parents to shift to, so the rest of the nodes
        # and all children need to be added to the lost_talents array
        if not new_parent_node:
            for node in node_list:
                self.__push_subtree_to_lost_talents(node)
            self.__push_subtree_to_lost_talents(new_left_child)
            self.__push_subtree_to_lost_talents(new_right_child)
        else:
            # check if the left child has already been placed
            if new_parent_node.left_child.rank == node.rank:
                new_parent_node.right_child = node
                next_parent = self.__get_right_sibling(new_parent_node)
            # otherwise just place it in the left child
            else:
                new_parent_node.left_child = node
                next_parent = new_parent_node

            node.parent = new_parent_node

        # recurse
        self.__shift_talent_nodes_left(node_list, next_parent, next_left_child, next_right_child)


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
        
    def __promote_talent_node(self, promoted_node: TalentNode) -> None:
        """
        Promotes a Talent Node up the T Tree.
        Be careful! If promoted too early, there's a risk of losing talents
        @param: promoted_node: Node to promote.
        """
        # first, we need to get some information about the promoted node and its surroundings
        old_rank = promoted_node.rank - 1
        old_parent = promoted_node.parent
        old_sibling = old_parent.right_child
        old_left_child = promoted_node.left_child
        old_right_child = promoted_node.right_child

        new_sibling = old_parent if old_parent.rank == promoted_node.rank else None
        if new_sibling:
            new_parent = old_parent.parent
            is_promotion_rank_new = False
        else:
            new_parent = None
            is_promotion_rank_new = True

        # if we are creating a new rank in the tree, we will potentially
        # move nodes to the lost_talent array at these levels:
        # - old rank
        # - old child rank
        # but not at
        # - new rank
        if is_promotion_rank_new:
            if old_sibling:
                # first we need to remove the promoted node from the old parent
                # and shift all the other nodes at that rank to the left
                old_ranked_nodes = self.__get_talent_node_list_at_rank(old_rank)
                # we need to push the old_sibling into the promoted_node's old spot and
                # inherit the promoted_nodes's old children
                self.__shift_talent_nodes_left(old_ranked_nodes, promoted_node, old_left_child, old_right_child)
        
        # if the node is being inserted at a rank that already exists, we will potentially
        # move nodes to the lost_talent array at these levels:
        # - new rank
        # - old child rank
        # but not at
        # - old rank
        else:
            # first we need to remove the promoted node from the old parent
            # and shift all the other nodes at that rank to the left
            old_ranked_nodes = self.__get_talent_node_list_at_rank(old_rank)
            # we need to push the old_sibling into the promoted_node's old spot and
            # inherit the promoted_nodes's old children
            self.__shift_talent_nodes_left(old_ranked_nodes, promoted_node, old_left_child, old_right_child)
            # now we can add the promoted node to the new parent and shift all the other nodes
            self.__shift_talent_nodes_right(promoted_node, new_parent)
            # TODO: fix the __shift_talent_nodes_right function to work as expected

        # Are we done here?
        return

        # if old parent rank is greater than promoted_node rank, we can leave
        # the parent connection intact
        # .. if the rank is the same, we need to get the parent's parent and connect 
        # the promoted node to that
        # then shift all the other nodes on the promoted nodes rank to the right using
        # __shift_talent_nodes_right to accommodate the new promoted node

        # now we need to worry about the old_sibling

        # if it had an old_sibling, we need to mark the sibling to be the new promoted node' 
        # left child and shift over any other nodes to the left

        # any nodes that can't fit in the new row, we need to send to lost talents

        # now we need to give the new left child the old left child and old right child
        # and shift all the other nodes at that rank to the right

        # things that are useful to know:
        # - the old_rank is 0: we don't need to determine what to do with children
        # - there is a old_right_child: we need to attempt a shift, otherwise we just deal with the old_left_child
        # - there is a old_sibling: we need to attempt a shift left at the old_rank level
        # - promoted_node.rank != old_parent.rank: we can just leave the parent level alone
        

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
    def _count_total_talents(self, root_node: TalentNode, count: int=0) -> int:
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