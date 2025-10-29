// 🎃 SpookyMinder - Background Music Controller

class BackgroundMusicController {
    constructor() {
        // Use existing audio element if available, otherwise create new one
        this.audio = document.getElementById('bgMusic') || new Audio('/static/sounds/scary-music-box-165983.mp3');
        this.audio.loop = true;
        this.audio.volume = 0.3; // Set volume to 30% so it's ambient
        
        // Get preference and restore playback position
        this.isPlaying = this.getPreference();
        this.restorePlaybackState();
        
        this.init();
    }

    init() {
        // Create music control button first
        this.createControlButton();
        
        // If user previously disabled it, pause the audio
        if (!this.isPlaying) {
            this.audio.pause();
            this.updateButton();
            return;
        }
        
        // Try to play immediately (will work with HTML audio autoplay)
        this.audio.play().then(() => {
            console.log('Music started automatically');
            this.updateButton();
            this.savePlaybackState();
        }).catch(error => {
            console.log('Autoplay blocked, waiting for user interaction');
            // Set up listeners for ANY user interaction to start music
            this.setupAutoplayListeners();
        });
        
        // Save playback position periodically
        this.audio.addEventListener('timeupdate', () => {
            if (this.isPlaying && !this.audio.paused) {
                this.savePlaybackState();
            }
        });
        
        // Save state before page unload
        window.addEventListener('beforeunload', () => {
            this.savePlaybackState();
        });
    }

    setupAutoplayListeners() {
        const startMusic = () => {
            if (this.isPlaying && this.audio.paused) {
                this.audio.play().then(() => {
                    console.log('Music started after user interaction');
                    this.updateButton();
                    this.savePlaybackState();
                }).catch(e => console.log('Still cannot play:', e));
            }
            // Remove all listeners after first successful play
            document.removeEventListener('click', startMusic, true);
            document.removeEventListener('keydown', startMusic, true);
            document.removeEventListener('touchstart', startMusic, true);
            document.removeEventListener('scroll', startMusic, true);
            document.removeEventListener('mousemove', startMusic, true);
        };
        
        // Attach to multiple interaction types with capture phase
        document.addEventListener('click', startMusic, true);
        document.addEventListener('keydown', startMusic, true);
        document.addEventListener('touchstart', startMusic, true);
        document.addEventListener('scroll', startMusic, true);
        document.addEventListener('mousemove', startMusic, true);
    }

    getPreference() {
        const saved = localStorage.getItem('backgroundMusicEnabled');
        return saved === null ? true : saved === 'true'; // Default to ON (true)
    }

    setPreference(enabled) {
        this.isPlaying = enabled;
        localStorage.setItem('backgroundMusicEnabled', enabled);
    }

    savePlaybackState() {
        if (!this.audio.paused && this.audio.currentTime > 0) {
            sessionStorage.setItem('musicCurrentTime', this.audio.currentTime.toString());
            sessionStorage.setItem('musicIsPlaying', 'true');
        }
    }

    restorePlaybackState() {
        const savedTime = sessionStorage.getItem('musicCurrentTime');
        const wasPlaying = sessionStorage.getItem('musicIsPlaying');
        
        if (savedTime && wasPlaying === 'true' && this.isPlaying) {
            this.audio.currentTime = parseFloat(savedTime);
            console.log('Restored playback position:', savedTime);
        }
    }

    play() {
        // Modern browsers require user interaction before playing audio
        this.audio.play().catch(error => {
            console.log('Autoplay prevented. User interaction required.');
            this.isPlaying = false;
            this.updateButton();
        });
    }

    pause() {
        this.audio.pause();
    }

    toggle() {
        if (this.isPlaying) {
            this.pause();
            this.isPlaying = false;
            sessionStorage.removeItem('musicIsPlaying');
        } else {
            this.play();
            this.isPlaying = true;
            this.savePlaybackState();
        }
        this.setPreference(this.isPlaying);
        this.updateButton();
    }

    createControlButton() {
        // Check if button already exists
        if (document.getElementById('musicToggle')) return;

        const button = document.createElement('button');
        button.id = 'musicToggle';
        button.className = 'music-toggle';
        button.title = this.isPlaying ? 'Pause Background Music' : 'Play Background Music';
        button.textContent = this.isPlaying ? '🎵' : '🔇';
        
        if (!this.isPlaying) {
            button.classList.add('disabled');
        }

        button.addEventListener('click', () => {
            this.toggle();
        });

        document.body.appendChild(button);
    }

    updateButton() {
        const button = document.getElementById('musicToggle');
        if (button) {
            if (this.isPlaying) {
                button.textContent = '🎵';
                button.title = 'Pause Background Music';
                button.classList.remove('disabled');
            } else {
                button.textContent = '🔇';
                button.title = 'Play Background Music';
                button.classList.add('disabled');
            }
        }
    }
}

// Initialize background music when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.backgroundMusic = new BackgroundMusicController();
    });
} else {
    window.backgroundMusic = new BackgroundMusicController();
}
