import string
import random
from structs import TTree, TalentNode

class TestHelpers:
    def build_robust_balanced_tree(self, tree) -> str:
        """
        Builds a tree with 7 talents, each non-leaf node with 2 children.
        The ranks are as follows:
             2
            /  \\
           1   1
         / \    / \\
        0    0 0    0
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