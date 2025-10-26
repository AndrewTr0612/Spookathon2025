from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Plant(models.Model):
    """Model representing a user's plant in the mini-game"""
    STAGE_CHOICES = [
        (1, 'Seed'),
        (2, 'Sprout'),
        (3, 'Young Plant'),
        (4, 'Mature Plant'),
    ]
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='plant')
    growth_stage = models.IntegerField(
        default=1, 
        validators=[MinValueValidator(1), MaxValueValidator(4)],
        choices=STAGE_CHOICES
    )
    water_drops = models.IntegerField(default=0)  # Total water drops given to plant
    water_progress = models.IntegerField(default=0)  # Progress towards next stage (0-100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'minigame_plant'
        verbose_name = 'Plant'
        verbose_name_plural = 'Plants'
    
    def __str__(self):
        return f"{self.user.username}'s Plant - Stage {self.growth_stage}"
    
    def add_water_drop(self):
        """Add one water drop and update growth"""
        self.water_drops += 1
        
        # Each water drop adds 25% progress (4 drops per stage)
        self.water_progress += 25
        
        # Check if plant should grow to next stage
        if self.water_progress >= 100 and self.growth_stage < 4:
            self.growth_stage += 1
            self.water_progress = 0  # Reset progress for next stage
        
        self.save()
        return self.growth_stage
    
    def get_stage_name(self):
        """Get the display name of current growth stage"""
        return dict(self.STAGE_CHOICES).get(self.growth_stage, 'Unknown')
    
    def drops_needed_for_next_stage(self):
        """Calculate drops needed to reach next stage"""
        if self.growth_stage >= 4:
            return 0  # Already at max stage
        remaining_progress = 100 - self.water_progress
        return (remaining_progress + 24) // 25  # Round up


class WaterTransaction(models.Model):
    """Model to track water drop exchanges"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='water_transactions')
    tokens_spent = models.IntegerField()
    water_drops_received = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'minigame_water_transaction'
        verbose_name = 'Water Transaction'
        verbose_name_plural = 'Water Transactions'
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.user.username} - {self.tokens_spent} tokens → {self.water_drops_received} drops"
