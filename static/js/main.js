class PDFConverter {
    constructor() {
        this.uploadArea = document.getElementById('uploadArea');
        this.progressArea = document.getElementById('progressArea');
        this.optionsArea = document.getElementById('optionsArea');
        this.successArea = document.getElementById('successArea');
        this.fileInput = document.getElementById('fileInput');
        this.batchFileInput = document.getElementById('batchFileInput');
        this.progressBar = document.getElementById('progressBar');
        this.progressText = document.getElementById('progressText');
        this.fileName = document.getElementById('fileName');
        this.downloadBtn = document.getElementById('downloadBtn');
        this.convertAnotherBtn = document.getElementById('convertAnotherBtn');
        this.startConversionBtn = document.getElementById('startConversionBtn');
        this.qualitySelect = document.getElementById('qualitySelect');
        this.passwordInput = document.getElementById('passwordInput');
        this.outputNameInput = document.getElementById('outputNameInput');
        this.uploadCard = document.getElementById('uploadCard');
        this.refreshHistoryBtn = document.getElementById('refreshHistoryBtn');
        this.historyList = document.getElementById('historyList');
        this.previewContainer = document.getElementById('previewContainer');
        this.previewContent = document.getElementById('previewContent');
        
        this.currentFileId = null;
        this.currentFileName = null;
        this.batchFiles = [];
        
        this.initializeEventListeners();
        
        // Load conversion history after a short delay to ensure all elements are ready
        setTimeout(() => {
            this.loadConversionHistory();
        }, 100);
    }
    
    initializeEventListeners() {
        // File input change
        this.fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                this.handleFile(e.target.files[0]);
            }
        });
        
        // Batch file input change
        this.batchFileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                this.handleBatchFiles(Array.from(e.target.files));
            }
        });
        
        // Enhanced drag and drop events
        this.uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            e.stopPropagation();
            this.uploadArea.classList.add('dragover');
        });
        
        this.uploadArea.addEventListener('dragenter', (e) => {
            e.preventDefault();
            e.stopPropagation();
            this.uploadArea.classList.add('dragover');
        });
        
        this.uploadArea.addEventListener('dragleave', (e) => {
            e.preventDefault();
            e.stopPropagation();
            // Only remove dragover if we're leaving the upload area entirely
            if (!this.uploadArea.contains(e.relatedTarget)) {
                this.uploadArea.classList.remove('dragover');
            }
        });
        
        this.uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            e.stopPropagation();
            this.uploadArea.classList.remove('dragover');
            
            const files = Array.from(e.dataTransfer.files);
            if (files.length > 1) {
                this.handleBatchFiles(files);
            } else if (files.length === 1) {
                this.handleFile(files[0]);
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
        
        // Start conversion button
        this.startConversionBtn.addEventListener('click', () => {
            this.convertFile();
        });
        
        // Refresh history button
        this.refreshHistoryBtn.addEventListener('click', () => {
            this.loadConversionHistory();
        });
    }
    
    handleFile(file) {
        // Validate file
        if (!this.validateFile(file)) {
            return;
        }
        
        this.currentFileName = file.name;
        this.fileName.textContent = file.name;
        
        // Show options area first
        this.showOptionsArea();
        
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
            'text/plain',
            'text/csv',
            'application/pdf',
            'application/rtf',
            'application/vnd.oasis.opendocument.text',
            'application/vnd.oasis.opendocument.spreadsheet',
            'application/vnd.oasis.opendocument.presentation'
        ];
        
        const allowedExtensions = [
            'docx', 'doc', 'xlsx', 'xls', 'pptx', 'ppt',
            'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'txt',
            'csv', 'pdf', 'rtf', 'odt', 'ods', 'odp',
            'html', 'htm', 'xml', 'json', 'md', 'py', 'js', 'css'
        ];
        
        const fileExtension = file.name.split('.').pop().toLowerCase();
        
        if (!allowedExtensions.includes(fileExtension)) {
            this.showError(`Unsupported file format: .${fileExtension}. Supported formats: DOC, DOCX, XLS, XLSX, PPT, PPTX, PNG, JPG, TXT, CSV, PDF, HTML, JSON, MD, PY, JS, CSS and more.`);
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
            this.updateProgress(100, 'File uploaded successfully! Configure options and convert.');
            
            // Auto-populate output name with original filename
            if (this.currentFileName) {
                const nameWithoutExt = this.currentFileName.replace(/\.[^/.]+$/, '');
                this.outputNameInput.value = nameWithoutExt;
            }
            
            // Show options instead of auto-converting
            this.showOptionsArea();
            
        } catch (error) {
            this.showError('Upload failed: ' + error.message);
            this.resetInterface();
        }
    }
    
    async convertFile() {
        try {
            this.showProgressArea();
            this.updateProgress(75, 'Converting to PDF...');
            
            const response = await fetch('/convert', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    file_id: this.currentFileId,
                    original_filename: this.currentFileName,
                    password: this.passwordInput.value || null,
                    quality: this.qualitySelect.value,
                    output_name: this.outputNameInput.value || null
                })
            });
            
            const result = await response.json();
            
            if (!response.ok) {
                throw new Error(result.error || 'Conversion failed');
            }
            
            this.updateProgress(100, 'Conversion completed!');
            
            // Load preview if available
            this.loadPreview();
            
            setTimeout(() => {
                this.showSuccessArea();
                this.loadConversionHistory(); // Refresh history
            }, 1000);
            
        } catch (error) {
            this.showError('Conversion failed: ' + error.message);
            this.resetInterface();
        }
    }
    
    async handleBatchFiles(files) {
        try {
            this.showProgressArea();
            this.updateProgress(25, 'Uploading batch files...');
            
            const formData = new FormData();
            files.forEach(file => {
                formData.append('files', file);
            });
            
            const response = await fetch('/batch-upload', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            if (!response.ok) {
                throw new Error(result.error || 'Batch upload failed');
            }
            
            this.batchFiles = result.files;
            this.updateProgress(100, `${result.files.length} files uploaded successfully!`);
            
            // Start batch conversion
            setTimeout(() => {
                this.processBatchConversion();
            }, 1000);
            
        } catch (error) {
            this.showError('Batch upload failed: ' + error.message);
            this.resetInterface();
        }
    }
    
    async processBatchConversion() {
        let completed = 0;
        const total = this.batchFiles.length;
        
        for (const fileInfo of this.batchFiles) {
            try {
                this.updateProgress((completed / total) * 100, `Converting ${fileInfo.original_filename}...`);
                
                const response = await fetch('/convert', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        file_id: fileInfo.file_id,
                        original_filename: fileInfo.original_filename,
                        quality: this.qualitySelect.value
                    })
                });
                
                completed++;
                
            } catch (error) {
                console.error(`Failed to convert ${fileInfo.original_filename}:`, error);
            }
        }
        
        this.updateProgress(100, `Batch conversion completed! ${completed}/${total} files converted.`);
        this.loadConversionHistory();
        
        setTimeout(() => {
            this.showSuccessArea();
        }, 1000);
    }
    
    async loadPreview() {
        if (!this.currentFileId) return;
        
        try {
            const response = await fetch(`/preview/${this.currentFileId}`);
            const result = await response.json();
            
            if (response.ok && result.preview) {
                this.previewContent.innerHTML = `<pre>${result.preview}</pre>`;
                this.previewContainer.classList.remove('d-none');
            }
        } catch (error) {
            console.error('Preview failed:', error);
        }
    }
    
    async loadConversionHistory() {
        try {
            const response = await fetch('/history');
            const result = await response.json();
            
            if (response.ok && result.files) {
                this.displayHistory(result.files);
            } else {
                this.historyList.innerHTML = '<p class="text-muted">No conversion history available.</p>';
            }
        } catch (error) {
            this.historyList.innerHTML = '<p class="text-danger">Failed to load history.</p>';
        }
    }
    
    displayHistory(files) {
        if (files.length === 0) {
            this.historyList.innerHTML = '<p class="text-muted">No converted files yet.</p>';
            return;
        }
        
        const historyHTML = files.map(file => {
            const date = new Date(file.created * 1000).toLocaleString();
            const sizeKB = Math.round(file.size / 1024);
            return `
                <div class="d-flex justify-content-between align-items-center border-bottom py-2">
                    <div>
                        <strong>${file.filename}</strong>
                        <br>
                        <small class="text-muted">${date} • ${sizeKB} KB</small>
                    </div>
                    <a href="/download/${file.filename.replace('.pdf', '')}" class="btn btn-sm btn-outline-primary">
                        <i class="fas fa-download"></i>
                    </a>
                </div>
            `;
        }).join('');
        
        this.historyList.innerHTML = historyHTML;
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
    
    showOptionsArea() {
        this.uploadArea.classList.add('d-none');
        this.progressArea.classList.add('d-none');
        this.optionsArea.classList.remove('d-none');
        this.optionsArea.classList.add('fade-in');
    }
    
    showProgressArea() {
        this.uploadArea.classList.add('d-none');
        this.optionsArea.classList.add('d-none');
        this.progressArea.classList.remove('d-none');
        this.progressArea.classList.add('fade-in');
    }
    
    showSuccessArea() {
        this.progressArea.classList.add('d-none');
        this.optionsArea.classList.add('d-none');
        this.successArea.classList.remove('d-none');
        this.successArea.classList.add('slide-up');
    }
    
    resetInterface() {
        // Hide all areas
        this.progressArea.classList.add('d-none');
        this.optionsArea.classList.add('d-none');
        this.successArea.classList.add('d-none');
        this.previewContainer.classList.add('d-none');
        
        // Show upload area
        this.uploadArea.classList.remove('d-none');
        
        // Reset form
        this.fileInput.value = '';
        this.batchFileInput.value = '';
        this.passwordInput.value = '';
        this.outputNameInput.value = '';
        this.progressBar.style.width = '0%';
        this.progressText.textContent = 'Uploading...';
        
        // Reset state
        this.currentFileId = null;
        this.currentFileName = null;
        this.batchFiles = [];
        
        // Remove animation classes
        this.progressArea.classList.remove('fade-in');
        this.optionsArea.classList.remove('fade-in');
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
