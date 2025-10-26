from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from accounts.models import User
from tasks.models import Task


class Command(BaseCommand):
    help = 'Creates a demo user with tasks and tokens'

    def handle(self, *args, **kwargs):
        # Create or update demo user
        demo_user, created = User.objects.get_or_create(
            username='demo',
            defaults={
                'email': 'demo@spookaminder.com',
                'first_name': 'Demo',
                'last_name': 'User',
                'tokens': 1000,
            }
        )
        
        if not created:
            # Update existing demo user
            demo_user.tokens = 1000
            demo_user.save()
            self.stdout.write(self.style.WARNING('Demo user already exists. Updated tokens to 1000.'))
        else:
            # Set password for new user
            demo_user.set_password('demo123')
            demo_user.save()
            self.stdout.write(self.style.SUCCESS('Created new demo user.'))
        
        # Clear existing tasks for demo user
        Task.objects.filter(user=demo_user).delete()
        
        # Create completed tasks
        completed_tasks = [
            {
                'name': '🎃 Decorate for Halloween',
                'deadline': timezone.now() - timedelta(days=2),
                'status': 'Completed',
                'priority': 'High',
                'category': 'Home',
            },
            {
                'name': '👻 Watch scary movies',
                'deadline': timezone.now() - timedelta(days=1),
                'status': 'Completed',
                'priority': 'Low',
                'category': 'Entertainment',
            },
            {
                'name': '🦇 Finish Halloween costume',
                'deadline': timezone.now() - timedelta(days=3),
                'status': 'Completed',
                'priority': 'High',
                'category': 'Personal',
            },
            {
                'name': '🕷️ Clean the garage',
                'deadline': timezone.now() - timedelta(days=5),
                'status': 'Completed',
                'priority': 'Medium',
                'category': 'Home',
            },
            {
                'name': '🍬 Buy Halloween candy',
                'deadline': timezone.now() - timedelta(days=4),
                'status': 'Completed',
                'priority': 'High',
                'category': 'Shopping',
            },
        ]
        
        # Create pending tasks
        pending_tasks = [
            {
                'name': '🎭 Attend Halloween party',
                'deadline': timezone.now() + timedelta(days=1),
                'status': 'Pending',
                'priority': 'High',
                'category': 'Social',
            },
            {
                'name': '📚 Study for Math exam',
                'deadline': timezone.now() + timedelta(days=3),
                'status': 'Pending',
                'priority': 'High',
                'category': 'School',
            },
            {
                'name': '🏋️ Hit the gym',
                'deadline': timezone.now() + timedelta(hours=4),
                'status': 'Pending',
                'priority': 'Medium',
                'category': 'Health',
            },
            {
                'name': '🛒 Grocery shopping',
                'deadline': timezone.now() + timedelta(days=2),
                'status': 'Pending',
                'priority': 'Medium',
                'category': 'Shopping',
            },
            {
                'name': '💻 Work on coding project',
                'deadline': timezone.now() + timedelta(days=4),
                'status': 'In Progress',
                'priority': 'High',
                'category': 'Work',
            },
            {
                'name': '📧 Reply to important emails',
                'deadline': timezone.now() + timedelta(hours=6),
                'status': 'Pending',
                'priority': 'High',
                'category': 'Work',
            },
            {
                'name': '🧹 Deep clean bedroom',
                'deadline': timezone.now() + timedelta(days=5),
                'status': 'Pending',
                'priority': 'Low',
                'category': 'Home',
            },
        ]
        
        # Create all tasks
        all_tasks = completed_tasks + pending_tasks
        for task_data in all_tasks:
            Task.objects.create(
                user=demo_user,
                **task_data
            )
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(completed_tasks)} completed tasks'))
        self.stdout.write(self.style.SUCCESS(f'Created {len(pending_tasks)} pending tasks'))
        self.stdout.write(self.style.SUCCESS('='*50))
        self.stdout.write(self.style.SUCCESS('Demo User Credentials:'))
        self.stdout.write(self.style.SUCCESS(f'Username: demo'))
        self.stdout.write(self.style.SUCCESS(f'Password: demo123'))
        self.stdout.write(self.style.SUCCESS(f'Tokens: 1000'))
        self.stdout.write(self.style.SUCCESS('='*50))
