class TalentNode:
    def __init__(self, name, burnout_limit = 2, max_tasks = 5, rank = 0):
        self.name = name
        self.parent = None
        self.left_child = None
        self.right_child = None
        self.recent_task_map = {}
        self.is_burnout = False
        self.is_mastered = False # TODO: needed?
        self.task_head = None
        self.last_access = 0
        self.rank = rank
        self.burnout_limit = burnout_limit # Start with a low burnout limit, but will grow
        self.max_tasks = max_tasks # Start with a low max tasks limit, but will grow

    def store_task(self, task_name, current_time):
        self.recent_task_map[current_time] = task_name
        self.last_access = current_time
        # TODO: need to check for relearn, ie it's been too long since current_time and last current_time
        # TODO: check to check for burnout, ie too frequent between tasks in list
        if len(self.recent_task_map) >=  self.max_tasks:
            self.convert_tasks_to_nodes()

        # TODO: update access rank & move up the tree if needed (will this require a left and right root?)
        # TODO: move to left most node at depth and shift the rest down

    def _convert_tasks_to_nodes(self):
        print(f"Converting tasks to Task Nodes for Talent Node '{self.name}'.")
        # TODO: take the full map or a portion of it, convert them to nodes if 
        # with is_burnout

            
        self.recent_task_map.clear()