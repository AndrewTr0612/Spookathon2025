// 🎃 SpookyMinder - Task Reminder System with Spooky Sound Alerts

class SpookyReminder {
    constructor() {
        this.checkInterval = 60000; // Check every minute
        this.notifiedTasks = new Set(); // Track which tasks we've already notified about
        this.isEnabled = this.getPreference();
        
        // Preload audio files
        this.ghoulSound = new Audio('/static/tasks/sounds/ghoul-ghost-scares-169233.mp3');
        this.ghoulSound.volume = 0.7;
        
        this.init();
    }

    init() {
        // Request notification permission
        if ('Notification' in window && Notification.permission === 'default') {
            Notification.requestPermission();
        }

        // Start checking for reminders
        this.startChecking();

        // Add visibility change handler to check when user returns to tab
        document.addEventListener('visibilitychange', () => {
            if (!document.hidden) {
                this.checkReminders();
            }
        });
    }

    getPreference() {
        const saved = localStorage.getItem('spookyRemindersEnabled');
        return saved === null ? true : saved === 'true';
    }

    setPreference(enabled) {
        this.isEnabled = enabled;
        localStorage.setItem('spookyRemindersEnabled', enabled);
    }

    startChecking() {
        // Check immediately
        this.checkReminders();

        // Then check every minute
        setInterval(() => {
            this.checkReminders();
        }, this.checkInterval);
    }

    async checkReminders() {
        if (!this.isEnabled) return;

        try {
            const response = await fetch('/tasks/api/upcoming/', {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            if (response.ok) {
                const data = await response.json();
                this.processReminders(data.tasks);
            }
        } catch (error) {
            console.error('Failed to fetch reminders:', error);
        }
    }

    processReminders(tasks) {
        tasks.forEach(task => {
            const taskKey = `${task.id}-${task.deadline}`;
            
            // Skip if we've already notified about this task
            if (this.notifiedTasks.has(taskKey)) return;

            const minutesUntil = task.minutes_until;
            
            // Trigger reminders at 30 min, 15 min, 5 min, and when overdue
            if (minutesUntil <= 0) {
                this.showOverdueReminder(task);
                this.notifiedTasks.add(taskKey);
            } else if (minutesUntil <= 5) {
                this.showUrgentReminder(task);
                this.notifiedTasks.add(taskKey);
            } else if (minutesUntil <= 15) {
                this.showWarningReminder(task);
                this.notifiedTasks.add(taskKey);
            } else if (minutesUntil <= 30) {
                this.showNormalReminder(task);
                this.notifiedTasks.add(taskKey);
            }
        });
    }

    showOverdueReminder(task) {
        this.playGhoulSound();
        this.showJumpscare();
        this.showNotification(
            '🚨 OVERDUE TASK!',
            `"${task.name}" is overdue! Complete it now!`,
            'overdue'
        );
        this.showInPageAlert(task, 'overdue', '🚨 OVERDUE!');
    }

    showUrgentReminder(task) {
        this.playGhoulSound();
        this.showJumpscare();
        const mins = task.minutes_until;
        this.showNotification(
            '⚠️ URGENT: Task Due Soon!',
            `"${task.name}" is due in ${mins} minute${mins !== 1 ? 's' : ''}!`,
            'urgent'
        );
        this.showInPageAlert(task, 'urgent', `⚠️ ${mins} min left!`);
    }

    showWarningReminder(task) {
        const mins = task.minutes_until;
        this.showNotification(
            '👻 Task Reminder',
            `"${task.name}" is due in ${mins} minutes`,
            'warning'
        );
        this.showInPageAlert(task, 'warning', `⏰ ${mins} min left`);
    }

    showNormalReminder(task) {
        const mins = task.minutes_until;
        this.showNotification(
            '🎃 Task Reminder',
            `"${task.name}" is due in ${mins} minutes`,
            'normal'
        );
        this.showInPageAlert(task, 'normal', `⏰ ${mins} min left`);
    }

    showNotification(title, body, type) {
        // Browser notification
        if ('Notification' in window && Notification.permission === 'granted') {
            new Notification(title, {
                body: body,
                icon: '/static/accounts/images/ghost-icon.png',
                badge: '/static/accounts/images/ghost-icon.png',
                tag: `task-reminder-${Date.now()}`,
                requireInteraction: type === 'overdue' || type === 'urgent',
                vibrate: type === 'overdue' ? [200, 100, 200, 100, 200] : [200, 100, 200]
            });
        }
    }

    showInPageAlert(task, type, timeText) {
        // Create visual alert on the page
        const alert = document.createElement('div');
        alert.className = `spooky-alert spooky-alert-${type}`;
        alert.innerHTML = `
            <div class="spooky-alert-content">
                <div class="spooky-alert-icon">${this.getIconForType(type)}</div>
                <div class="spooky-alert-text">
                    <strong>${task.name}</strong>
                    <span>${timeText}</span>
                </div>
                <button class="spooky-alert-close" onclick="this.parentElement.parentElement.remove()">✕</button>
            </div>
        `;

        // Add to page
        let container = document.getElementById('spooky-alerts-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'spooky-alerts-container';
            document.body.appendChild(container);
        }

        container.appendChild(alert);

        // Auto-remove after some time (longer for urgent tasks)
        const duration = type === 'overdue' ? 30000 : type === 'urgent' ? 15000 : 10000;
        setTimeout(() => {
            if (alert.parentElement) {
                alert.style.animation = 'slideOut 0.3s ease-out forwards';
                setTimeout(() => alert.remove(), 300);
            }
        }, duration);

        // Animate in
        setTimeout(() => alert.classList.add('show'), 10);
    }

    getIconForType(type) {
        switch(type) {
            case 'overdue': return '🚨';
            case 'urgent': return '⚠️';
            case 'warning': return '👻';
            default: return '🎃';
        }
    }

    playGhoulSound() {
        // Play the ghoul scream sound
        this.ghoulSound.currentTime = 0; // Reset to start
        this.ghoulSound.play().catch(e => console.log('Audio play failed:', e));
    }

    showJumpscare() {
        // Create fullscreen jumpscare overlay
        const jumpscare = document.createElement('div');
        jumpscare.className = 'jumpscare-overlay';
        jumpscare.innerHTML = `
            <img src="/static/tasks/gif/jumpscare.gif" alt="Jumpscare" class="jumpscare-gif">
        `;
        
        document.body.appendChild(jumpscare);
        
        // Remove after 2 seconds
        setTimeout(() => {
            jumpscare.style.opacity = '0';
            setTimeout(() => jumpscare.remove(), 500);
        }, 2000);
    }
}

// Initialize reminder system when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.spookyReminder = new SpookyReminder();
    });
} else {
    window.spookyReminder = new SpookyReminder();
}
