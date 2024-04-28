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
            # create an unattached talent node
            talent_node = TalentNode(talent_name)
            # and increment the total number of nodes
            self.total_nodes += 1

        # grab the starting rank of the talent node for comparison later
        starting_rank = talent_node.rank
        current_time = self.capture_flowing_time()
        talent_node.store_task(talent_node, task_name, current_time, self.total_nodes)
        parent_rank = talent_node.parent.rank if talent_node.parent else None

        # add this node to the left most position at this depth
        left_most_uncle = self.__get_left_most_talent_node_at_rank(self.head, parent_rank)
        self.__shift_talent_nodes_right(talent_node, left_most_uncle)

        # the talent node's rank may have been updated, in store_task
        # if so, a promotion is in order
        if talent_node.rank > starting_rank:
            self.__promote_talent_node(talent_node)

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
            left_most_uncle = self.__get_left_most_talent_node_at_rank(self.head, talent_node.parent.rank)
            self.__shift_talent_nodes_right(talent_node, left_most_uncle)
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
        if left_sibling_node == parent_node.child_left:
            return parent_node.child_right
        
        # otherwise, we need to find the grandparent node
        else:
            grandparent_node = parent_node.parent
            # multiple checks to ensure we aren't reaching too far
            if not grandparent_node:
                return None
            if not grandparent_node.child_right:
                return None
            if not grandparent_node.child_right.child_left:
                return None
            return grandparent_node.child_right.child_left
    
    def __get_talent_node_list_at_rank(self, rank: int,  root: TalentNode=None, node_list: list=None) -> list:
        """
        Gets all Talent Nodes at a given rank using an in order recursive search.
        @param: rank: Rank to search for.
        @return: List of Talent Nodes at the given rank from left to right.
        """

        # TODO: Convert to DFS?

        # initialize the search from the head node
        if root is None:
            root = self.head
            node_list = []

        # if we are at the rank, add this node to the list
        if root.rank == rank:
            return node_list.append(root)
        
        # if there is a left child, search down the left side
        if root.child_left:
            self.__get_talent_node_list_at_rank(rank, root.child_left, node_list)
        
        # if there is a right child, search down the right side
        if root.child_right:
            self.__get_talent_node_list_at_rank(rank, root.child_right, node_list)

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
        old_parent = node.parent
        node.parent = None

        if old_parent:
            # if the node is still the left or right child of the parent, make it official
            if old_parent.child_left == node:
                old_parent.child_left = None
            if old_parent.child_right == node:
                old_parent.child_right = None

        # push the node to the lost talents
        self.lost_talents.append(node)
        # we lost a good one
        self.total_nodes -= 1

        # recurse
        self.__push_subtree_to_lost_talents(node.child_left)
        self.__push_subtree_to_lost_talents(node.child_right)

        return

    def __shift_talent_nodes_right(self, new_node: TalentNode, root_node: TalentNode) -> None:
        """
        Shifts all Talent Nodes to the right starting from the left node.
        @param: new_node: The new node to this parent we will be adding as the left child
        @param: root_node: Root node to start the search from.
        """
        # the new node is already the left child of the root node
        if root_node.child_left == new_node:
            return
        
        # if there is no left child, we can just add the new node and stop shifting
        if not root_node.child_left:
            root_node.child_left = new_node
            new_node.parent = root_node
            return

        # pick up the left child and set it to the sent_node
        sent_node = root_node.child_left
        # place the new_node in the left child's old spot
        root_node.child_left = new_node
        # pick up the right child and set it to the sent_node
        temp_node = root_node.child_right
        # place the sent_node in the right child's old spot
        root_node.child_right = sent_node
        # set the new_node as the left child of the sent_node
        sent_node = temp_node

        # now set the parents on the set nodes
        root_node.child_left.parent = root_node
        root_node.child_right.parent = root_node
    
        # if somewhere along the way we picked up a None node, 
        # we should stop shifting
        if not sent_node:
            return
        
        # if we just needed to swap the left and right nodes, we are done
        if sent_node == new_node:
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
    
    def __shift_talent_nodes_left(self, node_list: list, new_parent_node: TalentNode, list_rank: int, new_child_left: TalentNode=None, new_child_right: TalentNode=None, remaining_nodes: list=[]) -> list:
        """
        Recursively shifts a list of nodes to the left until
        there are no more parents to shift to, then it adds the remaining
        nodes to the lost_talents array along with their subtrees
        @param: node_list: List of nodes to shift left
        @param: new_parent_node: Parent node to shift to
        @param: list_rank: Assumed rank of all nodes in the list
        @param: new_child_left: Initial left node to work with
        @param: new_child_right: Initial right node to work with
        @param: remaining_nodes: List of nodes that stay at the current rank
        @return: List of remaining nodes that stay at the current rank
        """
        # if there are no more nodes to shift, return the remaining nodes
        if not node_list:
            return remaining_nodes
        
        node = node_list.pop(0)
        next_child_left = node.child_left
        next_child_right = node.child_right

        # there's no more parents to shift to, so the rest of the nodes
        # and all children need to be added to the lost_talents array
        if not new_parent_node:
            # this will empty the remaining nodes list
            # so the next iteration will return the remaining nodes
            for node in node_list:
                self.__push_subtree_to_lost_talents(node)
            self.__push_subtree_to_lost_talents(new_child_left)
            self.__push_subtree_to_lost_talents(new_child_right)
            next_parent = None
            next_child_right = None
            next_child_left = None

        # we add the promoted node to the old node list initially
        # so we can just use its children and go ahead and break
        # the bonds
        # we can tell its the promoted node because it's rank is different
        # than the rest of the list
        elif node.rank != list_rank:
            self.__dissolve_bonds(node, new_parent_node, True)
            if new_child_left:
                self.__dissolve_bonds(new_child_left, node, True)
            if new_child_right:
                self.__dissolve_bonds(new_child_right, node, False)
            next_parent = new_parent_node
        # otherwise we need to place the node somewhere as the parent's children
        else:
            # if it's already the right child of the parent, we need to move it to the left
            # conversely, if the parent doesn't have a left child, we can just add it there
            if new_parent_node.right_child == node or not new_parent_node.child_left:
                # first, make sure there's no other record of this node with the parent
                if new_parent_node.child_right == node:
                    self.__dissolve_bonds(node, new_parent_node, False)
                # then, add the node to the left child of the parent
                self.__add_all_bonds(node, new_parent_node, new_child_left, new_child_right, True)
                # we will keep the parent the same
                next_parent = new_parent_node
            else:
                self.__add_all_bonds(node, new_parent_node, new_child_left, new_child_right, True)
                # we will get the right sibling of the parent
                next_parent = self.__get_right_sibling(new_parent_node)
            # finally add this node to the remaining nodes list
            remaining_nodes.append(node)

        # recurse
        return self.__shift_talent_nodes_left(node_list, next_parent, next_child_left, next_child_right)


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
        if root_node.child_left == None:
            talent_node = TalentNode(name=talent_name)
            root_node.child_left = talent_node
            talent_node.parent = root_node
            return talent_node

        # if this root node has a child with the same starting rank, we can insert here
        if root_node.child_left.rank == 0:
            # first, create a new node
            talent_node = TalentNode(name=talent_name)
            talent_node.parent = root_node
            # then, add it to the left most position (most recently accessed) 
            # and shift all the other nodes to the right
            self.__shift_talent_nodes_right(talent_node, root_node)
            return talent_node
        
        
        # otherwise, we need to keep searching down the left side of the tree
        return self.__add_talent_node(talent_name, root_node.child_left)
        
    def __promote_talent_node(self, promoted_node: TalentNode) -> None:
        """
        Promotes a Talent Node up the T Tree.
        Be careful! If promoted too early, there's a risk of losing talents
        @param: promoted_node: Node to promote.
        """
        # first, we need to get some information about the promoted node and its surroundings
        old_rank = promoted_node.rank - 1
        old_parent = promoted_node.parent

        # we need to determine if we are creating a new rank in the tree
        new_sibling = old_parent if old_parent.rank == promoted_node.rank else None
        if new_sibling:
            new_parent = old_parent.parent
            is_promotion_rank_new = False
        else:
            new_parent = old_parent
            is_promotion_rank_new = True

        # grab a list of all the nodes at the old rank
        old_ranked_nodes = self.__get_talent_node_list_at_rank(old_rank)
        # add the promoted node to the first item in the list so we can steal its children
        old_ranked_nodes.insert(0, promoted_node)
        # shift all the other nodes to the left to officially get rid of the promoted node at this rank
        remaining_nodes = self.__shift_talent_nodes_left(old_ranked_nodes, old_parent, old_rank)

        # if we are creating a new rank in the tree, we will potentially
        # move nodes to the lost_talent array at these levels:  
        # - old rank
        # - old child rank
        # but not at
        # - new rank
        if is_promotion_rank_new:
            # only the first 2 nodes in the remaining nodes can stay in the tree
            if len(remaining_nodes) > 0:
                new_left_child = remaining_nodes.pop(0)
            else:
                new_left_child = None
            if len(remaining_nodes) > 0:
                new_right_child = remaining_nodes.pop(0)
            else:
                new_right_child = None

            self.__add_all_bonds(promoted_node, new_parent, new_left_child, new_right_child, True)

            # the rest of the nodes need to be pushed to the lost_talents array
            for node in remaining_nodes:
                self.__push_subtree_to_lost_talents(node)

            return
        
        # if the node is being inserted at a rank that already exists, we will potentially
        # move nodes to the lost_talent array at these levels:
        # - new rank
        # - old child rank
        # but not at
        # - old rank
        else:
            self.__shift_talent_nodes_right(promoted_node, new_parent)
            return

    def __get_left_most_talent_node_at_rank(self, talent_node: TalentNode, rank: int=None) -> TalentNode:
        """
        Gets the left most Talent Node at a given rank.
        @param: talent_node: Node to start the search from.
        @param: rank: Rank to search for.
        @return: Left most Talent Node at the given rank.
        """
        # search down the left side of the talent tree until we find the rank
        if talent_node.rank == rank:
            return talent_node
        
        # if there's no given node, we are inserting at leaf level, so find the next rank up from the leaf rank (0)
        if not rank:
            if (not talent_node.child_left or talent_node.child_left.rank == 0):
                return talent_node
        
        # if there is a left child, search down the left side
        if talent_node.child_left:
            return self.__get_left_most_talent_node_at_rank(talent_node.child_left, rank)
        
    def __add_bonds(self, node: TalentNode, parent: TalentNode, is_left: bool) -> None:
        """
        Adds bonds between a Talent Node and its parent.
        @param: node: Node to bond.
        @param: parent: Parent to bond to.
        @param: is_left: Boolean to determine if the node is the left child.
        """
        if not node:
            return 

        if is_left:
            parent.child_left = node
        else:
            parent.child_right = node
        node.parent = parent
        return
    
    def __add_all_bonds(self, node: TalentNode, parent: TalentNode, child_left: TalentNode, child_right: TalentNode, is_left: bool) -> None:
        """
        Adds bonds between a Talent Node and its parent and children.
        @param: node: Node to bond.
        @param: parent: Parent to bond to.
        @param: child_left: Left child to bond to.
        @param: child_right: Right child to bond to.
        @param: is_left: Boolean to determine if the node is the left child.
        """
        if is_left:
            self.__add_bonds(node, parent, True)
        else:
            self.__add_bonds(node, parent, False)
        self.__add_bonds(child_left, node, True)
        self.__add_bonds(child_right, node, False)
        return
    
    def __dissolve_bonds(self, node: TalentNode, parent: TalentNode, is_left: bool) -> None:
        """
        Dissolves bonds between a Talent Node and its parent.
        @param: node: Node to dissolve bonds with.
        @param: parent: Parent to dissolve bonds with.
        @param: is_left: Boolean to determine if the node is the left child.
        """
        if not node:
            return

        if is_left:
            parent.child_left = None
        else:
            parent.child_right = None
        node.parent = None
        return
    
    def __dissolve_all_bonds(self, node: TalentNode, parent: TalentNode, child_left: TalentNode, child_right: TalentNode, is_left: bool) -> None:
        """
        Dissolves bonds between a Talent Node and its parent and children.
        @param: node: Node to dissolve bonds with.
        @param: parent: Parent to dissolve bonds with.
        @param: child_left: Left child to dissolve bonds with.
        @param: child_right: Right child to dissolve bonds with.
        @param: is_left: Boolean to determine if the node is the left child.
        """
        if is_left:
            self.__dissolve_bonds(node, parent, True)
        else:
            self.__dissolve_bonds(node, parent, False)
        self.__dissolve_bonds(child_left, node, True)
        self.__dissolve_bonds(child_right, node, False)
        return

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
            left_count = self._count_total_talents(root_node.child_left)
            right_count = self._count_total_talents(root_node.child_right)
            return left_count + right_count
        else:
            # otherwise, count this node and recurse down the tree
            left_count = self._count_total_talents(root_node.child_left)
            right_count = self._count_total_talents(root_node.child_right)
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
        left_result = self._find_talent_node(talent_name, root_node.child_left)
        right_result = self._find_talent_node(talent_name, root_node.child_right)

        # Return the result of the search
        return left_result or right_result