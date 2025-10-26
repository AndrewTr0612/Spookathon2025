from datetime import datetime, time
from Tasks import Task
from schedule import Schedule
from fixed_schedule import WeekDay, FixedEvent

def test_schedule_generation():
    # Create a schedule
    schedule = Schedule()
    
    # 1. Add fixed events (classes and work)
    fixed_events = [
        FixedEvent("CS101", [WeekDay.MONDAY, WeekDay.WEDNESDAY], 
                   time(9,0), time(10,30), "Class"),
        FixedEvent("MATH285", [WeekDay.MONDAY, WeekDay.WEDNESDAY], 
                   time(11,0), time(12,30), "Class"),
        FixedEvent("Work Shift", [WeekDay.TUESDAY, WeekDay.THURSDAY], 
                   time(13,0), time(17,0), "Work")
    ]
    
    for event in fixed_events:
        schedule.add_fixed_event(event)
    
    # 2. Create tasks with different priorities and deadlines
    tasks = [
        Task("High Priority Assignment", 
             datetime(2025,10,28,23,59), 120, "High", "School"),
        Task("Medium Priority Reading", 
             datetime(2025,10,27,20,0), 60, "Medium", "School"),
        Task("Low Priority Review", 
             datetime(2025,10,27,17,0), 30, "Low", "School"),
        Task("Urgent Project", 
             datetime(2025,10,26,16,0), 90, "High", "Work")
    ]
    
    # 3. Add tasks to schedule
    for task in tasks:
        schedule.insert_task(task)
    
    # 4. Generate schedule for specific period
    work_period_start = datetime(2025,10,25,8,0)  # Sunday 8 AM
    work_period_end = datetime(2025,10,28,23,59)  # Tuesday midnight
    
    print("\nFixed Schedule:")
    print(schedule.fixed_schedule)
    
    print("\nGenerating schedule from", 
          work_period_start.strftime("%Y-%m-%d %H:%M"),
          "to",
          work_period_end.strftime("%Y-%m-%d %H:%M"))
    
    scheduled_tasks = schedule.generate_schedule(work_period_start, work_period_end)
    
    # 5. Verify and print results
    print("\nScheduled Tasks:")
    for task in scheduled_tasks:
        print(f"\nTask: {task.name}")
        print(f"Priority: {task.priority}")
        print(f"Deadline: {task.deadline.strftime('%Y-%m-%d %H:%M')}")
        print(f"Scheduled: {task.scheduled_start.strftime('%Y-%m-%d %H:%M')} - "
              f"{task.scheduled_end.strftime('%Y-%m-%d %H:%M')}")
        
        # Verify scheduling constraints
        assert task.scheduled_end <= task.deadline, "Task scheduled after deadline"
        assert task.scheduled_start >= work_period_start, "Task scheduled before work period"
        assert task.scheduled_end <= work_period_end, "Task scheduled after work period"
        
        # Verify no conflicts with fixed events
        assert schedule.is_time_slot_available(task.scheduled_start, task.scheduled_end), \
            f"Task {task.name} conflicts with fixed events"

if __name__ == "__main__":
    try:
        test_schedule_generation()
        print("\nAll tests passed successfully!")
    except AssertionError as e:
        print(f"\nTest failed: {e}")
    except Exception as e:
        print(f"\nError occurred: {e}")