from django.contrib import admin
from .models import Task

# Register your models here.

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'priority', 'deadline', 'estimated_time_minutes', 'status', 'created_at']
    list_filter = ['priority', 'status', 'deadline']
    search_fields = ['name', 'user__username']
    date_hierarchy = 'deadline'
    ordering = ['-deadline']
