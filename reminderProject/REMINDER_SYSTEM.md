# 🔔 SpookyMinder Reminder System with Spooky Sound Alarms

## 🎃 Features

Your SpookyMinder now has an **automatic reminder system** with **spooky sound effects** that alerts you when tasks are approaching their deadline!

### 🔊 Four Levels of Spooky Alarms

1. **🎃 Normal Reminder (30 minutes before)**
   - Soft whisper sound effect
   - Gentle orange notification
   - In-page alert banner

2. **👻 Warning Reminder (15 minutes before)**
   - Eerie ghost "whoosh" sound
   - Yellow-orange alert
   - Browser notification (if permitted)

3. **⚠️ Urgent Reminder (5 minutes before)**
   - Ominous bell toll sound (2 chimes)
   - Bright orange pulsing alert
   - Persistent notification

4. **🚨 OVERDUE Alert (after deadline)**
   - Loud alarm scream sound
   - Red flashing alert with shake animation
   - Continuous alerts until completed

### 🎵 Sound Effects

All sound effects are generated procedurally using Web Audio API:
- **Whisper**: Subtle 300Hz sine wave
- **Ghost Whoosh**: Descending sawtooth wave (200Hz → 50Hz)
- **Bell Toll**: Classic 440Hz sine with decay
- **Scream**: Rapid frequency sweep (800Hz → 1200Hz)

### 📱 Features

- ✅ **Browser Notifications**: Desktop & mobile push notifications
- ✅ **Visual In-Page Alerts**: Beautiful animated banners
- ✅ **Auto-Check**: Checks every 60 seconds automatically
- ✅ **Smart Tracking**: Won't spam you with duplicate reminders
- ✅ **Toggle Control**: Enable/disable with 🔔/🔕 button
- ✅ **Persistent Preference**: Remembers your setting
- ✅ **Responsive Design**: Works on all screen sizes

## 🚀 How to Use

### 1. Enable Browser Notifications

When you first load the task list page, you'll be asked:
```
"SpookyMinder wants to send you notifications"
```
Click **Allow** to enable desktop/mobile notifications!

### 2. The Reminder Toggle Button

Look for the **🔔 bell button** in the bottom-right corner:
- **🔔 = Reminders Enabled** (orange glow)
- **🔕 = Reminders Disabled** (gray, faded)

Click it to toggle reminders on/off at any time!

### 3. When Reminders Trigger

Reminders will automatically trigger at these intervals:

| Time Until Deadline | Sound | Alert Type | Style |
|---------------------|-------|------------|-------|
| 30 minutes | Whisper 🎃 | Normal | Orange border |
| 15 minutes | Ghost Whoosh 👻 | Warning | Yellow-orange + pulse |
| 5 minutes | Bell Toll ⚠️ | Urgent | Bright orange + pulse |
| After deadline | Scream 🚨 | OVERDUE | Red + shake animation |

### 4. Visual Alerts

In-page alerts appear in the top-right corner with:
- Task name
- Time remaining/overdue
- Animated entrance
- Auto-dismiss (or click ✕ to close)
- Priority-based colors

## 🎨 Alert Styles

### Normal Alert (30 min)
```
Background: Gradient from orange to dark purple
Border: #ff6600 (orange)
Animation: Gentle pulse
```

### Warning Alert (15 min)
```
Background: Gradient from yellow-orange to dark purple
Border: #ffa726 (light orange)
Animation: Medium pulse
```

### Urgent Alert (5 min)
```
Background: Gradient from bright orange to dark purple
Border: #ff9800 (orange)
Animation: Strong pulse + scaling
```

### Overdue Alert
```
Background: Gradient from red to dark purple
Border: #ff1744 (red)
Animation: Rapid pulse + shake effect
```

## 🔧 Technical Details

### Files Created

1. **`tasks/static/tasks/js/reminders.js`**
   - Main reminder system logic
   - Sound generation using Web Audio API
   - API polling and notification display

