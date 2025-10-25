from datetime import datetime, timedelta

class Task:
    def __init__(self, name, deadline, duration_minutes, priority, category):
        self.name = name
        self.deadline = deadline  # datetime object
        self.duration = timedelta(minutes=duration_minutes)
        self.priority = priority  # 'High', 'Medium', 'Low'
        self.category = category
        self.scheduled_start = None # datetime object
        self.scheduled_end = None # datetime object
        self.status = "Pending"

    def __repr__(self):
        return (f"{self.name} ({self.priority}) - {self.scheduled_start} "
                f"to {self.scheduled_end}")
    
    # priority_value(): Return numerical value for priority
    def priority_value(self):
        priority_map = {"High": 1, "Medium": 2, "Low": 3}
        return priority_map.get(self.priority)
    
    # get_latest_start(): Calculate latest start time to meet deadline
    def get_latest_start(self):
        return self.deadline - self.duration
    
    # extend_duration(extra_minutes): 
    # Extend the task duration by extra_minutes
    # Update scheduled end time if already scheduled
    def extend_duration(self, extra_minutes):
        self.duration += timedelta(minutes=extra_minutes)
        if self.scheduled_start:
            self.scheduled_end = self.scheduled_start + self.duration
    
    # set_schedule_start(start_time) 
    # Set the scheduled start time and calculate end time
    # For tasks that have been scheduled
    def set_schedule_start(self, start_time):
        self.scheduled_start = start_time
        self.scheduled_end = start_time + self.duration
    
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


