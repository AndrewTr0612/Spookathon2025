from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Task
from datetime import datetime, timedelta
from django.utils import timezone

# Create your views here.

@login_required
def task_list(request):
    """Display all tasks for the logged-in user"""
    # Separate completed and pending tasks
    pending_tasks = Task.objects.filter(user=request.user).exclude(status='Completed').order_by('deadline')
    completed_tasks = Task.objects.filter(user=request.user, status='Completed').order_by('-deadline')
    
    completed_count = completed_tasks.count()
    pending_count = pending_tasks.count()
    
    context = {
        'pending_tasks': pending_tasks,
        'completed_tasks': completed_tasks,
        'completed_count': completed_count,
        'pending_count': pending_count,
        'total_tasks': pending_count + completed_count,
    }
    return render(request, 'tasks/task_list.html', context)


@login_required
def task_create(request):
    """Create a new task"""
    if request.method == 'POST':
        # Get today's date range (from 00:00:00 to 23:59:59)
        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = timezone.now().replace(hour=23, minute=59, second=59, microsecond=999999)
        
        # Count tasks created today (based on created_at timestamp)
        tasks_created_today = Task.objects.filter(
            user=request.user,
            created_at__gte=today_start,
            created_at__lte=today_end
        ).count()
        
        # Enforce maximum of 5 tasks created per day
        if tasks_created_today >= 5:
            messages.error(request, 'Daily limit reached! You can only create 5 tasks per day. The limit will reset at midnight.')
            return redirect('task_list')

        name = request.POST.get('name')
        deadline_str = request.POST.get('deadline')
        priority = request.POST.get('priority', 'Medium')
        category = request.POST.get('category', '')
        
        try:
            # Parse deadline
            deadline = datetime.strptime(deadline_str, '%Y-%m-%dT%H:%M')
            
            # Make deadline timezone-aware
            deadline_aware = timezone.make_aware(deadline)
            
            # Get current time and end of today
            now = timezone.now()
            today_end = now.replace(hour=23, minute=59, second=59, microsecond=999999)
            
            # Validate deadline is between now and end of today
            if deadline_aware < now:
                messages.error(request, 'Task deadline cannot be in the past! Please choose a time from now onwards.')
                return render(request, 'tasks/task_form.html', {
                    'tasks_created_today': tasks_created_today,
                    'remaining_tasks': 5 - tasks_created_today
                })
            
            if deadline_aware > today_end:
                messages.error(request, 'Task deadline must be within today! You can only create tasks for the current day.')
                return render(request, 'tasks/task_form.html', {
                    'tasks_created_today': tasks_created_today,
                    'remaining_tasks': 5 - tasks_created_today
                })
            
            # Create task
            task = Task.objects.create(
                user=request.user,
                name=name,
                deadline=deadline_aware,
                priority=priority,
                category=category if category else None
            )
            
            # Calculate remaining tasks for today
            remaining_tasks = 5 - (tasks_created_today + 1)
            messages.success(request, f'Task "{name}" created successfully! You can create {remaining_tasks} more task(s) today.')
            return redirect('task_list')
            
        except ValueError as e:
            messages.error(request, f'Invalid input: {str(e)}')
            return render(request, 'tasks/task_form.html')
    
    # For GET request, show how many tasks can still be created today
    today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = timezone.now().replace(hour=23, minute=59, second=59, microsecond=999999)
    tasks_created_today = Task.objects.filter(
        user=request.user,
        created_at__gte=today_start,
        created_at__lte=today_end
    ).count()
    remaining_tasks = 5 - tasks_created_today
    
    context = {
        'tasks_created_today': tasks_created_today,
        'remaining_tasks': remaining_tasks
    }
    return render(request, 'tasks/task_form.html', context)


@login_required
def task_update(request, task_id):
    """Update an existing task"""
    task = get_object_or_404(Task, id=task_id, user=request.user)
    
    if request.method == 'POST':
        task.name = request.POST.get('name')
        deadline_str = request.POST.get('deadline')
        task.priority = request.POST.get('priority', 'Medium')
        task.category = request.POST.get('category', '')
        task.status = request.POST.get('status', 'Pending')
        
        try:
            # Parse deadline and make it timezone-aware
            deadline = datetime.strptime(deadline_str, '%Y-%m-%dT%H:%M')
            task.deadline = timezone.make_aware(deadline)
            task.save()
            messages.success(request, f'Task "{task.name}" updated successfully!')
            return redirect('task_list')
            
        except ValueError as e:
            messages.error(request, f'Invalid input: {str(e)}')
            return render(request, 'tasks/task_form.html', {'task': task, 'is_update': True})
    
    return render(request, 'tasks/task_form.html', {'task': task, 'is_update': True})


@login_required
def task_delete(request, task_id):
    """Delete a task"""
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task_name = task.name
    task.delete()
    messages.success(request, f'Task "{task_name}" deleted successfully!')
    return redirect('task_list')


@login_required
def task_complete(request, task_id):
    """Mark a task as completed"""
    task = get_object_or_404(Task, id=task_id, user=request.user)
    # Only award token if task was not already completed
    if task.status != 'Completed':
        task.status = 'Completed'
        task.save()

        # Add 1 token to the user
        user = request.user
        user.tokens = (user.tokens or 0) + 1
        user.save()

        messages.success(request, f'Task "{task.name}" marked as completed! You earned 1 token.')
    else:
        messages.info(request, f'Task "{task.name}" is already completed.')
    return redirect('task_list')


@login_required
def upcoming_tasks_api(request):
    """API endpoint for upcoming tasks - used by reminder system"""
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)
    
    now = timezone.now()
    
    # Get all pending tasks due within the next hour
    upcoming_tasks = Task.objects.filter(
        user=request.user,
        status__in=['Pending', 'In Progress'],
        deadline__gte=now,
        deadline__lte=now + timedelta(hours=1)
    ).order_by('deadline')
    
    # Also get overdue tasks
    overdue_tasks = Task.objects.filter(
        user=request.user,
        status__in=['Pending', 'In Progress'],
        deadline__lt=now
    ).order_by('deadline')
    
    # Combine and format tasks
    all_tasks = list(upcoming_tasks) + list(overdue_tasks)
    
    tasks_data = []
    for task in all_tasks:
        time_diff = task.deadline - now
        minutes_until = int(time_diff.total_seconds() / 60)
        
        tasks_data.append({
            'id': task.id,
            'name': task.name,
            'deadline': task.deadline.isoformat(),
            'priority': task.priority,
            'minutes_until': minutes_until,
            'is_overdue': minutes_until < 0
        })
    
    return JsonResponse({'tasks': tasks_data})
