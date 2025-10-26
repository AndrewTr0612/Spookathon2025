from datetime import datetime, timedelta, time
from enum import Enum

class WeekDay(Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

class FixedEvent:
    def __init__(self, name, weekdays, start_time, end_time, category):
        """
        Args:
            name (str): Name of the fixed event (e.g., "CS101", "Work Shift")
            weekdays (list[WeekDay]): List of days when event occurs
            start_time (time): Start time (e.g., time(9,30) for 9:30 AM)
            end_time (time): End time
            category (str): "Class" or "Work"
        """
        self.name = name
        self.weekdays = weekdays  # List of WeekDay enums
        self.start_time = start_time
        self.end_time = end_time
        self.category = category

    def __repr__(self):
        """String representation of the fixed event"""
        days = [day.name for day in self.weekdays]
        return (f"{self.name} ({self.category}) - "
                f"{', '.join(days)} at {self.start_time.strftime('%H:%M')} - "
                f"{self.end_time.strftime('%H:%M')}")
    
    def occurs_on_date(self, date):
        """Check if the event occurs on a specific date"""
        return date.weekday() in [day.value for day in self.weekdays]

class FixedSchedule:
    def __init__(self):
        self.events = []  # List to store all fixed events
    
    def add_event(self, event):
        """Add a single fixed event"""
        if not isinstance(event, FixedEvent):
            raise TypeError("Event must be an instance of FixedEvent")
        self.events.append(event)
    
    def add_events(self, events):
        """Add multiple fixed events at once"""
        for event in events:
            self.add_event(event)
    
    def remove_event(self, event_name):
        """Remove an event by name"""
        self.events = [e for e in self.events if e.name != event_name]
    
    def get_events_for_date(self, date):
        """Get all events occurring on a specific date"""
        return [event for event in self.events if event.occurs_on_date(date)]
    
    def get_events_by_category(self, category):
        """Get all events of a specific category"""
        return [event for event in self.events if event.category == category]
    
    def __repr__(self):
        """String representation of the schedule"""
        return "\n".join(str(event) for event in self.events)
