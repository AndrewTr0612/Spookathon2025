from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User
from datetime import datetime

# Create your views here.

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        name = request.POST.get('name')
        date_of_birth = request.POST.get('date_of_birth')
        
        if password != password2:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'accounts/register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return render(request, 'accounts/register.html')
        
        try:
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=name,
                date_of_birth=datetime.strptime(date_of_birth, '%Y-%m-%d').date() if date_of_birth else None
            )
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
            return render(request, 'accounts/register.html')
    
    return render(request, 'accounts/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password!')
            return render(request, 'accounts/login.html')
    
    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('login')


@login_required
def home_view(request):
    return render(request, 'accounts/home.html')


@login_required
def profile_view(request):
    """View and edit user profile"""
    return render(request, 'accounts/profile.html')


@login_required
def profile_edit(request):
    """Edit user profile"""
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('name', '')
        
        # Handle date of birth field
        date_of_birth = request.POST.get('date_of_birth', '')
        if date_of_birth:
            try:
                user.date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
            except ValueError:
                messages.error(request, 'Please enter a valid date!')
                return render(request, 'accounts/profile_edit.html')
        else:
            user.date_of_birth = None
            
        user.email = request.POST.get('email', '')
        
        # Update password if provided
        new_password = request.POST.get('new_password', '')
        if new_password:
            user.set_password(new_password)
            messages.info(request, 'Password changed! Please login again.')
            user.save()
            logout(request)
            return redirect('login')
        
        try:
            user.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        except Exception as e:
            messages.error(request, f'Error updating profile: {str(e)}')
    
    return render(request, 'accounts/profile_edit.html')
