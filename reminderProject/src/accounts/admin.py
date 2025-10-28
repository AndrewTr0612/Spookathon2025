from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib import messages
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
    actions = ['add_100_tokens', 'add_500_tokens', 'add_1000_tokens', 'reset_tokens']
    
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
