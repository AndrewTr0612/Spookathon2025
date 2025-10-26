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

def get_latest_deadline(node):
        if not node:
            return datetime.min
        
        latest = node.task.deadline
        left_latest = get_latest_deadline(node.left)
        right_latest = get_latest_deadline(node.right)
        
        return max(latest, left_latest, right_latest)

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
    
    def add_fixed_event(self, event):
        """Add a fixed event to the schedule"""
        self.fixed_schedule.add_event(event)
    
    def is_time_slot_available(self, start_time, end_time):
        """Check if a time slot conflicts with any fixed events"""
        date = start_time.date()
        events = self.fixed_schedule.get_events_for_date(date)

        for event in events:
            event_start, event_end = event.get_datetime_for_date(date)
            # Check for overlap
            if not (end_time <= event_start or start_time >= event_end):
                return False
        return True
    
    def find_next_available_slot(self, start_time, duration, work_day_end):
        """Find the next available time slot after start_time"""
        current_time = start_time
        while current_time + duration <= work_day_end:
            end_time = current_time + duration
            if self.is_time_slot_available(current_time, end_time):
                return current_time
            
            # Get events for current day
            events = self.fixed_schedule.get_events_for_date(current_time.date())
            next_time = None
            
            # Find next available start time after current fixed events
            for event in events:
                event_start, event_end = event.get_datetime_for_date(current_time.date())
                if event_end > current_time:
                    next_time = event_end
                    break
            
            if not next_time:
                # No more events today, try next day at start time
                next_day = current_time.date() + timedelta(days=1)
                current_time = datetime.combine(next_day, datetime.min.time().replace(hour=8))
            else:
                current_time = next_time
        
        return None

    def generate_schedule(self, preferred_start=None, preferred_end=None):
        """Generate schedule considering fixed events"""
        latest_deadline = get_latest_deadline(self.root)
        
        # Set work period
        work_day_start = (preferred_start if preferred_start 
                         else datetime.now().replace(hour=8, minute=0, second=0, microsecond=0))
        work_day_end = (preferred_end if preferred_end and preferred_end <= latest_deadline 
                       else latest_deadline)
        
        if work_day_start >= work_day_end:
            raise ValueError("Start time must be before end time")
        
        scheduled_tasks = []
        self._schedule_inorder(self.root, scheduled_tasks, work_day_start, work_day_end)
        return scheduled_tasks
    
    def _schedule_inorder(self, node, scheduled_tasks, work_day_start, work_day_end):
        """Schedule tasks in-order, avoiding fixed events"""
        if node:
            self._schedule_inorder(node.left, scheduled_tasks, work_day_start, work_day_end)
            
            task = node.task
            
            if task.deadline < work_day_start:
                print(f"Warning: Task '{task.name}' deadline ({task.deadline}) is before work period start")
                return
            
            # Find suitable time slot
            if not scheduled_tasks:
                # First task - try to schedule as late as possible before deadline
                end_time = min(task.deadline, work_day_end)
                start_time = end_time - task.duration
                
                # Find available slot that doesn't conflict with fixed events
                while not self.is_time_slot_available(start_time, end_time):
                    end_time = start_time
                    start_time = end_time - task.duration
                    if start_time < work_day_start:
                        print(f"Warning: Cannot find suitable time slot for '{task.name}'")
                        return
            else:
                # Schedule before the last task
                last_task = scheduled_tasks[-1]
                end_time = last_task.scheduled_start
                start_time = self.find_next_available_slot(work_day_start, task.duration, end_time)
                
                if not start_time:
                    print(f"Warning: Cannot find suitable time slot for '{task.name}'")
                    return
            
            task.set_schedule_start(start_time)
            scheduled_tasks.append(task)

            self._schedule_inorder(node.right, scheduled_tasks, work_day_start, work_day_end)
    # def print_schedule(self):
    #     """Print the schedule using in-order traversal"""
    #     self._print_inorder(self.root)
    
    # def _print_inorder(self, node):
    #     """Helper method for in-order traversal"""
    #     if node:
    #         self._print_inorder(node.left)
    #         print(f"Task: {node.task}")
    #         self._print_inorder(node.right)


