from datetime import datetime, timedelta

class Task:
    def __init__(self, name, deadline, duration_minutes, priority, category):
        self.name = name
        self.deadline = deadline  # datetime object
        self.duration = timedelta(minutes=duration_minutes)
        self.priority = priority  # 'High', 'Medium', 'Low'
        self.category = category
        self.scheduled_start = None
        self.scheduled_end = None
        self.status = "Pending"

    def __repr__(self):
        return (f"{self.name} ({self.priority}) - {self.scheduled_start} "
                f"to {self.scheduled_end}")
    
    # duration_extend(extra_minutes): Extend the task duration by extra_minutes
    def duration_extend(self, extra_minutes):
        self.duration += timedelta(minutes=extra_minutes)
    
    # set_schedule_start(start_time): Set the scheduled start time and calculate end time
    def set_schedule_start(self, start_time):
        self.scheduled_start = start_time
        self.scheduled_end = start_time + self.duration
    
    # mark_complete(): Mark the task as completed
    def mark_complete(self):
        self.status = "Completed"
    
    # mark_cancelled(): Mark the task as cancelled
    def mark_cancelled(self):
        self.status = "Cancelled"
    
    

# Helper to assign priority values for sorting
priority_map = {"High": 1, "Medium": 2, "Low": 3}

def schedule_tasks(tasks, work_day_start=datetime(2025,10,25,8,0), work_day_end=datetime(2025,10,25,22,0)):
    """
    Schedule tasks to finish by deadlines, creating multiple-day schedules if needed.
    """
    # Sort tasks: High priority first, then earlier deadlines
    tasks_sorted = sorted(tasks, key=lambda t: (priority_map[t.priority], t.deadline))
    
    scheduled_tasks = []

    # Keep track of the next available time slot (we start from the last day)
    # We'll schedule backward from each task's deadline
    for task in tasks_sorted:
        end_time = min(task.deadline, work_day_end)
        start_time = end_time - task.duration
        
        # Adjust start time if it goes before the work day start
        current_day_start = work_day_start
        while start_time < current_day_start:
            # Task doesn't fit in current day, move to previous day
            end_time = current_day_start
            start_time = end_time - task.duration
            current_day_start -= timedelta(days=1)
        
        # Resolve conflicts with already scheduled tasks
        for scheduled in scheduled_tasks:
            # If overlapping, push the task earlier
            while not (start_time >= scheduled.scheduled_end or end_time <= scheduled.scheduled_start):
                end_time = scheduled.scheduled_start
                start_time = end_time - task.duration
        
        task.scheduled_start = start_time
        task.scheduled_end = end_time
        scheduled_tasks.append(task)
    
    # Sort final schedule by start time
    scheduled_tasks.sort(key=lambda t: t.scheduled_start)
    return scheduled_tasks

# Example usage
tasks = [
    Task("Finish project report", datetime(2025,10,27,18,0), 180, "High", "School"),
    Task("Study for exam", datetime(2025,10,26,21,0), 120, "High", "School"),
    Task("Workout", datetime(2025,10,25,20,0), 60, "Medium", "Health"),
    Task("Watch K-drama", datetime(2025,10,26,23,0), 90, "Low", "Entertainment"),
]

schedule = schedule_tasks(tasks)
for t in schedule:
    print(t)

print("\nAfter extending duration of first task:\n")
# Extend duration example
tasks[0].duration_extend(30)  # Extend first task by 30 minutes
schedule = schedule_tasks(tasks)
for t in schedule:
    print(t)

