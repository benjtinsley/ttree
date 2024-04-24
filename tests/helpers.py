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
        self.__promote_talent_node(tree, 'Talent1', 2)
        self.__promote_talent_node(tree, 'Talent3', 1)
        self.__promote_talent_node(tree, 'Talent2', 1)
        # Add these with a single task to add them at rank 0
        self.__add_single_task(tree, 'Talent7')
        self.__add_single_task(tree, 'Talent6')
        self.__add_single_task(tree, 'Talent5')
        # max out the last talent in preparation for a promotion
        self.__add_single_task(tree, 'Talent4')
        self.__add_single_task(tree, 'Talent4')
        self.__add_single_task(tree, 'Talent4')
        self.__add_single_task(tree, 'Talent4')
        return 'Talent4'

    def __promote_talent_node(self, tree: TTree, talent_node: TalentNode, rank_delta: int) -> None:
        """
        Generates a random task to feed into the given task.
        Note, this function does not consider burnout.
        @param tree: the tree to add the task to
        @param talent_name: name of the talent to add the task to
        @param rank_delta: the total ranks to add to the talent
        """
        ending_rank = talent_node.rank + rank_delta

        while ending_rank != talent_node.rank:
            self.__add_single_task(tree, talent_node.name)

        return 

    def __add_single_task(self, tree: TTree, talent_name: str) -> None:
        """
        Generates a random task to feed into the given talent.
        @param tree: the tree to add the task to
        @param talent_name: name of the talent to add the task to
        """
        nums = [i for i in range(100)]
        letters = list(string.ascii_uppercase)
        symbols = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+", "-", "=", "{", "}", "[", "]", "|", ":", ";", "'", '"', "<", ">", ",", ".", "?", "/", " "]
        # Create a random string
        num = random.choice(nums)
        letter = random.choice(letters)
        symbol = random.choice(symbols)
        task = f"{num}{letter}{symbol}"
        # Add the task to the talent
        tree.add_task(task, talent_name)