# 🎃 SPOOKAMINDER Demo Setup Guide

## Quick Start

### Option 1: Automatic Setup (Recommended)
Run the setup script from the project root:
```bash
cd /Users/takeiteasy/Desktop/Spookathon2025/reminderProject
chmod +x setup_demo.sh
./setup_demo.sh
```

### Option 2: Manual Setup
```bash
cd /Users/takeiteasy/Desktop/Spookathon2025/reminderProject/src

# 1. Run migrations
python manage.py makemigrations miniGame
python manage.py migrate

# 2. Create demo user
python manage.py create_demo_user

# 3. Start server
python manage.py runserver
```

## Demo User Credentials
- **Username:** `demo`
- **Password:** `demo123`
- **Tokens:** 200 (ready to use!)

## What's Included

### Demo Tasks
The demo user comes with **12 pre-loaded tasks**:

#### ✅ Completed Tasks (5 tasks)
- 🎃 Decorate for Halloween
- 👻 Watch scary movies
- 🦇 Finish Halloween costume
- 🕷️ Clean the garage
- 🍬 Buy Halloween candy

#### 📋 Pending Tasks (7 tasks)
- 🎭 Attend Halloween party (Tomorrow)
- 📚 Study for Math exam (3 days)
- 🏋️ Hit the gym (Today - 4 hours)
- 🛒 Grocery shopping (2 days)
- 💻 Work on coding project (4 days) - In Progress
- 📧 Reply to important emails (Today - 6 hours)
- 🧹 Deep clean bedroom (5 days)

### Features to Test

#### 🌱 Plant Garden Mini-Game
1. Navigate to the game from:
   - Home page → "Plant Garden" card
   - Tokens page → Green CTA button
   - Direct URL: `/game/`

2. Exchange tokens for water drops:
   - Rate: 5 tokens = 1 water drop
   - **Unlimited purchases per day**
   - Real-time token deduction

3. Water your plant:
   - 5 drops = 1 growth stage
   - Track progress with visual progress bar
   - 5 total growth stages: 🌰 → 🌱 → 🌿 → 🪴 → 🌳

#### 📋 Task Management
1. **View Tasks:**
   - Separated into "Pending" and "Completed" sections
   - Completed tasks shown with strikethrough
   - Color-coded priorities (High/Medium/Low)

2. **Complete Tasks:**
   - Click "✓ Done" button
   - Earn 1 token per completed task
   - Move to completed section automatically

3. **Task Organization:**
   - Pending tasks sorted by deadline (earliest first)
   - Completed tasks sorted by completion date (newest first)

#### 🪙 Token Economy
- Start with 200 tokens
- Earn 1 token per completed task
- Spend 5 tokens per water drop
- View token balance in top-right corner
- Track spending in game statistics

## Navigation

### Main Pages
- **Home** (`/`) - Dashboard with quick actions
- **Tasks** (`/tasks/`) - Task list with pending/completed separation
- **Tokens** (`/tokens/`) - Token stats and game access
- **Plant Garden** (`/game/`) - Mini-game interface
- **Game Stats** (`/game/stats/`) - Transaction history
- **Profile** (`/profile/`) - User account settings

### Key Features
- 🕷️ Spider-web background on all pages
- 🎃 Halloween orange theme (#ff6600)
- 📱 Mobile-responsive design
- 👤 Profile dropdown menu
- 🪙 Token counter always visible

## Testing Scenarios

### Scenario 1: Complete Tasks & Earn Tokens
1. Login as demo user
2. Go to Tasks page
3. Click "✓ Done" on pending tasks
4. Watch token count increase
5. Check completed section

### Scenario 2: Play the Plant Game
1. Go to Plant Garden
2. Buy water drops (5 tokens each)
3. Click "💰 Buy Water Drops"
4. Plant automatically waters and grows
5. Watch progress bar fill up
6. See plant advance through stages

### Scenario 3: Track Your Progress
1. Complete multiple tasks
2. Use tokens in the game
3. View game statistics
4. Check transaction history
5. Monitor plant growth

## Troubleshooting

### If migrations fail:
```bash
python manage.py makemigrations
python manage.py migrate --run-syncdb
```

### If demo user exists:
The command will update the existing demo user to 200 tokens and refresh tasks.

### If game doesn't show plant:
The game uses emoji fallbacks if images aren't found. This is expected and fully functional.

## Important Notes

✅ **Unlimited Token Redemption:** No daily limits on buying water drops
✅ **Task Filtering:** Completed tasks are clearly separated
✅ **Token Persistence:** Tokens persist across sessions
✅ **Real-time Updates:** All counters update immediately

## Next Steps After Setup

1. **Login** with demo credentials
2. **Complete** a few pending tasks to earn tokens
3. **Visit** the Plant Garden game
4. **Buy** water drops with your tokens
5. **Watch** your plant grow!

---

**Happy Testing! 🎃👻🌱**
