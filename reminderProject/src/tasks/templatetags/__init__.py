from django import template

register = template.Library()

@register.filter
def day_name(value):
    """Convert day number (0-6) to day name"""
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    try:
        return days[int(value)]
    except (ValueError, IndexError):
        return value
