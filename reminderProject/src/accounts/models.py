from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date

# Create your models here.

class User(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    # Tokens used for small game/quest system. Earned when completing tasks.
    tokens = models.IntegerField(default=0)
    
    @property
    def age(self):
        """Calculate age from date of birth"""
        if self.date_of_birth:
            today = date.today()
            age = today.year - self.date_of_birth.year
            # Adjust if birthday hasn't occurred yet this year
            if today.month < self.date_of_birth.month or (today.month == self.date_of_birth.month and today.day < self.date_of_birth.day):
                age -= 1
            return age
        return None
    
    def __str__(self):
        return self.username
