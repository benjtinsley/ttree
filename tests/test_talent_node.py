import unittest
from structs import TTree
from .helpers import TestHelpers

class TestTalentNode(unittest.TestCase):
    def test_check_talent_node_exists(self):
        tree = TTree()
        tasks = ["Some long task", "Some short task", "Some medium task", "Workbook", "Explaining it to someone else", "Trying it again"]
        for task in tasks:
            tree.add_task(task, "TalentA")
        tree.access_task("Some long task", "TalentA")
        self.assertIsNot(tree.head.left_child.task_head, None, "The Talent Node should not point to an empty task head after converting tasks to nodes.")
        self.assertIsNot(tree.head.left_child.recent_task_map, "The Talent Node should have an empty recent task map after converting tasks to nodes.")

    def test_is_burnout_toggleable(self):
        tree = TTree()
        tasks = ["Some long task", "Some short task", "Some medium task", "Workbook", "Explaining it to someone else", "Trying it again"]
        for task in tasks:
            tree.add_task(task, "TalentA")
        node = tree._find_talent_node("TalentA", tree.head)
        task_node = node._find_task_node(tasks[0], node.task_head)
        self.assertIs(task_node.is_burnt, True, "The found talent node should be burnt out by adding too many tasks without a break to a single talent.")

        other_tasks = ["Some other long task", "Some other short task", "Some other medium task", "Other Workbook", "Explaining it to some other one else", "Trying it other again", "Thinking about it", "Taking a break", "Going for a walk"]
        talents = ["TalentA", "TalentB", "TalentA", "TalentB", "TalentA", "TalentB",  "TalentA", "TalentB", "TalentA"]
        for task in other_tasks:
            talent = talents.pop()
            tree.add_task(task, talent)
        node = tree._find_talent_node("TalentA", tree.head)
        other_task_node = node._find_task_node(other_tasks[0], node.task_head)
        self.assertIs(other_task_node.is_burnt, False, "The found talent node should no longer be burnt out when spacing out the tasks added.")    

    def test_relearn(self):
        tree = TTree()
        talents = ["TalentA", "TalentB", "TalentB", "TalentB", "TalentB", "TalentB",  "TalentA"]
        for i in range(7):
            talent = talents.pop()
            TestHelpers().add_single_task(tree, talent)
        node = tree._find_talent_node("TalentA", tree.head)
        self.assertEqual(node.recent_task_map, {}, "The Talent Node should have an empty recent task map waiting too long between tasks (most recent add time - last add time is >= 2 x the amount of talent nodes).")

if __name__ == '__main__':
    unittest.main()