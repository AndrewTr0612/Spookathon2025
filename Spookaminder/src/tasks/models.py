from django.db import models
from django.conf import settings

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
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Medium')
    category = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        # Order by deadline ascending so tasks appear earliest-first
        ordering = ['deadline', 'priority']
    
    def __str__(self):
        return f"{self.name} - {self.priority} priority (Due: {self.deadline})"
