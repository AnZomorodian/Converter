class PDFConverter {
    constructor() {
        this.uploadArea = document.getElementById('uploadArea');
        this.progressArea = document.getElementById('progressArea');
        this.successArea = document.getElementById('successArea');
        this.fileInput = document.getElementById('fileInput');
        this.progressBar = document.getElementById('progressBar');
        this.progressText = document.getElementById('progressText');
        this.fileName = document.getElementById('fileName');
        this.downloadBtn = document.getElementById('downloadBtn');
        this.convertAnotherBtn = document.getElementById('convertAnotherBtn');
        this.uploadCard = document.getElementById('uploadCard');
        
        this.currentFileId = null;
        this.currentFileName = null;
        
        this.initializeEventListeners();
    }
    
    initializeEventListeners() {
        // File input change
        this.fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                this.handleFile(e.target.files[0]);
            }
        });
        
        // Drag and drop events
        this.uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            this.uploadArea.classList.add('dragover');
        });
        
        this.uploadArea.addEventListener('dragleave', (e) => {
            e.preventDefault();
            this.uploadArea.classList.remove('dragover');
        });
        
        this.uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            this.uploadArea.classList.remove('dragover');
            
            if (e.dataTransfer.files.length > 0) {
                this.handleFile(e.dataTransfer.files[0]);
            }
        });
        
        // Click to upload
        this.uploadArea.addEventListener('click', () => {
            this.fileInput.click();
        });
        
        // Download button
        this.downloadBtn.addEventListener('click', () => {
            this.downloadFile();
        });
        
        // Convert another button
        this.convertAnotherBtn.addEventListener('click', () => {
            this.resetInterface();
        });
    }
    
    handleFile(file) {
        // Validate file
        if (!this.validateFile(file)) {
            return;
        }
        
        this.currentFileName = file.name;
        this.fileName.textContent = file.name;
        
        // Show progress area
        this.showProgressArea();
        
        // Upload file
        this.uploadFile(file);
    }
    
    validateFile(file) {
        const allowedTypes = [
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document', // docx
            'application/msword', // doc
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', // xlsx
            'application/vnd.ms-excel', // xls
            'application/vnd.openxmlformats-officedocument.presentationml.presentation', // pptx
            'application/vnd.ms-powerpoint', // ppt
            'image/png',
            'image/jpeg',
            'image/gif',
            'image/bmp',
            'image/tiff',
            'text/plain'
        ];
        
        const allowedExtensions = [
            'docx', 'doc', 'xlsx', 'xls', 'pptx', 'ppt',
            'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'txt'
        ];
        
        const fileExtension = file.name.split('.').pop().toLowerCase();
        
        if (!allowedExtensions.includes(fileExtension)) {
            this.showError('Unsupported file format. Please select a Word, Excel, PowerPoint, image, or text file.');
            return false;
        }
        
        // Check file size (50MB limit)
        const maxSize = 50 * 1024 * 1024; // 50MB
        if (file.size > maxSize) {
            this.showError('File is too large. Maximum size is 50MB.');
            return false;
        }
        
        return true;
    }
    
    async uploadFile(file) {
        try {
            const formData = new FormData();
            formData.append('file', file);
            
            this.updateProgress(25, 'Uploading file...');
            
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            if (!response.ok) {
                throw new Error(result.error || 'Upload failed');
            }
            
            this.currentFileId = result.file_id;
            this.updateProgress(50, 'File uploaded successfully...');
            
            // Start conversion
            setTimeout(() => {
                this.convertFile();
            }, 500);
            
        } catch (error) {
            this.showError('Upload failed: ' + error.message);
            this.resetInterface();
        }
    }
    
    async convertFile() {
        try {
            this.updateProgress(75, 'Converting to PDF...');
            
            const response = await fetch('/convert', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    file_id: this.currentFileId,
                    original_filename: this.currentFileName
                })
            });
            
            const result = await response.json();
            
            if (!response.ok) {
                throw new Error(result.error || 'Conversion failed');
            }
            
            this.updateProgress(100, 'Conversion completed!');
            
            setTimeout(() => {
                this.showSuccessArea();
            }, 1000);
            
        } catch (error) {
            this.showError('Conversion failed: ' + error.message);
            this.resetInterface();
        }
    }
    
    downloadFile() {
        if (this.currentFileId) {
            const downloadUrl = `/download/${this.currentFileId}`;
            const link = document.createElement('a');
            link.href = downloadUrl;
            link.download = `converted_${this.currentFileName.replace(/\.[^/.]+$/, '')}.pdf`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    }
    
    updateProgress(percentage, text) {
        this.progressBar.style.width = percentage + '%';
        this.progressBar.setAttribute('aria-valuenow', percentage);
        this.progressText.textContent = text;
    }
    
    showProgressArea() {
        this.uploadArea.classList.add('d-none');
        this.progressArea.classList.remove('d-none');
        this.progressArea.classList.add('fade-in');
    }
    
    showSuccessArea() {
        this.progressArea.classList.add('d-none');
        this.successArea.classList.remove('d-none');
        this.successArea.classList.add('slide-up');
    }
    
    resetInterface() {
        // Hide all areas
        this.progressArea.classList.add('d-none');
        this.successArea.classList.add('d-none');
        
        // Show upload area
        this.uploadArea.classList.remove('d-none');
        
        // Reset form
        this.fileInput.value = '';
        this.progressBar.style.width = '0%';
        this.progressText.textContent = 'Uploading...';
        
        // Reset state
        this.currentFileId = null;
        this.currentFileName = null;
        
        // Remove animation classes
        this.progressArea.classList.remove('fade-in');
        this.successArea.classList.remove('slide-up');
    }
    
    showError(message) {
        const errorToast = document.getElementById('errorToast');
        const errorMessage = document.getElementById('errorMessage');
        
        errorMessage.textContent = message;
        
        const toast = new bootstrap.Toast(errorToast);
        toast.show();
    }
}

// Initialize the converter when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new PDFConverter();
});

// Add some additional UI enhancements
document.addEventListener('DOMContentLoaded', () => {
    // Add smooth scrolling for better UX
    document.documentElement.style.scrollBehavior = 'smooth';
    
    // Add loading animation to buttons on click
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            if (!this.classList.contains('loading')) {
                this.classList.add('loading');
                setTimeout(() => {
                    this.classList.remove('loading');
                }, 2000);
            }
        });
    });
    
    // Add hover effect to format items
    const formatItems = document.querySelectorAll('.format-item');
    formatItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px) scale(1.05)';
        });
        
        item.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
});
