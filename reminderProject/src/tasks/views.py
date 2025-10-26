from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task
from datetime import datetime

# Create your views here.

@login_required
def task_list(request):
    """Display all tasks for the logged-in user"""
    # Show user's tasks ordered by deadline (earliest first)
    tasks = Task.objects.filter(user=request.user).order_by('deadline')
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
        # Enforce maximum of 5 active tasks per user
        user_task_count = Task.objects.filter(user=request.user).count()
        if user_task_count >= 5:
            messages.error(request, 'You can only have up to 5 tasks. Please complete or delete an existing task before adding a new one.')
            return redirect('task_list')

        name = request.POST.get('name')
        deadline_str = request.POST.get('deadline')
        priority = request.POST.get('priority', 'Medium')
        category = request.POST.get('category', '')
        
        try:
            # Parse deadline
            deadline = datetime.strptime(deadline_str, '%Y-%m-%dT%H:%M')
            
            # Create task
            task = Task.objects.create(
                user=request.user,
                name=name,
                deadline=deadline,
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
        task.priority = request.POST.get('priority', 'Medium')
        task.category = request.POST.get('category', '')
        task.status = request.POST.get('status', 'Pending')
        
        try:
            # Parse deadline
            task.deadline = datetime.strptime(deadline_str, '%Y-%m-%dT%H:%M')
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
