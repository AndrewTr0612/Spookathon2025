from datetime import datetime, timedelta, time
from django.utils import timezone
from .models import Task

class Scheduler:
    def __init__(self, user):
        self.user = user
        self.fixed_events = []  # Will be used when FixedEvent model is added
    
    def _get_priority_value(self, priority):
        """Convert priority string to numeric value for sorting"""
        priority_map = {"High": 1, "Medium": 2, "Low": 3}
        return priority_map.get(priority, 4)
    
    def get_tasks_to_schedule(self, start_date=None, end_date=None):
        """Get tasks that need scheduling in the given period"""
        # Get tasks and sort by priority value (High->Medium->Low) then deadline
        tasks = Task.objects.filter(
            user=self.user,
            status='Pending'
        ).order_by(
            '-priority',  # Sort by priority field first
            'deadline'    # Then by deadline
        )
        
        if start_date:
            tasks = tasks.filter(deadline__gte=start_date)
        if end_date:
            tasks = tasks.filter(deadline__lte=end_date)
        
        return tasks
    
    def is_time_slot_available(self, start_time, end_time):
        """Check if a time slot conflicts with any fixed events or scheduled tasks"""
        # Check for conflicts with other scheduled tasks
        conflicts = Task.objects.filter(
            user=self.user,
            scheduled_start__lt=end_time,
            scheduled_end__gt=start_time
        ).exists()
        
        return not conflicts
    
    def find_next_available_slot(self, start_time, duration_minutes, end_limit):
        """Find next available time slot"""
        current_time = start_time
        while current_time + timedelta(minutes=duration_minutes) <= end_limit:
            end_time = current_time + timedelta(minutes=duration_minutes)
            if self.is_time_slot_available(current_time, end_time):
                return current_time
            current_time += timedelta(minutes=30)  # Try next slot in 30-min increments
        return None
    
    def generate_schedule(self, start_date=None, end_date=None):
        """Generate a schedule for pending tasks"""
        if not start_date:
            start_date = timezone.now()
        if not end_date:
            # Find the latest deadline among pending tasks
            latest_task = Task.objects.filter(
                user=self.user,
                status='Pending'
            ).order_by('-deadline').first()
            end_date = latest_task.deadline if latest_task else start_date + timedelta(days=7)
        
        tasks = self.get_tasks_to_schedule(start_date, end_date)
        scheduled_tasks = []
        
        for task in tasks:
            # Try to schedule the task
            start_time = self.find_next_available_slot(
                start_date,
                task.estimated_time_minutes,
                task.deadline
            )
            
            if start_time:
                task.scheduled_start = start_time
                task.scheduled_end = start_time + timedelta(minutes=task.estimated_time_minutes)
                task.save()
                scheduled_tasks.append(task)
            else:
                print(f"Warning: Could not schedule task '{task.name}'")
        
        return scheduled_tasks
    
    def reschedule_after_update(self, updated_task):
        """Reschedule tasks after a task is updated"""
        # Clear schedules of all pending tasks
        Task.objects.filter(
            user=self.user,
            status='Pending'
        ).update(scheduled_start=None, scheduled_end=None)
        
        # Regenerate schedule
        return self.generate_schedule()