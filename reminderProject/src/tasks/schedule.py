from datetime import datetime, timedelta
import Tasks
from fixed_schedule import FixedEvent, FixedSchedule

# Each node in the BST 
# represents a task and its position in the tree
class BSTNode:
    def __init__(self, task):
        self.task = task
        self.left = None
        self.right = None

# def get_latest_deadline(node):
#         if not node:
#             return datetime.min
        
#         latest = node.task.deadline
#         left_latest = get_latest_deadline(node.left)
#         right_latest = get_latest_deadline(node.right)
        
#         return max(latest, left_latest, right_latest)

class Schedule:
    def __init__(self):
        self.root = None
        self.fixed_schedule = FixedSchedule()
    
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
    
    def reschedule_after_extension(self, task_name):
        """Reschedule tasks after a task's duration has been extended"""
        # For simplicity, we will just re-generate the schedule
        # In a real implementation, we would need to find the task,
        # extend its duration, and then adjust subsequent tasks
        pass
    


