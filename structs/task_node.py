class TaskNode:
    def __init__(self, task_name, creation_time):
        self.task_name = task_name  # Name or description of the task
        self.creation_time = creation_time  # Time when the task was created
        self.last_access_time = creation_time  # Last time the task was accessed, initially set to creation time
        self.left_child = None  # Pointer to the left child Task Node
        self.right_child = None  # Pointer to the right child Task Node

    def update_access_time(self, access_time):
        """
        Updates the last access time of the task.
        """
        self.last_access_time = access_time

    def add_child(self, is_burnout, child_node):
        """
        Adds a child node to this Task Node. This is a stubbed out for now.
        """
        # TODO: needs to think about adding this as head and having head go left and head's left go right if not burnout
        # probably need to think about this more to not make it so easy to fix a broken tree
        return

