# 🎃 SpookyMinder - Background Music & Enhanced Reminders

## 🎵 New Features Implemented

### 1. **Background Music (Scary Music Box)**
- **File**: `scary-music-box-165983.mp3`
- **Location**: `/static/sounds/`
- **Plays**: Continuously on loop at 30% volume
- **Control**: Purple music button (🎵/🔇) in bottom-left corner
- **Preference**: Saved in browser localStorage
- **Auto-disabled**: If browser blocks autoplay

### 2. **Enhanced Reminders with Ghoul Sound & Jumpscare**
- **Ghoul Sound**: `ghoul-ghost-scares-169233.mp3` plays for urgent/overdue tasks
- **Jumpscare GIF**: Full-screen animated GIF appears with sound
- **Trigger**: 5 minutes before deadline & overdue tasks

## 🎬 Jumpscare Effect

When a task is **5 minutes away** or **overdue**:

1. 🔊 **Ghoul scream sound** plays (loud!)
2. 📺 **Full-screen flash** (white → black)
3. 🎃 **Jumpscare GIF** appears (scales in with rotation)
4. ⏱️ **Displays for 2 seconds** then fades out
5. 🚨 **Alert banner** shows in top-right

### Visual Sequence:
```
Normal browsing → Sound plays → Screen flashes white → 
GIF appears (scaling + rotating) → Holds 2 seconds → 
Fades to black → Returns to normal + alert banner
```

## 🎮 User Controls

### Background Music Toggle (Bottom-Left)
- **🎵 = Playing** (purple glow, pulsing)
- **🔇 = Paused** (gray, no animation)
- Click to toggle on/off
- Preference saved across sessions

### Reminder Toggle (Top-Right)
- **🔔 = Enabled** (orange glow)
- **🔕 = Disabled** (gray)
- Click to toggle on/off
- Preference saved across sessions

## 📁 Files Created/Modified

### New Files:
1. **`/static/sounds/scary-music-box-165983.mp3`** - Background music
2. **`/static/js/background-music.js`** - Music controller
3. **`/static/css/background-music.css`** - Music button styling
4. **`/tasks/static/tasks/sounds/ghoul-ghost-scares-169233.mp3`** - Reminder sound
5. **`/tasks/static/tasks/gif/jumpscare.gif`** - Jumpscare animation

### Modified Files:
1. **`tasks/static/tasks/js/reminders.js`**
   - Removed Web Audio API sound generation
   - Added real MP3 audio playback
   - Added jumpscare overlay function
   - Ghoul sound plays for urgent/overdue only

2. **`tasks/static/tasks/css/reminders.css`**
   - Added `.jumpscare-overlay` styles
   - Added `.jumpscare-gif` animations
   - Flash and scale animations

3. **`myproject/settings.py`**
   - Added `STATICFILES_DIRS = [BASE_DIR / 'static']`

4. **Templates (added music + CSS)**:
   - `tasks/templates/tasks/task_list.html`
   - `accounts/templates/accounts/home.html`
   - `miniGame/templates/miniGame/game.html`

## 🎯 Reminder Behavior

| Time Until Deadline | Sound | Jumpscare | Alert Style |
|---------------------|-------|-----------|-------------|
| 30 minutes | ❌ None | ❌ No | 🎃 Normal (orange) |
| 15 minutes | ❌ None | ❌ No | 👻 Warning (yellow-orange) |
| 5 minutes | ✅ Ghoul | ✅ Yes | ⚠️ Urgent (bright orange + pulse) |
| Overdue | ✅ Ghoul | ✅ Yes | 🚨 Critical (red + shake) |

## 🎨 Styling Details

### Music Button (Bottom-Left)
```css
Position: fixed, bottom: 100px, left: 20px
Colors: Purple gradient (#9c27b0 → #673ab7)
Size: 48px × 48px
Animation: Gentle pulse when playing
```

### Jumpscare Overlay
```css
Position: fixed fullscreen (z-index: 99999)
Background: Black with 95% opacity
Flash animation: White → Black (0.2s)
GIF animation: Scale 0.5 → 1.1 → 1.0 with rotation
Duration: 2 seconds, then fade out
```

### Reminder Button (Top-Right)
```css
Position: fixed, top: 80px, right: 20px
Colors: Orange gradient (#ff6600 → #ff4400)
Size: 48px × 48px
```

## 🔧 Technical Details

### Background Music Controller
```javascript
- Audio loop: true
- Volume: 0.3 (30%)
- Autoplay: Requires user interaction (browser policy)
- localStorage key: 'backgroundMusicEnabled'
```

### Ghoul Sound
```javascript
- Preloaded on page load
- Volume: 0.7 (70%)
- Triggered: 5 min before & overdue
- Reset to start on each trigger
```

### Jumpscare Sequence
```javascript
1. Play ghoul sound
2. Create overlay div
3. Insert GIF image
4. Flash animation (0.2s)
5. Hold for 2 seconds
6. Fade out (0.5s)
7. Remove from DOM
```

## 📱 Mobile Responsive

- Music button: 44px on mobile, left: 16px, bottom: 90px
- Reminder button: 44px on mobile, right: 16px, top: 70px
- Jumpscare GIF: max-width: 90%, max-height: 90%
- All buttons scale properly on small screens

## 🎃 User Experience Flow

### First Visit:
1. User opens website
2. Music button appears (🔇 gray, paused)
3. User clicks → Music starts playing (🎵 purple, pulsing)
4. Music continues across all pages
5. Preference saved in browser

### Task Reminder:
1. Task deadline approaching (5 min)
2. Ghoul scream sound plays
3. Screen flashes white
4. Jumpscare GIF appears with scaling animation
5. Holds for 2 seconds
6. Fades out
7. Alert banner shows in top-right
8. Browser notification sent

### Toggling Music:
- **Playing → Click → Paused**: Music stops, button grays out
- **Paused → Click → Playing**: Music resumes, button glows purple
- Setting persists across page navigation

## 🐛 Error Handling

- **Autoplay blocked**: Music button defaults to paused, user must click
- **Audio load fail**: Console log, button remains functional
- **Missing files**: Graceful fallback, no crashes
- **Browser compatibility**: Works on all modern browsers

## ✨ Animation Details

### Flash In (Jumpscare)
```
0%: opacity 0, white background
50%: white background 80%
100%: opacity 1, black background 95%
```

### Scale Jumpscare (GIF)
```
0%: scale(0.5), rotate(-5deg), opacity 0
50%: scale(1.1), rotate(2deg)
100%: scale(1), rotate(0), opacity 1
```

### Music Pulse
```
0%/100%: Normal shadow
50%: Enhanced purple glow shadow
```

## 🎉 Result

Your SpookyMinder now has:
- ✅ Creepy background music playing throughout the site
- ✅ Jump-scare alerts with ghoul screams for urgent tasks
- ✅ Full-screen animated GIF for maximum spook factor
- ✅ User controls for both features
- ✅ Smooth animations and transitions
- ✅ Mobile-responsive design
- ✅ Saved preferences

**Perfect for a Halloween-themed task manager! 👻🎃**
