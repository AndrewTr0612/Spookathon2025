# Reminder Project

A Django web application with user authentication system that stores user name and age.

## Features

- ✅ User registration with name and age
- ✅ User login/logout functionality
- ✅ Beautiful gradient UI design
- ✅ Protected home page displaying user information

## Quick Start

1. **Delete existing database and apply migrations**:
   ```bash
   cd src
   rm db.sqlite3  # Only if you have an existing database
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

## URLs

- `/` - Home page (requires login)
- `/login/` - Login page
- `/register/` - Registration page
- `/logout/` - Logout
- `/admin/` - Django admin (requires superuser)
