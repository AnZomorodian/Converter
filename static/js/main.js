class PDFConverter {
    constructor() {
        this.initializeElements();
        this.attachEventListeners();
        this.loadConversionHistory();
        this.selectedConversionType = null;
        this.hideUploadAreaInitially();
    }
    
    initializeElements() {
        // File inputs
        this.fileInput = document.getElementById('fileInput');
        this.batchFileInput = document.getElementById('batchFileInput');
        
        // Upload area
        this.uploadArea = document.getElementById('uploadArea');
        
        // Form elements
        this.passwordInput = document.getElementById('passwordInput');
        this.qualitySelect = document.getElementById('qualitySelect');
        this.outputNameInput = document.getElementById('outputNameInput');
        
        // Buttons
        this.startConversionBtn = document.getElementById('startConversionBtn');
        this.downloadBtn = document.getElementById('downloadBtn');
        this.convertAnotherBtn = document.getElementById('convertAnotherBtn');
        this.refreshHistoryBtn = document.getElementById('refreshHistoryBtn');
        
        // Display areas
        this.optionsArea = document.getElementById('optionsArea');
        this.progressArea = document.getElementById('progressArea');
        this.successArea = document.getElementById('successArea');
        this.previewContainer = document.getElementById('previewContainer');
        this.previewContent = document.getElementById('previewContent');
        
        // Progress elements
        this.progressBar = document.querySelector('.progress-bar');
        this.progressText = document.getElementById('progressText');
        this.fileName = document.getElementById('fileName');
        
        // History
        this.historyList = document.getElementById('historyList');
        
        // State
        this.currentFileId = null;
        this.currentFileName = null;
        this.batchFiles = [];
        this.selectedConversionType = null;
    }
    
    hideUploadAreaInitially() {
        this.uploadArea.classList.add('initial-hidden');
    }
    
    showUploadArea() {
        this.uploadArea.classList.remove('initial-hidden', 'd-none');
        document.getElementById('conversionTypeSelector').style.display = 'none';
        document.getElementById('supportedFormatsSection').style.display = 'none';
        document.getElementById('backButtonContainer').style.display = 'block';
    }
    
    attachEventListeners() {
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
        
        // Click to upload - prevent multiple triggers
        this.uploadArea.addEventListener('click', (e) => {
            if (!e.target.closest('.btn')) {
                this.fileInput.click();
            }
        });
        
        // Buttons
        this.downloadBtn.addEventListener('click', () => {
            this.downloadFile();
        });
        
        this.convertAnotherBtn.addEventListener('click', () => {
            this.resetInterface();
        });
        
        this.startConversionBtn.addEventListener('click', () => {
            this.convertFile();
        });
        
        this.refreshHistoryBtn.addEventListener('click', () => {
            this.loadConversionHistory();
        });
    }
    
    handleFile(file) {
        if (!this.validateFile(file)) {
            return;
        }
        
        this.currentFileName = file.name;
        this.fileName.textContent = file.name;
        
        this.showOptionsArea();
        this.uploadFile(file);
    }
    
    validateFile(file) {
        const allowedExtensions = [
            'docx', 'doc', 'xlsx', 'xls', 'pptx', 'ppt',
            'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'txt',
            'pdf', 'rtf', 'odt', 'ods', 'odp', 'csv',
            'html', 'htm', 'xml', 'json', 'md', 'py', 'js', 'css'
        ];
        
        const fileExtension = file.name.split('.').pop().toLowerCase();
        
        if (!allowedExtensions.includes(fileExtension)) {
            this.showError(`Unsupported file format: .${fileExtension}. Supported formats: DOC, DOCX, XLS, XLSX, PPT, PPTX, PNG, JPG, TXT, CSV, PDF, HTML, JSON, MD, PY, JS, CSS and more.`);
            return false;
        }
        
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
            
            // Auto-populate output name
            if (this.currentFileName) {
                const nameWithoutExt = this.currentFileName.replace(/\.[^/.]+$/, '');
                this.outputNameInput.value = nameWithoutExt;
            }
            
        } catch (error) {
            this.showError('Upload failed: ' + error.message);
            this.resetInterface();
        }
    }
    
    async convertFile() {
        try {
            this.showProgressArea();
            this.updateProgress(75, 'Converting to PDF...');
            
            // Ensure we have the required data
            if (!this.currentFileId) {
                throw new Error('No file selected for conversion');
            }
            
            const requestData = {
                file_id: this.currentFileId,
                original_filename: this.currentFileName || '',
                password: this.passwordInput.value || null,
                quality: this.qualitySelect.value || 'high',
                output_name: this.outputNameInput.value || null
            };
            
            console.log('Sending conversion request:', requestData);
            
            const response = await fetch('/convert', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestData)
            });
            
            const result = await response.json();
            
            if (!response.ok) {
                throw new Error(result.error || 'Conversion failed');
            }
            
            this.updateProgress(100, 'Conversion completed successfully!');
            this.showSuccessArea();
            this.loadConversionHistory();
            
        } catch (error) {
            this.showError('Conversion failed: ' + error.message);
            this.resetInterface();
        }
    }
    
    downloadFile() {
        if (this.currentFileId) {
            window.open(`/download/${this.currentFileId}`, '_blank');
        }
    }
    
    async loadConversionHistory() {
        try {
            const response = await fetch('/history');
            const result = await response.json();
            
            if (response.ok) {
                this.displayHistory(result.files);
            } else {
                throw new Error(result.error || 'Failed to load history');
            }
        } catch (error) {
            console.error('History loading failed:', error);
            this.historyList.innerHTML = '<p class="text-danger">Failed to load history.</p>';
        }
    }
    
    displayHistory(files) {
        if (files.length === 0) {
            this.historyList.innerHTML = '<p class="text-muted">No converted files yet.</p>';
            return;
        }
        
        const recentFiles = files.slice(0, 5);
        
        const historyHTML = recentFiles.map(file => {
            const date = new Date(file.created * 1000).toLocaleString();
            const sizeKB = Math.round(file.size / 1024);
            return `
                <div class="d-flex justify-content-between align-items-center border-bottom py-2 history-item">
                    <div class="flex-grow-1">
                        <strong>${file.filename}</strong>
                        <br>
                        <small class="text-muted">${date} • ${sizeKB} KB</small>
                    </div>
                    <div class="btn-group">
                        <a href="/download/${file.filename.replace('.pdf', '')}" class="btn btn-sm btn-outline-primary">
                            <i class="fas fa-download"></i>
                        </a>
                        <button onclick="deleteHistoryItem('${file.filename}')" class="btn btn-sm btn-outline-danger">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
            `;
        }).join('');
        
        this.historyList.innerHTML = historyHTML;
    }
    
    updateProgress(percentage, text) {
        this.progressBar.style.width = `${percentage}%`;
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
        this.progressArea.classList.add('d-none');
        this.optionsArea.classList.add('d-none');
        this.successArea.classList.add('d-none');
        this.previewContainer.classList.add('d-none');
        
        // Reset to conversion type selection
        this.uploadArea.classList.add('initial-hidden');
        document.getElementById('conversionTypeSelector').style.display = 'block';
        document.getElementById('supportedFormatsSection').style.display = 'block';
        document.getElementById('backButtonContainer').style.display = 'none';
        
        // Reset selection
        document.querySelectorAll('.conversion-option').forEach(option => {
            option.classList.remove('selected');
        });
        
        // Reset hero subtitle
        const heroSubtitle = document.getElementById('heroSubtitle');
        if (heroSubtitle) {
            heroSubtitle.textContent = 'Choose your conversion type below, then upload your files';
        }
        
        this.fileInput.value = '';
        this.batchFileInput.value = '';
        this.passwordInput.value = '';
        this.outputNameInput.value = '';
        this.progressBar.style.width = '0%';
        this.progressText.textContent = 'Uploading...';
        
        this.currentFileId = null;
        this.currentFileName = null;
        this.batchFiles = [];
        this.selectedConversionType = null;
        
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

// Global functions
function deleteHistoryItem(filename) {
    if (confirm('Delete this file from history?')) {
        fetch(`/delete/${filename}`, { method: 'DELETE' })
            .then(response => response.json())
            .then(result => {
                if (result.success) {
                    window.converter.loadConversionHistory();
                } else {
                    alert('Failed to delete file');
                }
            })
            .catch(err => {
                console.error('Delete failed:', err);
                alert('Failed to delete file');
            });
    }
}

function selectConversionType(type) {
    // Remove previous selection
    document.querySelectorAll('.conversion-option').forEach(option => {
        option.classList.remove('selected');
    });
    
    // Add selection to clicked option
    event.target.closest('.conversion-option').classList.add('selected');
    
    // Store selection
    window.converter.selectedConversionType = type;
    
    // Update hero subtitle
    const modeMessages = {
        'pdf-to-word': 'PDF to Word conversion - Upload your PDF files below',
        'pdf-password': 'Add Password Protection - Upload PDF files to secure them',
        'pdf-merge': 'Merge PDFs - Upload multiple PDF files to combine',
        'any-to-pdf': 'Convert to PDF - Upload any supported file format below'
    };
    
    const heroSubtitle = document.getElementById('heroSubtitle');
    if (heroSubtitle && modeMessages[type]) {
        heroSubtitle.textContent = modeMessages[type];
    }
    
    // Show upload area
    setTimeout(() => {
        window.converter.showUploadArea();
        document.getElementById('uploadArea').scrollIntoView({ behavior: 'smooth' });
    }, 300);
}

function showConversionMode(mode) {
    selectConversionType(mode);
}

function goBackToSelection() {
    window.converter.resetInterface();
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.converter = new PDFConverter();
});