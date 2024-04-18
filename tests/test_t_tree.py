import unittest
from structs import TTree

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
        self.assertIsNotNone(tree.head.right_child, "There should be a right child.")
        self.assertEqual(tree.head.left_child.name, "TalentA", "The left child's name should be 'TalentA'.")
        self.assertIsNotNone(tree.head.left_child, "There should be a right child.")

    def test_add_three_talents(self):
        tree = TTree()
        tree.add_task("Some long task", "TalentB")
        tree.add_task("Some short task", "TalentA")
        tree.add_task("Some medium task", "TalentC")

        self.assertEqual(tree.head.right_child.name, "TalentA", "The right child's name should be 'TalentA'.")
        self.assertIsNotNone(tree.head.right_child, "There should be a right child.")
        self.assertEqual(tree.head.left_child.name, "TalentC", "The left child's name should be 'TalentC'.")
        self.assertIsNotNone(tree.head.left_child, "There should be a right child.")
        self.assertEqual(tree.lost_talents[0].name, "TalentB", "'TalentB' should have been moved to lost_talents.")

if __name__ == '__main__':
    unittest.main()