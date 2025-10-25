from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task
from datetime import datetime

# Create your views here.

@login_required
def task_list(request):
    """Display all tasks for the logged-in user"""
    tasks = Task.objects.filter(user=request.user)
    completed_count = tasks.filter(status='Completed').count()
    pending_count = tasks.exclude(status='Completed').count()
    
    context = {
        'tasks': tasks,
        'completed_count': completed_count,
        'pending_count': pending_count,
    }
    return render(request, 'tasks/task_list.html', context)


@login_required
def task_create(request):
    """Create a new task"""
    if request.method == 'POST':
        name = request.POST.get('name')
        deadline_str = request.POST.get('deadline')
        hours = request.POST.get('hours', 0)
        minutes = request.POST.get('minutes', 0)
        priority = request.POST.get('priority', 'Medium')
        category = request.POST.get('category', '')
        
        try:
            # Parse deadline
            deadline = datetime.strptime(deadline_str, '%Y-%m-%dT%H:%M')
            
            # Calculate total minutes
            estimated_time_minutes = int(hours) * 60 + int(minutes)
            
            if estimated_time_minutes <= 0:
                messages.error(request, 'Estimated time must be greater than 0!')
                return render(request, 'tasks/task_form.html')
            
            # Create task
            task = Task.objects.create(
                user=request.user,
                name=name,
                deadline=deadline,
                estimated_time_minutes=estimated_time_minutes,
                priority=priority,
                category=category if category else None
            )
            
            messages.success(request, f'Task "{name}" created successfully!')
            return redirect('task_list')
            
        except ValueError as e:
            messages.error(request, f'Invalid input: {str(e)}')
            return render(request, 'tasks/task_form.html')
    
    return render(request, 'tasks/task_form.html')


@login_required
def task_update(request, task_id):
    """Update an existing task"""
    task = get_object_or_404(Task, id=task_id, user=request.user)
    
    if request.method == 'POST':
        task.name = request.POST.get('name')
        deadline_str = request.POST.get('deadline')
        hours = request.POST.get('hours', 0)
        minutes = request.POST.get('minutes', 0)
        task.priority = request.POST.get('priority', 'Medium')
        task.category = request.POST.get('category', '')
        task.status = request.POST.get('status', 'Pending')
        
        try:
            # Parse deadline
            task.deadline = datetime.strptime(deadline_str, '%Y-%m-%dT%H:%M')
            
            # Calculate total minutes
            task.estimated_time_minutes = int(hours) * 60 + int(minutes)
            
            if task.estimated_time_minutes <= 0:
                messages.error(request, 'Estimated time must be greater than 0!')
                return render(request, 'tasks/task_form.html', {'task': task, 'is_update': True})
            
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
    task.status = 'Completed'
    task.save()
    messages.success(request, f'Task "{task.name}" marked as completed!')
    return redirect('task_list')
