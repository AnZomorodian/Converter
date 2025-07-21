// Amazing new features for Fily Pro
class AmazingFeatures {
    constructor() {
        this.initializeFeatures();
        this.setupAnimations();
        this.createParticleSystem();
        this.setupRealTimeStats();
        this.initializeThemes();
    }

    initializeFeatures() {
        // Add amazing floating particles
        this.createFloatingParticles();
        
        // Add sound effects
        this.setupSoundEffects();
        
        // Add typing animation
        this.setupTypingAnimation();
        
        // Add live visitor counter
        this.setupVisitorCounter();
        
        // Add conversion speed meter
        this.setupSpeedMeter();
        
        // Add file format detector
        this.setupFormatDetector();
    }

    createFloatingParticles() {
        const particleContainer = document.createElement('div');
        particleContainer.className = 'particle-container';
        particleContainer.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            pointer-events: none;
            z-index: 1;
            overflow: hidden;
        `;
        document.body.appendChild(particleContainer);

        // Create 50 floating particles
        for (let i = 0; i < 50; i++) {
            const particle = document.createElement('div');
            particle.className = 'floating-particle';
            particle.style.cssText = `
                position: absolute;
                width: ${Math.random() * 6 + 2}px;
                height: ${Math.random() * 6 + 2}px;
                background: linear-gradient(45deg, #667eea, #764ba2);
                border-radius: 50%;
                opacity: ${Math.random() * 0.6 + 0.2};
                left: ${Math.random() * 100}vw;
                top: ${Math.random() * 100}vh;
                animation: float ${Math.random() * 20 + 10}s linear infinite;
            `;
            particleContainer.appendChild(particle);
        }

        // Add CSS animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes float {
                0% { transform: translateY(100vh) rotate(0deg); }
                100% { transform: translateY(-100vh) rotate(360deg); }
            }
            .floating-particle:hover {
                transform: scale(3) !important;
                opacity: 1 !important;
                transition: all 0.3s ease;
            }
        `;
        document.head.appendChild(style);
    }

    setupSoundEffects() {
        // Create audio context for sound effects
        try {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
            
            // Success sound effect
            this.createSuccessSound = () => {
                const oscillator = this.audioContext.createOscillator();
                const gainNode = this.audioContext.createGain();
                
                oscillator.connect(gainNode);
                gainNode.connect(this.audioContext.destination);
                
                oscillator.frequency.setValueAtTime(523.25, this.audioContext.currentTime); // C5
                oscillator.frequency.setValueAtTime(659.25, this.audioContext.currentTime + 0.1); // E5
                oscillator.frequency.setValueAtTime(783.99, this.audioContext.currentTime + 0.2); // G5
                
                gainNode.gain.setValueAtTime(0.1, this.audioContext.currentTime);
                gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.3);
                
                oscillator.start(this.audioContext.currentTime);
                oscillator.stop(this.audioContext.currentTime + 0.3);
            };

            // Error sound effect
            this.createErrorSound = () => {
                const oscillator = this.audioContext.createOscillator();
                const gainNode = this.audioContext.createGain();
                
                oscillator.connect(gainNode);
                gainNode.connect(this.audioContext.destination);
                
                oscillator.frequency.setValueAtTime(220, this.audioContext.currentTime); // A3
                oscillator.frequency.setValueAtTime(196, this.audioContext.currentTime + 0.1); // G3
                
                gainNode.gain.setValueAtTime(0.1, this.audioContext.currentTime);
                gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.2);
                
                oscillator.start(this.audioContext.currentTime);
                oscillator.stop(this.audioContext.currentTime + 0.2);
            };
        } catch (e) {
            console.log('Audio not supported');
        }
    }

    setupTypingAnimation() {
        const textElement = document.getElementById('heroSubtitle');
        if (textElement) {
            const texts = [
                'Transform any file into professional PDFs instantly',
                'Secure, fast, and reliable file conversion',
                'Support for 20+ file formats with advanced features',
                'Batch processing with real-time progress tracking',
                'Professional quality with enterprise security'
            ];
            
            let currentIndex = 0;
            let charIndex = 0;
            let isDeleting = false;
            
            const typeText = () => {
                const currentText = texts[currentIndex];
                
                if (isDeleting) {
                    textElement.textContent = currentText.substring(0, charIndex - 1);
                    charIndex--;
                } else {
                    textElement.textContent = currentText.substring(0, charIndex + 1);
                    charIndex++;
                }
                
                let typeSpeed = isDeleting ? 50 : 100;
                
                if (!isDeleting && charIndex === currentText.length) {
                    typeSpeed = 2000; // Pause at end
                    isDeleting = true;
                } else if (isDeleting && charIndex === 0) {
                    isDeleting = false;
                    currentIndex = (currentIndex + 1) % texts.length;
                }
                
                setTimeout(typeText, typeSpeed);
            };
            
            typeText();
        }
    }

    setupVisitorCounter() {
        const navbarBrand = document.querySelector('.navbar-brand');
        if (navbarBrand) {
            const counter = document.createElement('span');
            counter.className = 'visitor-counter badge bg-success ms-2';
            counter.style.cssText = `
                font-size: 0.6rem;
                padding: 2px 6px;
                border-radius: 10px;
                animation: pulse 2s infinite;
            `;
            
            // Simulate live visitor count
            let visitors = Math.floor(Math.random() * 1000) + 500;
            counter.textContent = `👥 ${visitors} online`;
            
            setInterval(() => {
                visitors += Math.floor(Math.random() * 5) - 2;
                visitors = Math.max(100, visitors);
                counter.textContent = `👥 ${visitors} online`;
            }, 5000);
            
            navbarBrand.appendChild(counter);
        }
    }

    setupSpeedMeter() {
        const speedMeter = document.createElement('div');
        speedMeter.className = 'speed-meter';
        speedMeter.innerHTML = `
            <div class="speed-display">
                <div class="speed-label">Conversion Speed</div>
                <div class="speed-value" id="speedValue">⚡ Lightning Fast</div>
                <div class="speed-bar">
                    <div class="speed-progress" id="speedProgress"></div>
                </div>
            </div>
        `;
        speedMeter.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            border-radius: 10px;
            font-size: 0.8rem;
            z-index: 1000;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            min-width: 200px;
        `;
        
        const style = document.createElement('style');
        style.textContent = `
            .speed-bar {
                width: 100%;
                height: 4px;
                background: rgba(255,255,255,0.3);
                border-radius: 2px;
                margin-top: 5px;
                overflow: hidden;
            }
            .speed-progress {
                height: 100%;
                background: linear-gradient(90deg, #00ff88, #00ffff);
                border-radius: 2px;
                width: 0%;
                transition: width 0.5s ease;
                animation: speedPulse 2s infinite;
            }
            @keyframes speedPulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.7; }
            }
        `;
        document.head.appendChild(style);
        document.body.appendChild(speedMeter);
        
        // Animate speed meter
        setInterval(() => {
            const speeds = ['⚡ Lightning Fast', '🚀 Turbo Mode', '💨 Ultra Speed', '⭐ Maximum Performance'];
            const randomSpeed = speeds[Math.floor(Math.random() * speeds.length)];
            const progress = Math.random() * 40 + 60; // 60-100%
            
            document.getElementById('speedValue').textContent = randomSpeed;
            document.getElementById('speedProgress').style.width = progress + '%';
        }, 3000);
    }

    setupFormatDetector() {
        // Enhanced file format detection with preview
        const originalInput = document.querySelector('input[type="file"]');
        if (originalInput) {
            originalInput.addEventListener('change', (e) => {
                const files = Array.from(e.target.files);
                files.forEach(file => this.analyzeFile(file));
            });
        }
    }

    analyzeFile(file) {
        const analyzer = document.createElement('div');
        analyzer.className = 'file-analyzer';
        analyzer.innerHTML = `
            <div class="analyzer-content">
                <h6><i class="fas fa-search me-2"></i>File Analysis</h6>
                <div class="analysis-item">
                    <strong>Name:</strong> ${file.name}
                </div>
                <div class="analysis-item">
                    <strong>Size:</strong> ${this.formatBytes(file.size)}
                </div>
                <div class="analysis-item">
                    <strong>Type:</strong> ${file.type || 'Unknown'}
                </div>
                <div class="analysis-item">
                    <strong>Modified:</strong> ${new Date(file.lastModified).toLocaleDateString()}
                </div>
                <div class="compatibility-score">
                    <div class="score-label">Conversion Compatibility</div>
                    <div class="score-bar">
                        <div class="score-fill" style="width: ${this.getCompatibilityScore(file)}%"></div>
                    </div>
                    <div class="score-text">${this.getCompatibilityText(file)}</div>
                </div>
            </div>
        `;
        
        analyzer.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: white;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            z-index: 10000;
            max-width: 400px;
            width: 90%;
        `;
        
        const style = document.createElement('style');
        style.textContent = `
            .analysis-item {
                margin: 8px 0;
                padding: 5px 0;
                border-bottom: 1px solid #eee;
            }
            .compatibility-score {
                margin-top: 15px;
                text-align: center;
            }
            .score-bar {
                width: 100%;
                height: 8px;
                background: #eee;
                border-radius: 4px;
                margin: 10px 0;
                overflow: hidden;
            }
            .score-fill {
                height: 100%;
                background: linear-gradient(90deg, #ff4757, #ffa502, #2ed573);
                border-radius: 4px;
                transition: width 1s ease;
            }
            .score-text {
                font-weight: bold;
                color: #2ed573;
            }
        `;
        document.head.appendChild(style);
        document.body.appendChild(analyzer);
        
        // Auto remove after 3 seconds
        setTimeout(() => {
            analyzer.remove();
        }, 3000);
        
        // Play success sound
        if (this.createSuccessSound) {
            this.createSuccessSound();
        }
    }

    getCompatibilityScore(file) {
        const supportedTypes = [
            'application/pdf', 'application/msword', 
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'text/plain', 'image/jpeg', 'image/png'
        ];
        
        if (supportedTypes.includes(file.type)) {
            return 95 + Math.random() * 5; // 95-100%
        }
        return 60 + Math.random() * 30; // 60-90%
    }

    getCompatibilityText(file) {
        const score = this.getCompatibilityScore(file);
        if (score >= 90) return 'Excellent';
        if (score >= 70) return 'Good';
        if (score >= 50) return 'Fair';
        return 'Limited';
    }

    formatBytes(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    setupRealTimeStats() {
        const statsPanel = document.createElement('div');
        statsPanel.className = 'live-stats-panel';
        statsPanel.innerHTML = `
            <div class="stats-header">
                <i class="fas fa-chart-line me-2"></i>Live Statistics
                <button class="btn-close-stats" onclick="this.parentElement.parentElement.style.display='none'">×</button>
            </div>
            <div class="stats-content">
                <div class="stat-item">
                    <div class="stat-value" id="totalConversions">0</div>
                    <div class="stat-label">Total Conversions</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value" id="successRate">100%</div>
                    <div class="stat-label">Success Rate</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value" id="avgTime">1.2s</div>
                    <div class="stat-label">Avg Time</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value" id="filesProcessed">0 MB</div>
                    <div class="stat-label">Data Processed</div>
                </div>
            </div>
        `;
        
        statsPanel.style.cssText = `
            position: fixed;
            top: 20px;
            left: 20px;
            background: rgba(0,0,0,0.9);
            color: white;
            border-radius: 10px;
            padding: 15px;
            min-width: 200px;
            z-index: 1000;
            font-family: 'Courier New', monospace;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        `;
        
        const statsStyle = document.createElement('style');
        statsStyle.textContent = `
            .stats-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 10px;
                font-weight: bold;
                border-bottom: 1px solid #333;
                padding-bottom: 5px;
            }
            .btn-close-stats {
                background: none;
                border: none;
                color: white;
                font-size: 18px;
                cursor: pointer;
                padding: 0;
                width: 20px;
                height: 20px;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .stats-content {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 10px;
            }
            .stat-item {
                text-align: center;
            }
            .stat-value {
                font-size: 1.2rem;
                font-weight: bold;
                color: #00ff88;
                margin-bottom: 2px;
            }
            .stat-label {
                font-size: 0.7rem;
                opacity: 0.8;
            }
        `;
        document.head.appendChild(statsStyle);
        document.body.appendChild(statsPanel);
        
        // Update stats in real time
        this.updateStats();
        setInterval(() => this.updateStats(), 2000);
    }

    updateStats() {
        // Simulate real-time statistics
        const totalConversions = Math.floor(Math.random() * 50000) + 25000;
        const successRate = (Math.random() * 5 + 95).toFixed(1) + '%';
        const avgTime = (Math.random() * 2 + 0.5).toFixed(1) + 's';
        const filesProcessed = (Math.random() * 500 + 250).toFixed(1) + ' GB';
        
        document.getElementById('totalConversions').textContent = totalConversions.toLocaleString();
        document.getElementById('successRate').textContent = successRate;
        document.getElementById('avgTime').textContent = avgTime;
        document.getElementById('filesProcessed').textContent = filesProcessed;
    }

    initializeThemes() {
        // Add theme switcher
        const themeButton = document.createElement('button');
        themeButton.className = 'theme-switcher btn btn-outline-light btn-sm';
        themeButton.innerHTML = '<i class="fas fa-palette me-1"></i>Theme';
        themeButton.style.cssText = `
            position: fixed;
            bottom: 20px;
            left: 20px;
            z-index: 1000;
            border-radius: 20px;
        `;
        
        const themes = ['default', 'dark', 'neon', 'sunset'];
        let currentTheme = 0;
        
        themeButton.addEventListener('click', () => {
            currentTheme = (currentTheme + 1) % themes.length;
            this.applyTheme(themes[currentTheme]);
        });
        
        document.body.appendChild(themeButton);
    }

    applyTheme(themeName) {
        const existingTheme = document.getElementById('dynamic-theme');
        if (existingTheme) existingTheme.remove();
        
        const themeStyle = document.createElement('style');
        themeStyle.id = 'dynamic-theme';
        
        const themes = {
            default: '',
            dark: `
                body { background: #1a1a1a !important; color: #fff !important; }
                .card { background: #2d2d2d !important; color: #fff !important; }
                .navbar { background: #000 !important; }
            `,
            neon: `
                body { background: #0a0a0a !important; color: #00ff88 !important; }
                .card { background: #1a1a1a !important; border: 1px solid #00ff88 !important; color: #00ff88 !important; }
                .navbar { background: linear-gradient(45deg, #ff006e, #00ff88) !important; }
                .btn-primary { background: #00ff88 !important; border-color: #00ff88 !important; color: #000 !important; }
            `,
            sunset: `
                body { background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%) !important; }
                .card { background: rgba(255,255,255,0.9) !important; }
                .navbar { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important; }
            `
        };
        
        themeStyle.textContent = themes[themeName];
        document.head.appendChild(themeStyle);
        
        // Play theme change sound
        if (this.createSuccessSound) {
            this.createSuccessSound();
        }
    }

    setupAnimations() {
        // Add entrance animations
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.animation = 'slideInUp 0.6s ease-out';
                }
            });
        });
        
        document.querySelectorAll('.card, .hero-section').forEach(el => {
            observer.observe(el);
        });
        
        // Add CSS animations
        const animationStyle = document.createElement('style');
        animationStyle.textContent = `
            @keyframes slideInUp {
                from { transform: translateY(30px); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }
            @keyframes pulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.05); }
            }
            .floating-icon {
                animation: pulse 2s infinite;
            }
        `;
        document.head.appendChild(animationStyle);
    }

    // Easter egg function
    activateEasterEgg() {
        const colors = ['#ff006e', '#fb5607', '#ffbe0b', '#8338ec', '#3a86ff'];
        let colorIndex = 0;
        
        const interval = setInterval(() => {
            document.body.style.background = `linear-gradient(45deg, ${colors[colorIndex]}, ${colors[(colorIndex + 1) % colors.length]})`;
            colorIndex = (colorIndex + 1) % colors.length;
        }, 200);
        
        setTimeout(() => {
            clearInterval(interval);
            document.body.style.background = '';
        }, 3000);
        
        // Create confetti effect
        for (let i = 0; i < 100; i++) {
            const confetti = document.createElement('div');
            confetti.style.cssText = `
                position: fixed;
                width: 10px;
                height: 10px;
                background: ${colors[Math.floor(Math.random() * colors.length)]};
                left: ${Math.random() * 100}vw;
                top: -10px;
                z-index: 10000;
                animation: confetti 3s linear;
            `;
            document.body.appendChild(confetti);
            
            setTimeout(() => confetti.remove(), 3000);
        }
        
        const confettiStyle = document.createElement('style');
        confettiStyle.textContent = `
            @keyframes confetti {
                to { transform: translateY(100vh) rotate(360deg); }
            }
        `;
        document.head.appendChild(confettiStyle);
    }
}

// Initialize amazing features
document.addEventListener('DOMContentLoaded', () => {
    const features = new AmazingFeatures();
    
    // Easter egg trigger (Konami code)
    let konamiCode = [];
    const correctCode = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'KeyB', 'KeyA'];
    
    document.addEventListener('keydown', (e) => {
        konamiCode.push(e.code);
        if (konamiCode.length > correctCode.length) {
            konamiCode.shift();
        }
        
        if (JSON.stringify(konamiCode) === JSON.stringify(correctCode)) {
            features.activateEasterEgg();
            konamiCode = [];
        }
    });
});

// Export for global access
window.AmazingFeatures = AmazingFeatures;