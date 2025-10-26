# 🎃 SPOOKAMINDER - Halloween Task Manager

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-orange)
![Django](https://img.shields.io/badge/Django-5.2.7-darkgreen)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-blue)
![License](https://img.shields.io/badge/license-MIT-purple)

A spooky-themed, mobile-first Django web application with gamification features, task tracking, and a delightful plant watering mini-game! 🌱👻

[Features](#-features) • [Quick Start](#-quick-start) • [Game System](#-mini-game-system) • [Tech Stack](#-tech-stack)

</div>

---

## ✨ Features

### 🎃 Halloween Theme
- **Spooky Design**: Orange (#ff6600) and purple (#1a0928) color scheme
- **Spider Web Background**: Atmospheric overlay with blend modes
- **Creepster Font**: Halloween-themed typography
- **Ghost Animations**: Floating ghost icons throughout
- **Glowing Effects**: Text shadows and neon-style buttons

### 📱 Mobile-First Design
- Modern iOS/Android-style interface
- Smooth animations and touch-friendly buttons
- Bottom navigation bar
- Floating action button
- Card-based UI with gradients

### 🔐 User Authentication
- User registration with name and age
- Secure login/logout functionality
- Profile management system
- Edit name, age, email, and password
- Beautiful gradient UI design

### ✅ Task Management
- Create, read, update, and delete tasks
- Track task name, deadline, estimated time (hours and minutes), and priority
- Priority levels: High 🔥, Medium ⚡, Low ✅
- Task status tracking: Pending, In Progress, Completed
- Optional category assignment
- Automatic time conversion (hours + minutes → total minutes in database)
- Color-coded priority badges (Red=High, Orange=Medium, Green=Low)
- Visual task cards with left-border color coding
- Quick complete/edit/delete actions
- Task statistics dashboard

### 👤 Profile Management
- View profile with avatar
- Edit personal information (name, age, email)
- Change password securely
- Profile history (joined date)
- User avatar with initials

## 🚀 Quick Start

1. **Set up database**:
   ```bash
   cd src
   python3 manage.py migrate
   ```

2. **Run the development server**:
   ```bash
   python3 manage.py runserver
   ```

3. **Access the application**:
   - Register: http://127.0.0.1:8000/register/
   - Login: http://127.0.0.1:8000/login/
   - Home: http://127.0.0.1:8000/
   - Tasks: http://127.0.0.1:8000/tasks/

## 📍 URLs

### Authentication
- `/` - Home dashboard (requires login)
- `/login/` - Login page
- `/register/` - Registration page
- `/logout/` - Logout

### Profile
- `/profile/` - View profile
- `/profile/edit/` - Edit profile

### Task Management
- `/tasks/` - View all tasks with stats
- `/tasks/create/` - Create new task (mobile-style form)
- `/tasks/<id>/edit/` - Edit task
- `/tasks/<id>/delete/` - Delete task
- `/tasks/<id>/complete/` - Mark task as completed

### Admin
- `/admin/` - Django admin panel (requires superuser)

## 🎨 UI/UX Features

- **Bottom Navigation**: Easy thumb-friendly navigation between Tasks, Home, and Profile
- **Floating Action Button**: Quick access to create new tasks
- **Stats Cards**: Overview of total, pending, and completed tasks
- **Priority Badges**: Visual priority indicators with emoji
- **Color-Coded Cards**: Tasks have colored left borders based on priority
- **Touch Feedback**: Smooth animations on tap/click
- **Mobile Optimized**: 480px max width, perfect for phone screens
- **Gradient Backgrounds**: Beautiful purple gradient theme

## 💾 Database Structure

### User Model (accounts.User)
- Username
- Name (first_name)
- Age
- Email
- Password (hashed)
- Date joined

### Task Model (tasks.Task)
- User (foreign key)
- Name
- Deadline (datetime)
- Estimated time in minutes (auto-calculated from hours + minutes input)
- Priority (High/Medium/Low)
- Category (optional)
- Status (Pending/In Progress/Completed)
- Scheduled start/end times
- Timestamps (created_at, updated_at)

## 🗄️ Tech Stack

- **Backend**: Django 5.2.7
- **Database**: PostgreSQL
- **Frontend**: HTML5, CSS3 (mobile-first design)
- **Design**: Card-based UI with gradient themes
- **Icons**: Emoji-based (no external dependencies)
