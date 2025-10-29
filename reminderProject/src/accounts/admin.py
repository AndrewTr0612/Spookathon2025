from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib import messages
from django.utils import timezone
from .models import User

# Register your models here.

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'get_age', 'tokens', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'groups']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    ordering = ['username']
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'date_of_birth')}),
        ('Game Info', {'fields': ('tokens',)}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'date_of_birth', 'tokens'),
        }),
    )
    
    readonly_fields = ['last_login', 'date_joined']
    
    def get_age(self, obj):
        """Display calculated age in admin list"""
        return obj.age if obj.age else '-'
    get_age.short_description = 'Age'
    filter_horizontal = ['groups', 'user_permissions']
    actions = ['add_100_tokens', 'add_500_tokens', 'add_1000_tokens', 'reset_tokens', 'reset_daily_task_limit']
    
    def add_100_tokens(self, request, queryset):
        """Add 100 tokens to selected users"""
        count = 0
        for user in queryset:
            user.tokens += 100
            user.save()
            count += 1
        self.message_user(request, f'Added 100 tokens to {count} user(s).', messages.SUCCESS)
    add_100_tokens.short_description = '🎃 Add 100 tokens to selected users'
    
    def add_500_tokens(self, request, queryset):
        """Add 500 tokens to selected users"""
        count = 0
        for user in queryset:
            user.tokens += 500
            user.save()
            count += 1
        self.message_user(request, f'Added 500 tokens to {count} user(s).', messages.SUCCESS)
    add_500_tokens.short_description = '🎃 Add 500 tokens to selected users'
    
    def add_1000_tokens(self, request, queryset):
        """Add 1000 tokens to selected users"""
        count = 0
        for user in queryset:
            user.tokens += 1000
            user.save()
            count += 1
        self.message_user(request, f'Added 1000 tokens to {count} user(s).', messages.SUCCESS)
    add_1000_tokens.short_description = '🎃 Add 1000 tokens to selected users'
    
    def reset_tokens(self, request, queryset):
        """Reset tokens to 0 for selected users"""
        count = 0
        for user in queryset:
            user.tokens = 0
            user.save()
            count += 1
        self.message_user(request, f'Reset tokens for {count} user(s).', messages.WARNING)
    reset_tokens.short_description = '🔄 Reset tokens to 0 for selected users'
    
    def reset_daily_task_limit(self, request, queryset):
        """Delete all tasks created today for selected users to reset their daily task limit"""
        from tasks.models import Task
        
        # Get today's date range
        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = timezone.now().replace(hour=23, minute=59, second=59, microsecond=999999)
        
        total_deleted = 0
        for user in queryset:
            # Delete all tasks created today for this user
            deleted = Task.objects.filter(
                user=user,
                created_at__gte=today_start,
                created_at__lte=today_end
            ).delete()
            total_deleted += deleted[0]  # deleted[0] contains the count
        
        self.message_user(
            request,
            f'Reset daily task limit for {queryset.count()} user(s). Deleted {total_deleted} task(s) created today. Users can now create 5 new tasks today.',
            messages.SUCCESS
        )
    reset_daily_task_limit.short_description = '📋 Reset daily task limit (delete today\'s tasks)'
