class TalentNode:
    def __init__(self, name, burnout_limit, max_tasks):
        self.name = name
        self.left_child = None
        self.right_child = None
        self.recent_task_map = {}
        self.is_burnout = False
        self.is_mastered = False # TODO: needed?
        self.task_head = None
        self.total_accesses = 0
        self.access_rank = 0

    def add_task(self, task_name, current_time):

        self.recent_task_map[current_time] = task_name
        # TODO: need to check for relearn, ie it's been too long since current_time and last current_time
        # TODO: check to check for burnout, ie too frequent between tasks in list
        if len(self.recent_task_map) > self.max_tasks:
            self.convert_tasks_to_nodes()


    def convert_tasks_to_nodes(self):
        print(f"Converting tasks to Task Nodes for Talent Node '{self.name}'.")
        # TODO: take the full map or a portion of it, convert them to nodes if 
        # with is_burnout

            
        self.recent_task_map.clear()