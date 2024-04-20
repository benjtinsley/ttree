class TaskNode:
    def __init__(self, task_name, creation_time, is_burnt):
        self.left_child = None  # Pointer to the left child Task Node
        self.right_child = None  # Pointer to the right child Task Node
        self.parent = None  # Pointer to the parent Task Node
        self.task_name = task_name  # Name or description of the task
        self.creation_time = creation_time  # Time when the task was created
        self.last_access_time = creation_time  # Last time the task was accessed, initially set to creation time
        self.is_burnt = is_burnt  # Flag indicating if the Task Node is burnt out
