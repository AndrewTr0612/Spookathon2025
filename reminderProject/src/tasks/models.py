from django.db import models
from django.conf import settings

# Create your models here.

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]
    
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks')
    name = models.CharField(max_length=200)
    deadline = models.DateTimeField()
    estimated_time_minutes = models.IntegerField(help_text="Total time in minutes")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Medium')
    category = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    scheduled_start = models.DateTimeField(null=True, blank=True)
    scheduled_end = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-deadline', 'priority']
    
    def __str__(self):
        return f"{self.name} - {self.priority} priority (Due: {self.deadline})"
    
    @property
    def estimated_hours(self):
        """Return hours part of estimated time"""
        return self.estimated_time_minutes // 60
    
    @property
    def estimated_minutes_remainder(self):
        """Return minutes remainder after hours"""
        return self.estimated_time_minutes % 60
