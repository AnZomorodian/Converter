// Advanced copy protection and security features
class ProtectionSystem {
    constructor() {
        this.initializeProtection();
        this.setupEventListeners();
        this.createWarningMessage();
    }

    initializeProtection() {
        // Disable right-click context menu
        document.addEventListener('contextmenu', (e) => {
            e.preventDefault();
            this.showWarning('Right-click is disabled for security!');
            return false;
        });

        // Disable common keyboard shortcuts for copying/saving
        document.addEventListener('keydown', (e) => {
            const forbiddenKeys = [
                // Copy, Cut, Paste
                { ctrl: true, key: 'c' },
                { ctrl: true, key: 'x' },
                { ctrl: true, key: 'v' },
                { ctrl: true, key: 'a' }, // Select all
                // Developer tools
                { key: 'F12' },
                { ctrl: true, shift: true, key: 'I' },
                { ctrl: true, shift: true, key: 'J' },
                { ctrl: true, shift: true, key: 'C' },
                { ctrl: true, key: 'U' }, // View source
                // Save page
                { ctrl: true, key: 's' },
                // Print
                { ctrl: true, key: 'p' },
                // Refresh with cache clear
                { ctrl: true, shift: true, key: 'R' },
                { ctrl: true, key: 'F5' }
            ];

            for (const forbidden of forbiddenKeys) {
                if (this.matchesKeyCombo(e, forbidden)) {
                    e.preventDefault();
                    e.stopPropagation();
                    this.showWarning('This action is disabled for security!');
                    return false;
                }
            }
        });

        // Disable drag and drop
        document.addEventListener('dragstart', (e) => {
            e.preventDefault();
            return false;
        });

        // Disable text selection programmatically
        document.addEventListener('selectstart', (e) => {
            if (!this.isAllowedElement(e.target)) {
                e.preventDefault();
                return false;
            }
        });

        // Disable image saving
        document.addEventListener('dragstart', (e) => {
            if (e.target.tagName === 'IMG') {
                e.preventDefault();
                return false;
            }
        });
    }

    matchesKeyCombo(event, combo) {
        const ctrlMatch = combo.ctrl ? (event.ctrlKey || event.metaKey) : !event.ctrlKey && !event.metaKey;
        const shiftMatch = combo.shift ? event.shiftKey : !event.shiftKey;
        const keyMatch = event.key.toLowerCase() === combo.key.toLowerCase();
        
        return ctrlMatch && shiftMatch && keyMatch;
    }

    isAllowedElement(element) {
        const allowedTags = ['INPUT', 'TEXTAREA'];
        const allowedTypes = ['text', 'password', 'email', 'number', 'search'];
        
        if (allowedTags.includes(element.tagName)) {
            if (element.type && allowedTypes.includes(element.type)) {
                return true;
            }
        }
        
        return element.contentEditable === 'true';
    }

    setupEventListeners() {
        // Monitor for developer tools
        this.detectDevTools();
        
        // Disable printing
        window.addEventListener('beforeprint', (e) => {
            e.preventDefault();
            this.showWarning('Printing is disabled for security!');
            return false;
        });

        // Monitor focus/blur for developer tools detection
        let devToolsOpen = false;
        const threshold = 160;

        setInterval(() => {
            if (window.outerHeight - window.innerHeight > threshold || 
                window.outerWidth - window.innerWidth > threshold) {
                if (!devToolsOpen) {
                    devToolsOpen = true;
                    this.showWarning('Developer tools detected! Please close them.');
                }
            } else {
                devToolsOpen = false;
            }
        }, 500);
    }

    detectDevTools() {
        // Console detection
        let devtools = {open: false, orientation: null};
        const threshold = 160;

        setInterval(() => {
            if (window.outerHeight - window.innerHeight > threshold) {
                devtools.open = true;
                devtools.orientation = 'horizontal';
                this.handleDevToolsDetection();
            } else if (window.outerWidth - window.innerWidth > threshold) {
                devtools.open = true;
                devtools.orientation = 'vertical';
                this.handleDevToolsDetection();
            } else {
                devtools.open = false;
                devtools.orientation = null;
            }
        }, 500);

        // Console debugger detection
        let start = new Date();
        debugger;
        let end = new Date();
        if (end - start > 100) {
            this.handleDevToolsDetection();
        }
    }

    handleDevToolsDetection() {
        this.showWarning('Developer tools detected! This action is monitored.');
        // Could add more sophisticated handling here
    }

    createWarningMessage() {
        const warningDiv = document.createElement('div');
        warningDiv.className = 'copy-warning';
        warningDiv.id = 'copyWarning';
        warningDiv.innerHTML = `
            <div>
                <i class="fas fa-shield-alt fa-2x mb-2"></i>
                <h5>Security Notice</h5>
                <p id="warningText">This action is not allowed!</p>
            </div>
        `;
        document.body.appendChild(warningDiv);
    }

    showWarning(message) {
        const warning = document.getElementById('copyWarning');
        const warningText = document.getElementById('warningText');
        
        if (warning && warningText) {
            warningText.textContent = message;
            warning.classList.add('show');
            
            setTimeout(() => {
                warning.classList.remove('show');
            }, 2000);
        }
    }

    // Advanced protection against common bypass methods
    protectAgainstBypass() {
        // Prevent iframe embedding
        if (window !== window.top) {
            window.top.location = window.location;
        }

        // Clear clipboard periodically
        setInterval(() => {
            if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText('').catch(() => {});
            }
        }, 1000);

        // Monitor for unauthorized access attempts
        window.addEventListener('message', (e) => {
            // Block cross-frame communication
            e.preventDefault();
            e.stopPropagation();
        });
    }

    // Watermark overlay
    addWatermark() {
        const watermark = document.createElement('div');
        watermark.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            pointer-events: none;
            z-index: 9998;
            background-image: repeating-linear-gradient(
                45deg,
                transparent,
                transparent 100px,
                rgba(255,255,255,0.05) 100px,
                rgba(255,255,255,0.05) 120px
            );
        `;
        document.body.appendChild(watermark);
    }

    // Disable zoom functionality
    disableZoom() {
        document.addEventListener('wheel', (e) => {
            if (e.ctrlKey) {
                e.preventDefault();
                this.showWarning('Zoom is disabled!');
            }
        }, { passive: false });

        document.addEventListener('keydown', (e) => {
            if ((e.ctrlKey || e.metaKey) && (e.key === '+' || e.key === '-' || e.key === '0')) {
                e.preventDefault();
                this.showWarning('Zoom shortcuts are disabled!');
            }
        });
    }

    // Initialize all protection features
    enableFullProtection() {
        this.protectAgainstBypass();
        this.addWatermark();
        this.disableZoom();
        
        // Add blur effect when window loses focus (screenshot protection)
        window.addEventListener('blur', () => {
            document.body.style.filter = 'blur(5px)';
        });
        
        window.addEventListener('focus', () => {
            document.body.style.filter = 'none';
        });
    }
}

// Initialize protection system
document.addEventListener('DOMContentLoaded', () => {
    const protection = new ProtectionSystem();
    protection.enableFullProtection();
    
    // Add loading animation for protection setup
    const loadingElement = document.getElementById('protectionLoading');
    if (loadingElement) {
        setTimeout(() => {
            loadingElement.style.display = 'none';
        }, 1000);
    }
});

// Export for global access
window.ProtectionSystem = ProtectionSystem;