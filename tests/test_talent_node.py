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
        self.assertIsNot(tree.head.left_child.recent_task_map, "The Talent Node should have an empty recent task map after converting tasks to nodes.")

    def test_is_burnout_set(self):
        tree = TTree()
        tasks = ["Some long task", "Some short task", "Some medium task", "Workbook", "Explaining it to someone else", "Trying it again"]
        for task in tasks:
            tree.add_task(task, "TalentA")
        node = tree._find_talent_node("TalentA", tree.head)
        self.assertIs(node.task_head.is_burnt, True, "The most recent talent node should be burnt out by adding too many tasks without a break to a single talent.")

if __name__ == '__main__':
    unittest.main()