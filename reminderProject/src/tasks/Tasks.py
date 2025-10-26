from datetime import datetime, timedelta

class Task:
    def __init__(self, name, deadline, priority):
        self.name = name
        self.deadline = deadline  # datetime object
        self.priority = priority  # 'High', 'Medium', 'Low'
        self.status = "Pending"

    def __repr__(self):
        return (f"{self.name} Priority: {self.priority}"
                f"Deadline: {self.deadline} Status: {self.status}")
    
    # priority_value(): Return numerical value for priority
    def priority_value(self):
        priority_map = {"High": 1, "Medium": 2, "Low": 3}
        return priority_map.get(self.priority)
     
    # mark_complete(): Mark the task as completed
    def mark_complete(self):
        self.status = "Completed"
    
    # mark_cancelled(): Mark the task as cancelled
    def mark_cancelled(self):
        self.status = "Cancelled"

    # is_overdue(current_time=None): 
    # Check if the task is overdue
    def is_overdue(self, current_time=None):
        if current_time is None:
            current_time = datetime.now()
        return current_time > self.deadline and self.status == "Pending"


