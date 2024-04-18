import math
from structs.talent_node import TalentNode

class TTree:
    def __init__(self):
        # Track total actions or time across the entire T Tree
        self.time = 0  
        self.lost_talents = []
        # The head node is an infinite rank Talent Node that is unreachable and unknown
        # TODO: should this be a different kind of node that can scale?
        self.head = TalentNode(name=None, rank=math.inf) 
    
    # Public functions
    def add_task(self, task_name, talent_name):
        talent_node = self._find_talent_node(talent_name, self.head)
        if not talent_node:
            talent_node = self._add_talent_node(talent_name, self.head)
        talent_node.store_task(task_name, self.time)
        self._update_time()

    def access_task(self, task_name, talent_name=None):
        if not talent_name:
            # we will have to search the entire t tree for this task, if it exists
            pass
        talent_node = self._find_talent_node(talent_name, self.head)
        talent_node.recall_task(task_name, self.time)
        # TODO: move this node to the left most position at this depth
        self._update_time()

    def die(self) -> None:
        """
        Destroys T Tree.
        """
        pass
    
        
    # Private functions
    def _get_right_sibling(self, left_sibling_node: TalentNode) -> TalentNode:
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
    

    def _shift_talent_nodes_right(self, new_node: TalentNode, root_node: TalentNode) -> None:
        """
        Shifts all Talent Nodes to the right starting from the left node.
        @param: new_node: The new node to this parent we will be adding as the left child
        @param: root_node: Root node to start the search from.
        """
        # the root node has no children
        if not root_node.left_child:
            root_node.left_child = new_node
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
    
        # if somewhere along the way we picked up a None node, 
        # we should stop shifting
        if not sent_node:
            return

        # find the parent's sibling...
        uncle_node = self._get_right_sibling(root_node)
        
        if uncle_node:
            # ...and recurse
            return self._shift_talent_nodes_right(sent_node, uncle_node)
        else:
            # we have reached the end of the tree
            # and must lose this talent
            self.lost_talents.append(sent_node)
        
        return


    def _update_time(self) -> None:
        self.time += 1

    def _add_talent_node(self, talent_name: str, root_node: TalentNode) -> TalentNode:
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
            return talent_node

        # if this root node has a child with the same starting rank, we can insert here
        if root_node.left_child.rank == 0:
            # first, create a new node
            talent_node = TalentNode(name=talent_name)
            talent_node.parent = root_node
            # then, add it to the left most position (most recently accessed) 
            # and shift all the other nodes to the right
            self._shift_talent_nodes_right(talent_node, root_node)
            return talent_node
        
        
        # otherwise, we need to keep searching down the left side of the tree
        return self._add_talent_node(talent_name, root_node.left_child)
        
    
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
    
    def _promote_talent_node(self) -> None:
        """
        Promotes a Talent Node up the T Tree.
        Be careful! If promoted too early, there's a risk of losing subtalents
        """
        pass