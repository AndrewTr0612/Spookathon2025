from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    name = models.CharField(max_length=200)
    deadline = models.DateTimeField()
    priority = models.CharField(
        max_length=6,
        choices=PRIORITY_CHOICES,
        default='Medium'
    )
    status = models.CharField(
        max_length=9,
        choices=STATUS_CHOICES,
        default='Pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['priority', 'deadline', 'name']
        indexes = [
            models.Index(fields=['user', 'status', 'priority', 'deadline', 'name']),
        ]

    def __str__(self):
        return f"{self.name} (Priority: {self.priority}, Due: {self.deadline})"

    # ----- Core Methods -----
    def mark_complete(self):
        """Mark task as completed and timestamp it."""
        self.status = 'Completed'
        self.completed_at = timezone.now()
        self.save()

    def mark_cancelled(self):
        """Mark task as cancelled."""
        self.status = 'Cancelled'
        self.save()

    def is_overdue(self):
        """Check if a pending task is past its deadline."""
        return self.status == 'Pending' and timezone.now() > self.deadline

    # ----- Query Helpers -----
    @classmethod
    def get_sorted_tasks(cls, user):
        """Return all pending tasks for a user, sorted by priority → deadline → name."""
        priority_order = models.Case(
            models.When(priority='High', then=1),
            models.When(priority='Medium', then=2),
            models.When(priority='Low', then=3),
            default=4,
            output_field=models.IntegerField(),
        )

        return cls.objects.filter(
            user=user,
            status='Pending'
        ).annotate(
            priority_order=priority_order
        ).order_by(
            'priority_order', 'deadline', 'name'
        )
