from datetime import datetime, timedelta

priority_map = {"High": 1, "Medium": 2, "Low": 3}

class Task:
    def __init__(self, name, deadline, duration_minutes, priority, category=None):
        self.name = name
        self.deadline = deadline  # datetime
        self.duration = timedelta(minutes=duration_minutes)
        self.priority = priority
        self.category = category
        self.scheduled_start = None
        self.scheduled_end = None
        self.status = "Pending"

    def __repr__(self):
        return (f"{self.name} ({self.priority}) - {self.scheduled_start} "
                f"to {self.scheduled_end}")

def parse_deadline(s):
    """
    Parse deadline strings. Expected format: 'YYYY-MM-DD HH:MM'
    """
    try:
        return datetime.strptime(s.strip(), "%Y-%m-%d %H:%M")
    except ValueError:
        raise ValueError("Deadline must be in format 'YYYY-MM-DD HH:MM'")

def duration_minutes_from_h_m(hours, minutes):
    return int(hours) * 60 + int(minutes)

def schedule_tasks(tasks, work_day_start_hour=8, work_day_end_hour=22):
    """
    Schedule tasks as contiguous blocks finishing by their deadlines.
    - work_day_start_hour, work_day_end_hour are integers (0..23).
    - Tasks are scheduled backward from their deadlines and pushed earlier if conflicts occur.
    Returns tasks with scheduled_start/scheduled_end set.
    """
    # Sort by priority then by deadline (highest priority / earliest deadline first)
    tasks_sorted = sorted(tasks, key=lambda t: (priority_map.get(t.priority, 99), t.deadline))

    scheduled_intervals = []  # list of tuples (start_datetime, end_datetime, task)

    for task in tasks_sorted:
        remaining = task.duration
        # start trying to place the block ending at min(deadline, that day's work_end)
        current_end = datetime(task.deadline.year, task.deadline.month, task.deadline.day, work_day_end_hour, 0)
        if task.deadline < current_end:
            current_end = task.deadline

        # We'll try to find a contiguous slot of length 'remaining' ending <= current_end,
        # moving to previous days if needed, and avoiding overlaps with already scheduled_intervals.
        attempts = 0
        max_attempts = 1000  # guard vs infinite loops
        while remaining > timedelta(0) and attempts < max_attempts:
            attempts += 1
            # Compute start if we place entire remaining ending at current_end
            start_candidate = current_end - remaining
            day_start = datetime(current_end.year, current_end.month, current_end.day, work_day_start_hour, 0)

            if start_candidate < day_start:
                # Doesn't fit entirely in this day: use up this day's available time and move to previous day
                time_in_this_day = current_end - day_start
                remaining -= time_in_this_day
                # move current_end to previous day's work_end
                prev_day = day_start.date() - timedelta(days=1)
                current_end = datetime(prev_day.year, prev_day.month, prev_day.day, work_day_end_hour, 0)
                continue

            # Check for overlaps with already scheduled intervals
            overlaps = [ (s,e,t) for (s,e,t) in scheduled_intervals if not (start_candidate >= e or current_end <= s) ]
            if overlaps:
                # Find the earliest start among intervals that overlap the slot
                earliest_overlapping_start = min(s for (s,e,t) in overlaps)
                # push the candidate end to be just before that earliest start (so it finishes before overlap)
                current_end = earliest_overlapping_start
                # After pushing, loop will recompute start_candidate and check day bounds again
                continue

            # No overlap and fits within day -> place task
            task.scheduled_start = start_candidate
            task.scheduled_end = current_end
            scheduled_intervals.append((task.scheduled_start, task.scheduled_end, task))
            break

        if attempts >= max_attempts:
            raise RuntimeError(f"Scheduling failed for task {task.name} (too many attempts)")

        if task.scheduled_start is None:
            # Could not schedule (no space before deadline within allowed days)
            task.status = "Unscheduled"
        else:
            task.status = "Scheduled"

    # Return tasks sorted by start time (ignore unscheduled tasks at end)
    scheduled_intervals.sort(key=lambda x: x[0])
    result = [t for (_, _, t) in scheduled_intervals]
    # Append unscheduled (if any)
    unscheduled = [t for t in tasks_sorted if t.status != "Scheduled"]
    return result + unscheduled

# Small interactive helper to create tasks from user input
def create_task_from_input():
    name = input("Task name: ").strip()
    dstr = input("Deadline (YYYY-MM-DD HH:MM): ").strip()
    deadline = parse_deadline(dstr)
    hours = input("Estimated hours (integer): ").strip()
    minutes = input("Estimated minutes (integer): ").strip()
    duration_min = duration_minutes_from_h_m(hours or "0", minutes or "0")
    priority = input("Priority (High/Medium/Low): ").strip().capitalize()
    if priority not in priority_map:
        print("Unknown priority, defaulting to Low")
        priority = "Low"
    category = input("Category (optional): ").strip() or None
    return Task(name, deadline, duration_min, priority, category)

# Example usage (uncomment to run)
if __name__ == "__main__":
    # Build tasks interactively or programmatically
    tasks = []
    # Example programmatic tasks:
    tasks.append(Task("Finish project report", datetime(2025,10,27,18,0), 180, "High", "School"))
    tasks.append(Task("Study for exam", datetime(2025,10,26,21,0), 120, "High", "School"))
    tasks.append(Task("Workout", datetime(2025,10,25,20,0), 60, "Medium", "Health"))
    tasks.append(Task("Watch K-drama", datetime(2025,10,26,23,0), 90, "Low", "Entertainment"))

    schedule = schedule_tasks(tasks)
    for t in schedule:
        print(t)