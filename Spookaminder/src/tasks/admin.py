from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'priority', 'deadline', 'status', 'created_at']
    list_filter = ['priority', 'status', 'deadline']
    search_fields = ['name', 'user__username']
    date_hierarchy = 'deadline'
    ordering = ['-deadline']
