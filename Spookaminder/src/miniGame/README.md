# Plant Watering Mini-Game

## Overview
A token-based plant growing game integrated with the SPOOKAMINDER task management system.

## Game Mechanics

### Token Economy
- **Earn Tokens**: Complete tasks to earn 1 token per task
- **Exchange Rate**: 5 tokens = 1 water drop

### Plant Growth
- **5 Growth Stages**:
  1. 🌰 Seed
  2. 🌱 Sprout
  3. 🌿 Seedling
  4. 🪴 Young Plant
  5. 🌳 Mature Plant

- **Growth Progression**: Each water drop adds 20% progress to the current stage
- **Stage Advancement**: Requires 5 water drops (100% progress) to reach the next stage

### How to Play
1. Complete tasks in SPOOKAMINDER to earn tokens
2. Visit the Plant Garden at `/game/`
3. Exchange tokens for water drops
4. Water your plant to help it grow
5. Track your progress and transaction history

## File Structure

```
miniGame/
├── models.py          # Plant and WaterTransaction models
├── views.py           # Game logic and views
├── urls.py            # URL routing
├── admin.py           # Django admin configuration
├── templates/
│   └── miniGame/
│       ├── game.html       # Main game interface
│       ├── water.html      # Watering interface
│       └── stats.html      # Statistics page
├── static/
│   └── miniGame/
│       ├── css/
│       │   └── game.css    # Game styling
│       └── images/
│           ├── plant_stage_1.png  # Seed image
│           ├── plant_stage_2.png  # Sprout image
│           ├── plant_stage_3.png  # Seedling image
│           ├── plant_stage_4.png  # Young plant image
│           └── plant_stage_5.png  # Mature plant image
```

## Setup Instructions

### 1. Make Migrations
```bash
cd /Users/takeiteasy/Desktop/Spookathon2025/reminderProject/src
python manage.py makemigrations miniGame
python manage.py migrate
```

### 2. Add Plant Images
Place your custom plant images in:
`miniGame/static/miniGame/images/`

Name them:
- `plant_stage_1.png` (Seed)
- `plant_stage_2.png` (Sprout)
- `plant_stage_3.png` (Seedling)
- `plant_stage_4.png` (Young Plant)
- `plant_stage_5.png` (Mature Plant)

**Note**: The game will fallback to emoji icons (🌰🌱🌿🪴🌳) if images are not found.

### 3. Access the Game
- Navigate to: `http://localhost:8000/game/`
- Or click the "🎮 Plant Garden" button from any page

## Database Schema

### Plant Model
- `user`: OneToOne relationship with User
- `growth_stage`: Integer (1-5)
- `water_drops`: Total water drops used
- `water_progress`: Progress percentage (0-100)
- `created_at`: Timestamp
- `updated_at`: Timestamp

### WaterTransaction Model
- `user`: ForeignKey to User
- `tokens_spent`: Number of tokens exchanged
- `water_drops_received`: Number of drops purchased
- `timestamp`: Transaction time

## Features

### User Interface
- **Consistent Halloween Theme**: Spider-web background, orange (#ff6600) accent colors
- **Real-time Progress Bar**: Visual feedback on plant growth
- **Token Display**: Current token balance always visible
- **Transaction History**: Track all water drop purchases
- **Responsive Design**: Mobile-optimized interface

### Game Logic
- **Atomic Transactions**: Token deduction and water purchases are atomic
- **Validation**: Ensures users have sufficient tokens before purchase
- **Progress Calculation**: Automatic stage advancement at 100% progress
- **Statistics Tracking**: Comprehensive game statistics

## Admin Panel
Access the Django admin panel to:
- View all plants and their growth stages
- Monitor water transactions
- Filter by growth stage, date, user
- Search for specific users

Admin URL: `http://localhost:8000/admin/`

## Integration Points

### Navigation
The game is integrated into the main navigation:
- Bottom navigation bar: "🎮 Game" link
- Token button: Links to tokens page showing game connection

### Token System
- Seamlessly uses existing token system from User model
- Real-time token balance updates
- Prevents purchases with insufficient tokens

## Future Enhancements Ideas
- Add achievements/badges for milestones
- Introduce plant varieties
- Add seasonal events
- Implement plant decay if not watered
- Add multiplayer garden features
- Create token multipliers for streak completions
