from django.contrib import admin
from django.contrib import messages
from django.utils import timezone
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'priority', 'deadline', 'status', 'created_at']
    list_filter = ['priority', 'status', 'deadline']
    search_fields = ['name', 'user__username']
    date_hierarchy = 'deadline'
    ordering = ['-deadline']
    actions = ['reset_daily_task_limit']
    
    def reset_daily_task_limit(self, request, queryset):
        """Delete all tasks created today for the selected tasks' users to reset their daily limit"""
        # Get unique users from selected tasks
        users = set(task.user for task in queryset)
        
        # Get today's date range
        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = timezone.now().replace(hour=23, minute=59, second=59, microsecond=999999)
        
        total_deleted = 0
        for user in users:
            # Delete all tasks created today for this user
            deleted = Task.objects.filter(
                user=user,
                created_at__gte=today_start,
                created_at__lte=today_end
            ).delete()
            total_deleted += deleted[0]  # deleted[0] contains the count
        
        self.message_user(
            request,
            f'Reset daily task limit for {len(users)} user(s). Deleted {total_deleted} task(s) created today. Users can now create 5 new tasks today.',
            messages.SUCCESS
        )
    reset_daily_task_limit.short_description = '🔄 Reset daily task limit (delete today\'s tasks for selected users)'
