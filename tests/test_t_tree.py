import unittest
from structs import TTree
from .helpers import TestHelpers

class TestTTree(unittest.TestCase):
    def test_add_single_talent(self):
        tree = TTree()
        tree.add_task("Some short task", "TalentA")
        self.assertIsNotNone(tree.head, "The root should not be None after adding a talent.")
        self.assertEqual(tree.head.child_left.name, "TalentA", "The root's name should match the added talent.")

    def test_add_two_talents(self):
        tree = TTree()
        tree.add_task("Some long task", "TalentB")
        tree.add_task("Some short task", "TalentA")

        self.assertEqual(tree.head.child_right.name, "TalentB", "The right child's name should be 'TalentB'.")
        self.assertEqual(tree.head.child_left.name, "TalentA", "The left child's name should be 'TalentA'.")
        self.assertEqual(tree._count_total_talents(tree.head), tree.total_nodes, "There should be 2 talents in the tree.")

    def test_add_three_talents_with_lost_node(self):
        """
        Test to see if the tree pushes nodes that can't fit into the lost talents list.
        """
        tree = TTree()
        tree.add_task("Some long task", "TalentB")
        tree.add_task("Some short task", "TalentA")
        tree.add_task("Some medium task", "TalentC")

        self.assertEqual(tree.head.child_right.name, "TalentA", "The right child's name should be 'TalentA'.")
        self.assertIsNotNone(tree.head.child_right, "There should be a right child.")
        self.assertEqual(tree.head.child_left.name, "TalentC", "The left child's name should be 'TalentC'.")
        self.assertIsNotNone(tree.head.child_left, "There should be a right child.")
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
        final_node_name = TestHelpers().build_robust_balanced_tree(tree)
        self.assertListEqual(tree.lost_talents, [], "There should be no lost talents.")
        self.assertEqual(tree._count_total_talents(tree.head), 7, "There should be 7 starting talents in the tree.")
        # add one more task to promote the talent
        tree.add_task("Promotional task", final_node_name)
        
        list_at_rank_2 = tree._get_talent_node_list_at_rank(2)
        list_at_rank_1 = tree._get_talent_node_list_at_rank(1)
        list_at_rank_0 = tree._get_talent_node_list_at_rank(0)

        self.assertEqual(len(tree.lost_talents), 1, "The promotion should have pushed 1 talent to lost_talents.")
        self.assertEqual(tree._find_talent_node(final_node_name, tree.head).rank, 1, "The final node should have been promoted to rank 1.")
        self.assertEqual(list_at_rank_1[0].name, final_node_name, "The first talent at rank 1 should be the promoted node.")
        self.assertEqual(len(list_at_rank_2), 1, "There should be 1 talent at rank 2.")
        self.assertEqual(len(list_at_rank_1), 2, "There should be 2 talents at rank 1.")
        self.assertEqual(len(list_at_rank_0), 3, "There should be 3 talents at rank 0.")
        self.assertEqual(tree._count_total_talents(tree.head), tree.total_nodes, "There should be 4 remaining talents in the tree.")

if __name__ == '__main__':
    unittest.main()