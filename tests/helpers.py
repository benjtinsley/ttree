import string
import random
from sys import getsizeof
from structs import TTree, TalentNode, TaskNode

class TestHelpers:
    def build_robust_balanced_tree(self, tree) -> str:
        """
        Builds a tree with 7 countable, each non-infinite, non-leaf node with 2 children.
        The ranks are as follows:
             ∞
              /
             2
            /  \\
           1   1
         / \    / \\
        0    0 0    0
        Promoting rank 1 or 0 will push the talent to an existing rank.
        @param tree: the tree to add the talents to
        @return the name of the last talent node added
        """
        self.promote_talent_node(tree, 'Talent1', 2)
        self.promote_talent_node(tree, 'Talent3', 1)
        self.promote_talent_node(tree, 'Talent2', 1)
        # Add these with a single task to add them at rank 0
        self.add_single_task(tree, 'Talent7')
        self.add_single_task(tree, 'Talent6')
        self.add_single_task(tree, 'Talent5')
        # max out the last talent in preparation for a promotion
        self.add_single_task(tree, 'Talent4')
        self.add_single_task(tree, 'Talent4')
        self.add_single_task(tree, 'Talent4')
        self.add_single_task(tree, 'Talent4')
        return 'Talent4'
    
    def build_gapped_balanced_tree(self, tree) -> str:
        """
        Builds a tree with 7 countable talents, each non-infinite, non-leaf node with 2 children.
        The ranks are as follows:
             ∞
              /
             4
            /  \\
           2   2
         / \    / \\
        0    0 0    0
        Promoting any node will create a new rank in the tree.
        @param tree: the tree to add the talents to
        @return the name of the last talent node added
        """
        self.promote_talent_node(tree, 'Talent1', 4)
        self.promote_talent_node(tree, 'Talent3', 2)
        self.promote_talent_node(tree, 'Talent2', 2)
        # Add these with a single task to add them at rank 0
        self.add_single_task(tree, 'Talent7')
        self.add_single_task(tree, 'Talent6')
        self.add_single_task(tree, 'Talent5')
        self.add_single_task(tree, 'Talent4')
        return 'Talent2'

    def promote_talent_node(self, tree: TTree, talent_name: str, rank_delta: int) -> None:
        """
        Generates a random task to feed into the given task.
        Note, this function does not consider burnout.
        @param tree: the tree to add the task to
        @param talent_name: name of the talent to add the task to
        @param rank_delta: the total ranks to add to the talent
        """
        self.add_single_task(tree, talent_name)
        talent_node = tree._find_talent_node(talent_name, tree.head)
        ending_rank = talent_node.rank + rank_delta

        while ending_rank != talent_node.rank:
            self.add_single_task(tree, talent_node.name)
        return 

    def add_single_task(self, tree: TTree, talent_name: str) -> TalentNode:
        """
        Generates a random task to feed into the given talent.
        @param tree: the tree to add the task to
        @param talent_name: name of the talent to add the task to
        """
        nums = [i for i in range(9)]
        letters = list(string.ascii_uppercase)
        symbols = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+", "-", "=", "{", "}", "[", "]", "|", ":", ";", "<", ">", ",", ".", "?", "/", " "]
        # Create a random string
        num1 = random.choice(nums)
        num2 = random.choice(nums)
        letter = random.choice(letters)
        symbol = random.choice(symbols)
        task = f"{num1}{num2}{symbol}{letter}"
        # Add the task to the talent
        tree.add_task(task, talent_name)
    
    def get_tree_memory_size(self, node: TalentNode, size: int=0) -> int:
        """
        Recursively gets the memory size of the tree.
        @param node: the node to get the memory size of
        @param size: the total size of the tree
        @return the memory size of the tree
        """

        if node is None:
            return
        
        size += getsizeof(node)

        if node.child_left:
            if node.child_left.task_head:
                size += self._get_node_memory_size(node.child_left.task_head)
            self.get_tree_memory_size(node.child_left, size)

        if node.child_right:
            if node.child_right.task_head:
                size += self._get_node_memory_size(node.child_right.task_head)
            self.get_tree_memory_size(node.child_right, size)

        return size

    
    # Internal
    def _get_node_memory_size(self, task: TaskNode, size: int=0) -> int:
        """
        Recursively gets the memory size of the node.
        @param node: the node to get the memory size of
        @param size: the total size of the node
        @return the memory size of the node
        """
        if not task:
            return
        
        size += getsizeof(task)

        if task.child_left:
            size += self._get_node_memory_size(task.child_left)
        if task.child_right:
            size += self._get_node_memory_size(task.child_right)

        return size