// Advanced features for Fily Pro
class FilyPro {
    constructor() {
        this.conversionProgress = new Map();
        this.uploadQueue = [];
        this.isProcessing = false;
        this.initializeAdvancedFeatures();
    }

    initializeAdvancedFeatures() {
        this.setupProgressTracking();
        this.setupBatchProcessing();
        this.setupFilePreview();
        this.setupDragAndDrop();
        this.setupKeyboardShortcuts();
        this.setupAutoCleanup();
    }

    setupProgressTracking() {
        // Real-time progress updates using Server-Sent Events
        if (typeof(EventSource) !== "undefined") {
            this.eventSource = new EventSource('/stream-progress');
            this.eventSource.onmessage = (event) => {
                const data = JSON.parse(event.data);
                this.updateProgressBar(data.file_id, data.progress, data.status, data.message);
            };
        }
    }

    setupBatchProcessing() {
        document.getElementById('batchProcessBtn')?.addEventListener('click', () => {
            this.processBatchQueue();
        });
    }

    setupFilePreview() {
        document.addEventListener('change', (e) => {
            if (e.target.type === 'file') {
                this.previewFiles(e.target.files);
            }
        });
    }

    setupDragAndDrop() {
        const dropZone = document.getElementById('uploadArea');
        if (!dropZone) return;

        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, this.preventDefaults, false);
        });

        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, () => dropZone.classList.add('drag-over'), false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, () => dropZone.classList.remove('drag-over'), false);
        });

        dropZone.addEventListener('drop', (e) => {
            const files = e.dataTransfer.files;
            this.handleFileSelection(files);
        }, false);
    }

    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ctrl+U or Cmd+U for upload
            if ((e.ctrlKey || e.metaKey) && e.key === 'u') {
                e.preventDefault();
                document.getElementById('fileInput')?.click();
            }
            
            // Ctrl+Enter or Cmd+Enter for convert
            if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
                e.preventDefault();
                this.startConversion();
            }
            
            // Escape to cancel/clear
            if (e.key === 'Escape') {
                this.clearAllFiles();
            }
        });
    }

    setupAutoCleanup() {
        // Clean up old files every 5 minutes
        setInterval(() => {
            this.cleanupOldFiles();
        }, 5 * 60 * 1000);
    }

    preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    async handleFileSelection(files) {
        const fileArray = Array.from(files);
        const validFiles = [];

        for (const file of fileArray) {
            if (this.validateFile(file)) {
                validFiles.push(file);
                await this.addToQueue(file);
            } else {
                this.showError(`Invalid file: ${file.name}`);
            }
        }

        if (validFiles.length > 0) {
            this.updateFileList();
            this.enableConversionButton();
        }
    }

    validateFile(file) {
        const allowedTypes = [
            'application/pdf',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'application/vnd.ms-excel',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'application/vnd.ms-powerpoint',
            'application/vnd.openxmlformats-officedocument.presentationml.presentation',
            'text/plain',
            'image/jpeg',
            'image/png',
            'image/gif',
            'text/csv'
        ];

        const maxSize = 50 * 1024 * 1024; // 50MB

        if (file.size > maxSize) {
            this.showError(`File ${file.name} is too large. Maximum size is 50MB.`);
            return false;
        }

        if (!allowedTypes.includes(file.type) && !this.validateByExtension(file.name)) {
            this.showError(`File type ${file.type} is not supported.`);
            return false;
        }

        return true;
    }

    validateByExtension(filename) {
        const allowedExtensions = [
            '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
            '.txt', '.rtf', '.odt', '.ods', '.odp', '.csv', '.html',
            '.htm', '.xml', '.json', '.md', '.py', '.js', '.css',
            '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'
        ];

        const extension = filename.toLowerCase().substring(filename.lastIndexOf('.'));
        return allowedExtensions.includes(extension);
    }

    async addToQueue(file) {
        const fileInfo = {
            id: this.generateId(),
            file: file,
            name: file.name,
            size: file.size,
            type: file.type,
            status: 'queued',
            progress: 0,
            previewUrl: null
        };

        // Generate preview for images
        if (file.type.startsWith('image/')) {
            fileInfo.previewUrl = await this.generateImagePreview(file);
        }

        this.uploadQueue.push(fileInfo);
    }

    async generateImagePreview(file) {
        return new Promise((resolve) => {
            const reader = new FileReader();
            reader.onload = (e) => resolve(e.target.result);
            reader.readAsDataURL(file);
        });
    }

    updateFileList() {
        const container = document.getElementById('fileList');
        if (!container) return;

        container.innerHTML = '';

        this.uploadQueue.forEach(fileInfo => {
            const fileItem = this.createFileItem(fileInfo);
            container.appendChild(fileItem);
        });
    }

    createFileItem(fileInfo) {
        const item = document.createElement('div');
        item.className = 'file-item card mb-2';
        item.innerHTML = `
            <div class="card-body p-3">
                <div class="row align-items-center">
                    <div class="col-auto">
                        ${fileInfo.previewUrl ? 
                            `<img src="${fileInfo.previewUrl}" class="file-preview" style="width: 40px; height: 40px; object-fit: cover; border-radius: 4px;">` :
                            `<i class="fas fa-file-alt fa-2x text-primary"></i>`
                        }
                    </div>
                    <div class="col">
                        <h6 class="mb-1">${fileInfo.name}</h6>
                        <small class="text-muted">${this.formatFileSize(fileInfo.size)}</small>
                        <div class="progress mt-2" style="height: 4px;">
                            <div class="progress-bar" role="progressbar" style="width: ${fileInfo.progress}%"></div>
                        </div>
                    </div>
                    <div class="col-auto">
                        <span class="badge bg-${this.getStatusColor(fileInfo.status)}">${fileInfo.status}</span>
                        <button class="btn btn-sm btn-outline-danger ms-2" onclick="filyPro.removeFromQueue('${fileInfo.id}')">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                </div>
            </div>
        `;
        return item;
    }

    getStatusColor(status) {
        const colors = {
            'queued': 'secondary',
            'uploading': 'primary',
            'converting': 'warning',
            'completed': 'success',
            'failed': 'danger'
        };
        return colors[status] || 'secondary';
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 B';
        const k = 1024;
        const sizes = ['B', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
    }

    removeFromQueue(fileId) {
        this.uploadQueue = this.uploadQueue.filter(f => f.id !== fileId);
        this.updateFileList();
        
        if (this.uploadQueue.length === 0) {
            this.disableConversionButton();
        }
    }

    clearAllFiles() {
        this.uploadQueue = [];
        this.updateFileList();
        this.disableConversionButton();
    }

    async processBatchQueue() {
        if (this.isProcessing || this.uploadQueue.length === 0) return;

        this.isProcessing = true;
        this.updateProcessingState(true);

        for (const fileInfo of this.uploadQueue) {
            if (fileInfo.status === 'queued') {
                await this.processFile(fileInfo);
            }
        }

        this.isProcessing = false;
        this.updateProcessingState(false);
    }

    async processFile(fileInfo) {
        try {
            // Update status to uploading
            fileInfo.status = 'uploading';
            this.updateFileInList(fileInfo);

            // Upload file
            const uploadResult = await this.uploadFile(fileInfo.file);
            
            if (uploadResult.success) {
                fileInfo.status = 'converting';
                this.updateFileInList(fileInfo);

                // Convert file
                const conversionResult = await this.convertFile(uploadResult.file_id, {
                    conversion_type: this.getSelectedConversionType(),
                    quality: this.getSelectedQuality(),
                    password: this.getPasswordSetting()
                });

                if (conversionResult.success) {
                    fileInfo.status = 'completed';
                    fileInfo.downloadUrl = conversionResult.download_url;
                } else {
                    fileInfo.status = 'failed';
                    fileInfo.error = conversionResult.error;
                }
            } else {
                fileInfo.status = 'failed';
                fileInfo.error = uploadResult.error;
            }

        } catch (error) {
            fileInfo.status = 'failed';
            fileInfo.error = error.message;
        }

        this.updateFileInList(fileInfo);
    }

    async uploadFile(file) {
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const result = await response.json();
                return { success: true, ...result };
            } else {
                const error = await response.json();
                return { success: false, error: error.error };
            }
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    async convertFile(fileId, options) {
        try {
            const response = await fetch('/convert', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    file_id: fileId,
                    ...options
                })
            });

            if (response.ok) {
                const result = await response.json();
                return { success: true, ...result };
            } else {
                const error = await response.json();
                return { success: false, error: error.error };
            }
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    updateFileInList(fileInfo) {
        this.updateFileList(); // Refresh the entire list for simplicity
    }

    updateProgressBar(fileId, progress, status, message) {
        const fileInfo = this.uploadQueue.find(f => f.id === fileId);
        if (fileInfo) {
            fileInfo.progress = progress;
            fileInfo.status = status;
            fileInfo.message = message;
            this.updateFileInList(fileInfo);
        }
    }

    enableConversionButton() {
        const btn = document.getElementById('convertBtn');
        if (btn) {
            btn.disabled = false;
            btn.classList.remove('btn-secondary');
            btn.classList.add('btn-primary');
        }
    }

    disableConversionButton() {
        const btn = document.getElementById('convertBtn');
        if (btn) {
            btn.disabled = true;
            btn.classList.remove('btn-primary');
            btn.classList.add('btn-secondary');
        }
    }

    updateProcessingState(isProcessing) {
        const elements = document.querySelectorAll('.processing-indicator');
        elements.forEach(el => {
            el.style.display = isProcessing ? 'block' : 'none';
        });
    }

    getSelectedConversionType() {
        const selected = document.querySelector('input[name="conversionType"]:checked');
        return selected ? selected.value : 'any-to-pdf';
    }

    getSelectedQuality() {
        const selected = document.querySelector('input[name="quality"]:checked');
        return selected ? selected.value : 'high';
    }

    getPasswordSetting() {
        const passwordInput = document.getElementById('pdfPassword');
        return passwordInput ? passwordInput.value : '';
    }

    generateId() {
        return Math.random().toString(36).substr(2, 9);
    }

    showError(message) {
        const alertContainer = document.getElementById('alertContainer');
        if (alertContainer) {
            const alert = document.createElement('div');
            alert.className = 'alert alert-danger alert-dismissible fade show';
            alert.innerHTML = `
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            `;
            alertContainer.appendChild(alert);

            // Auto-dismiss after 5 seconds
            setTimeout(() => {
                alert.remove();
            }, 5000);
        }
    }

    showSuccess(message) {
        const alertContainer = document.getElementById('alertContainer');
        if (alertContainer) {
            const alert = document.createElement('div');
            alert.className = 'alert alert-success alert-dismissible fade show';
            alert.innerHTML = `
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            `;
            alertContainer.appendChild(alert);

            // Auto-dismiss after 3 seconds
            setTimeout(() => {
                alert.remove();
            }, 3000);
        }
    }

    async cleanupOldFiles() {
        try {
            await fetch('/cleanup-files', { method: 'POST' });
        } catch (error) {
            console.error('Cleanup failed:', error);
        }
    }

    // Analytics and Statistics
    async getUsageStats() {
        try {
            const response = await fetch('/api/stats');
            if (response.ok) {
                return await response.json();
            }
        } catch (error) {
            console.error('Failed to fetch stats:', error);
        }
        return null;
    }

    // Export functionality
    exportConversionHistory() {
        const data = this.uploadQueue.filter(f => f.status === 'completed');
        const csv = this.convertToCSV(data);
        this.downloadCSV(csv, 'conversion_history.csv');
    }

    convertToCSV(data) {
        const headers = ['File Name', 'Size', 'Status', 'Conversion Type'];
        const rows = data.map(item => [
            item.name,
            this.formatFileSize(item.size),
            item.status,
            this.getSelectedConversionType()
        ]);

        return [headers, ...rows].map(row => 
            row.map(field => `"${field}"`).join(',')
        ).join('\n');
    }

    downloadCSV(csv, filename) {
        const blob = new Blob([csv], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.setAttribute('hidden', '');
        a.setAttribute('href', url);
        a.setAttribute('download', filename);
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    }
}

// Initialize the application
const filyPro = new FilyPro();

// Expose globally for HTML onclick handlers
window.filyPro = filyPro;