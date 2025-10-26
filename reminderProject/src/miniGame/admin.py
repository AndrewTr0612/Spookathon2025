from django.contrib import admin
from django.contrib import messages
from .models import Plant, WaterTransaction


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ('user', 'growth_stage', 'water_drops', 'water_progress', 'updated_at')
    list_filter = ('growth_stage', 'created_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    actions = ['water_plant_once', 'water_plant_5x', 'reset_plant_to_seed', 'max_out_plant']
    
    fieldsets = (
        ('User Info', {
            'fields': ('user',)
        }),
        ('Plant Status', {
            'fields': ('growth_stage', 'water_drops', 'water_progress')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def water_plant_once(self, request, queryset):
        """Add 1 water drop to selected plants"""
        count = 0
        for plant in queryset:
            plant.add_water_drop()
            count += 1
        self.message_user(request, f'Watered {count} plant(s).', messages.SUCCESS)
    water_plant_once.short_description = '💧 Water plant once'
    
    def water_plant_5x(self, request, queryset):
        """Add 5 water drops to selected plants"""
        count = 0
        for plant in queryset:
            for _ in range(5):
                plant.add_water_drop()
            count += 1
        self.message_user(request, f'Watered {count} plant(s) 5 times.', messages.SUCCESS)
    water_plant_5x.short_description = '💧💧💧💧💧 Water plant 5 times'
    
    def reset_plant_to_seed(self, request, queryset):
        """Reset plants to stage 1"""
        count = 0
        for plant in queryset:
            plant.growth_stage = 1
            plant.water_drops = 0
            plant.water_progress = 0
            plant.save()
            count += 1
        self.message_user(request, f'Reset {count} plant(s) to seed stage.', messages.WARNING)
    reset_plant_to_seed.short_description = '🌰 Reset plant to seed stage'
    
    def max_out_plant(self, request, queryset):
        """Max out plants to stage 4 with 100% progress"""
        count = 0
        for plant in queryset:
            plant.growth_stage = 4
            plant.water_progress = 100
            plant.save()
            count += 1
        self.message_user(request, f'Maxed out {count} plant(s).', messages.SUCCESS)
    max_out_plant.short_description = '🌳 Max out plant to stage 4'


@admin.register(WaterTransaction)
class WaterTransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'tokens_spent', 'water_drops_received', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('timestamp',)
    date_hierarchy = 'timestamp'
