import unittest
from structs import TTree

class TestTalentNode(unittest.TestCase):
    def test_check_talent_node_exists(self):
        tree = TTree()
        tasks = ["Some long task", "Some short task", "Some medium task", "Workbook", "Explaining it to someone else", "Trying it again"]
        for task in tasks:
            tree.add_task(task, "TalentA")
        tree.access_task("Some long task", "TalentA")
        self.assertIsNot(tree.head.left_child.task_head, None, "The Talent Node should not point to an empty task head after converting tasks to nodes.")
        print(tree.head.left_child.recent_task_map)
        self.assertIsNot(tree.head.left_child.recent_task_map, "The Talent Node should have an empty recent task map after converting tasks to nodes.")

if __name__ == '__main__':
    unittest.main()