#!/bin/bash

# Setup script for SPOOKAMINDER demo

echo "🎃 Setting up SPOOKAMINDER Demo..."
echo "=================================="

# Navigate to project directory
cd /Users/takeiteasy/Desktop/Spookathon2025/reminderProject/src

# Run migrations for miniGame
echo ""
echo "📦 Creating database migrations..."
python manage.py makemigrations miniGame
python manage.py migrate

# Create demo user
echo ""
echo "👻 Creating demo user with tasks..."
python manage.py create_demo_user

echo ""
echo "=================================="
echo "✅ Setup complete!"
echo ""
echo "🎮 You can now:"
echo "   1. Start the server: python manage.py runserver"
echo "   2. Login with:"
echo "      Username: demo"
echo "      Password: demo123"
echo "   3. The demo user has 200 tokens ready to use!"
echo ""
