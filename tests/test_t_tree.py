import unittest
from structs import TTree
from .helpers import TestHelpers

class TestTTree(unittest.TestCase):
    def test_add_single_talent(self):
        tree = TTree()
        tree.add_task("Some short task", "TalentA")
        self.assertIsNotNone(tree.head, "The root should not be None after adding a talent.")
        self.assertEqual(tree.head.left_child.name, "TalentA", "The root's name should match the added talent.")

    def test_add_two_talents(self):
        tree = TTree()
        tree.add_task("Some long task", "TalentB")
        tree.add_task("Some short task", "TalentA")

        self.assertEqual(tree.head.right_child.name, "TalentB", "The right child's name should be 'TalentB'.")
        self.assertEqual(tree.head.left_child.name, "TalentA", "The left child's name should be 'TalentA'.")
        self.assertEqual(tree._count_total_talents(tree.head), tree.total_nodes, "There should be 2 talents in the tree.")

    def test_add_three_talents_with_lost_node(self):
        """
        Test to see if the tree pushes nodes that can't fit into the lost talents list.
        """
        tree = TTree()
        tree.add_task("Some long task", "TalentB")
        tree.add_task("Some short task", "TalentA")
        tree.add_task("Some medium task", "TalentC")

        self.assertEqual(tree.head.right_child.name, "TalentA", "The right child's name should be 'TalentA'.")
        self.assertIsNotNone(tree.head.right_child, "There should be a right child.")
        self.assertEqual(tree.head.left_child.name, "TalentC", "The left child's name should be 'TalentC'.")
        self.assertIsNotNone(tree.head.left_child, "There should be a right child.")
        self.assertEqual(tree.lost_talents[0].name, "TalentB", "'TalentB' should have been moved to lost_talents.")
        self.assertEqual(tree._count_total_talents(tree.head), tree.total_nodes, "There should be 2 talents in the tree.")

    def test_time(self):
        tree = TTree()
        self.assertEqual(tree.time, 0, "The time should be 0 upon initialization.")
        tree.add_task("Some long task", "TalentA")
        self.assertEqual(tree.time, 1, "The time should be 1 after adding 1 task.")
        tree.add_task("Some short task", "TalentA")
        self.assertEqual(tree.time, 2, "The time should be 2 after adding 1 task.")
        tree.add_task("Some medium task", "TalentC")
        self.assertEqual(tree.time, 3, "The time should be 3 after adding 1 task.")
        tree.access_task("Some long task", "TalentA")
        self.assertEqual(tree.time, 4, "The time should be 4 after accessing an existing task.")
        tree.access_task("Some long task", "TalentA")
        self.assertEqual(tree.time, 5, "The time should be 5 after accessing a non-existing task.")

    def test_promote_talent_in_balanced_tree(self):
        tree = TTree()
        final_node = TestHelpers().build_robust_balanced_tree(tree)
        # add one more task to promote the talent
        tree.add_task("Promotional task", final_node)

if __name__ == '__main__':
    unittest.main()