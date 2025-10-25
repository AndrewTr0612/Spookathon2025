from datetime import datetime, timedelta
import Task

# Each node in the BST 
# represents a task and its position in the tree
class BSTNode:
    def __init__(self, task):
        self.task = task
        self.left = None
        self.right = None

class Schedule:
    def __init__(self):
        self.root = None
    
    def insert_task(self, task):
        self.root = self._insert_recursive(self.root, task)
    
    def _insert_recursive(self, node, task):
        if node is None:
            return BSTNode(task)
        if (task.priority_value(), task.deadline) < (node.task.priority_value(), node.task.deadline):
            node.left = self._insert_recursive(node.left, task)
        else:
            node.right = self._insert_recursive(node.right, task)
        return node
    
    def print_schedule(self):
        """Print the schedule using in-order traversal"""
        self._print_inorder(self.root)
    
    def _print_inorder(self, node):
        """Helper method for in-order traversal"""
        if node:
            self._print_inorder(node.left)
            print(f"Task: {node.task}")
            self._print_inorder(node.right)

    def generate_schedule(self):
        ...

# Example 
task1 = BSTNode(Task.Task("Finish project report", datetime(2025,10,27,18,0), 180, "High", "School"))
task2 = BSTNode(Task.Task("Study for exam", datetime(2025,10,26,21,0), 120, "High", "School"))

schedule = Schedule()
schedule.insert_task(task1.task)
schedule.insert_task(task2.task)

schedule.print_schedule()
# # Helper to assign priority values for sorting
# priority_map = {"High": 1, "Medium": 2, "Low": 3}

# def schedule_tasks(tasks, work_day_start=datetime(2025,10,25,8,0), work_day_end=datetime(2025,10,25,22,0)):
#     """
#     Schedule tasks to finish by deadlines, creating multiple-day schedules if needed.
#     """
#     # Sort tasks: High priority first, then earlier deadlines
#     tasks_sorted = sorted(tasks, key=lambda t: (priority_map[t.priority], t.deadline))
    
#     scheduled_tasks = []

#     # Keep track of the next available time slot (we start from the last day)
#     # We'll schedule backward from each task's deadline
#     for task in tasks_sorted:
#         end_time = min(task.deadline, work_day_end)
#         start_time = end_time - task.duration
        
#         # Adjust start time if it goes before the work day start
#         current_day_start = work_day_start
#         while start_time < current_day_start:
#             # Task doesn't fit in current day, move to previous day
#             end_time = current_day_start
#             start_time = end_time - task.duration
#             current_day_start -= timedelta(days=1)
        
#         # Resolve conflicts with already scheduled tasks
#         for scheduled in scheduled_tasks:
#             # If overlapping, push the task earlier
#             while not (start_time >= scheduled.scheduled_end or end_time <= scheduled.scheduled_start):
#                 end_time = scheduled.scheduled_start
#                 start_time = end_time - task.duration
        
#         task.scheduled_start = start_time
#         task.scheduled_end = end_time
#         scheduled_tasks.append(task)
    
#     # Sort final schedule by start time
#     scheduled_tasks.sort(key=lambda t: t.scheduled_start)
#     return scheduled_tasks

# Example usage
# tasks = [
#     Task.Task("Finish project report", datetime(2025,10,27,18,0), 180, "High", "School"),
#     Task.Task("Study for exam", datetime(2025,10,26,21,0), 120, "High", "School"),
#     Task.Task("Workout", datetime(2025,10,25,20,0), 60, "Medium", "Health"),
#     Task.Task("Watch K-drama", datetime(2025,10,26,23,0), 90, "Low", "Entertainment"),
# ]

# schedule = schedule_tasks(tasks)
# for t in schedule:
#     print(t)

# print("\nAfter extending duration of first task:\n")
# # Extend duration example
# tasks[0].duration_extend(30)  # Extend first task by 30 minutes
# schedule = schedule_tasks(tasks)
# for t in schedule:
#     print(t)