2. **`tasks/static/tasks/css/reminders.css`**
   - Visual alert styling
   - Animations and transitions
   - Responsive design

3. **API Endpoint**: `/tasks/api/upcoming/`
   - Returns tasks due within 1 hour
   - Returns overdue tasks
   - JSON response with task details

### How It Works

```
1. Page loads → Initialize SpookyReminder class
2. Request notification permission
3. Start checking loop (every 60 seconds)
4. Fetch upcoming tasks from API
5. Calculate time until deadline
6. Trigger appropriate reminder level
7. Play sound + show notification + display alert
8. Track notified tasks (avoid duplicates)
```

### Browser Compatibility

- ✅ Chrome/Edge (full support)
- ✅ Firefox (full support)
- ✅ Safari (full support)
- ✅ Mobile browsers (notifications may vary)

### Permission Requirements

- **Notification API**: For desktop/mobile notifications
- **Web Audio API**: For sound generation (no permission needed)
- **LocalStorage**: To save reminder preference

## 🎮 User Experience

### First Visit
1. User loads task list page
2. Browser asks for notification permission
3. User clicks "Allow"
4. Reminders are now active!

### Creating a Task with Deadline
1. Create task with deadline "Today, 3:00 PM"
2. Current time: 2:25 PM
3. At 2:30 PM → Normal reminder (whisper)
4. At 2:45 PM → Warning reminder (ghost)
5. At 2:55 PM → Urgent reminder (bell)
6. At 3:01 PM → OVERDUE alert (scream)

### Toggling Reminders
- Click 🔔 button → Changes to 🔕 (disabled)
- Click 🔕 button → Changes to 🔔 (enabled)
- Preference saved in browser
- Works immediately (no page reload)

## 📊 API Response Format

```json
{
  "tasks": [
    {
      "id": 1,
      "name": "🏋️ Hit the gym",
      "deadline": "2025-10-29T16:00:00-07:00",
      "priority": "Medium",
      "minutes_until": 15,
      "is_overdue": false
    },
    {
      "id": 2,
      "name": "📧 Reply to emails",
      "deadline": "2025-10-29T14:00:00-07:00",
      "priority": "High",
      "minutes_until": -30,
      "is_overdue": true
    }
  ]
}
```

## 🎉 Benefits

1. **Never Miss a Deadline**: Multi-level alerts ensure you're always aware
2. **Spooky Theme**: Sound effects match Halloween aesthetic
3. **Non-Intrusive**: Smart tracking prevents notification spam
4. **User Control**: Easy toggle on/off
5. **Mobile-Friendly**: Works on all devices
6. **Offline-Safe**: Gracefully handles network errors

## 🛠️ Customization

Want to adjust the reminder intervals? Edit `reminders.js`:

```javascript
// Current thresholds (in processReminders method)
if (minutesUntil <= 0) {
    this.showOverdueReminder(task);  // Overdue
} else if (minutesUntil <= 5) {
    this.showUrgentReminder(task);   // 5 minutes
} else if (minutesUntil <= 15) {
    this.showWarningReminder(task);  // 15 minutes
} else if (minutesUntil <= 30) {
    this.showNormalReminder(task);   // 30 minutes
}
```

Change the numbers to your preference!

## 🐛 Troubleshooting

### Not Getting Notifications?
1. Check browser notification permission
2. Make sure reminders are enabled (🔔 not 🔕)
3. Check if task has deadline within 1 hour
4. Look at browser console for errors

### Sounds Not Playing?
1. Check if audio is muted in browser
2. Try clicking anywhere on page first (some browsers require user interaction)
3. Check browser console for Web Audio API errors

### Alerts Not Showing?
1. Check if reminders are enabled
2. Clear browser cache and reload
3. Make sure CSS file is loaded (check Network tab)

## 🎃 Enjoy Your Spooky Reminders!

Your SpookyMinder now has a fully functional reminder system with atmospheric Halloween sound effects. Never miss a deadline again! 👻🔔
