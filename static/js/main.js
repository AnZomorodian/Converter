// Modern JavaScript for Fily Pro - File to PDF Converter
class FilyPro {
    constructor() {
        this.selectedType = null;
        this.selectedFiles = [];
        this.isConverting = false;
        
        this.initializeElements();
        this.setupEventListeners();
        this.loadRecentConversions();
    }

    initializeElements() {
        // Main elements
        this.conversionTypeCard = document.getElementById('conversionTypeCard');
        this.uploadCard = document.getElementById('uploadCard');
        this.fileInput = document.getElementById('fileInput');
        this.uploadArea = document.getElementById('uploadArea');
        this.filesPreview = document.getElementById('filesPreview');
        this.filesList = document.getElementById('filesList');
        this.convertButton = document.getElementById('convertButton');
        this.progressSection = document.getElementById('progressSection');
        this.progressBar = document.getElementById('progressBar');
        this.progressText = document.getElementById('progressText');
        this.backButton = document.getElementById('backButton');
        this.convertSection = document.getElementById('convertSection');
        this.conversionOptions = document.getElementById('conversionOptions');
        this.recentConversions = document.getElementById('recentConversions');
    }

    setupEventListeners() {
        // Conversion type selection
        document.querySelectorAll('.conversion-option').forEach(option => {
            option.addEventListener('click', (e) => this.selectConversionType(e.target.closest('.conversion-option')));
        });

        // File input and upload area
        this.fileInput?.addEventListener('change', (e) => this.handleFileSelect(e));
        
        if (this.uploadArea) {
            this.uploadArea.addEventListener('click', (e) => {
                // Only trigger file input if clicking directly on upload area, not on file input
                if (e.target !== this.fileInput) {
                    this.fileInput.click();
                }
            });
            this.uploadArea.addEventListener('dragover', (e) => this.handleDragOver(e));
            this.uploadArea.addEventListener('dragleave', (e) => this.handleDragLeave(e));
            this.uploadArea.addEventListener('drop', (e) => this.handleFileDrop(e));
        }

        // Convert button
        this.convertButton?.addEventListener('click', () => this.convertFiles());

        // Back button
        this.backButton?.addEventListener('click', () => this.goBack());

        // Prevent default drag behavior on document
        document.addEventListener('dragover', (e) => e.preventDefault());
        document.addEventListener('drop', (e) => e.preventDefault());
    }

    selectConversionType(option) {
        // Remove previous selection
        document.querySelectorAll('.conversion-option').forEach(opt => {
            opt.classList.remove('selected');
        });

        // Select new option
        option.classList.add('selected');
        this.selectedType = option.dataset.type;

        // Show appropriate options based on conversion type
        this.showConversionTypeOptions();

        // Show upload card after a short delay
        setTimeout(() => {
            this.conversionTypeCard.style.display = 'none';
            this.uploadCard.style.display = 'block';
            this.uploadCard.scrollIntoView({ behavior: 'smooth' });
        }, 300);
    }

    showConversionTypeOptions() {
        // Hide all specific options first
        document.getElementById('imageFormatOptions').style.display = 'none';
        document.getElementById('mergeInstructions').style.display = 'none';
        document.getElementById('imagesToPdfInstructions').style.display = 'none';

        // Set file input accept attribute based on conversion type
        const fileInput = document.getElementById('fileInput');
        if (this.selectedType === 'image-converter') {
            document.getElementById('imageFormatOptions').style.display = 'block';
            fileInput.accept = '.png,.jpg,.jpeg,.gif,.bmp,.tiff,.webp';
        } else if (this.selectedType === 'merge-pdf') {
            document.getElementById('mergeInstructions').style.display = 'block';
            fileInput.accept = '.pdf';
        } else if (this.selectedType === 'images-to-pdf') {
            document.getElementById('imagesToPdfInstructions').style.display = 'block';
            fileInput.accept = '.png,.jpg,.jpeg,.gif,.bmp,.tiff';
        } else if (this.selectedType === 'document-to-pdf') {
            fileInput.accept = '.doc,.docx,.xls,.xlsx,.ppt,.pptx,.odt,.ods,.odp';
        } else if (this.selectedType === 'text-to-pdf') {
            fileInput.accept = '.txt,.rtf,.md,.html,.csv';
        } else {
            fileInput.accept = '.doc,.docx,.xls,.xlsx,.ppt,.pptx,.txt,.rtf,.odt,.ods,.odp,.csv,.png,.jpg,.jpeg,.gif,.bmp,.tiff,.pdf,.md,.html';
        }
    }

    goBack() {
        this.uploadCard.style.display = 'none';
        this.conversionTypeCard.style.display = 'block';
        this.resetUpload();
    }

    resetUpload() {
        this.selectedFiles = [];
        this.filesList.innerHTML = '';
        this.filesPreview.style.display = 'none';
        this.convertSection.style.display = 'none';
        this.conversionOptions.style.display = 'none';
        this.progressSection.style.display = 'none';
        this.isConverting = false;
    }

    handleDragOver(e) {
        e.preventDefault();
        this.uploadArea.classList.add('dragover');
    }

    handleDragLeave(e) {
        e.preventDefault();
        if (!this.uploadArea.contains(e.relatedTarget)) {
            this.uploadArea.classList.remove('dragover');
        }
    }

    handleFileDrop(e) {
        e.preventDefault();
        this.uploadArea.classList.remove('dragover');
        this.uploadArea.classList.add('pulse');
        
        setTimeout(() => {
            this.uploadArea.classList.remove('pulse');
        }, 600);

        const files = Array.from(e.dataTransfer.files);
        this.processFiles(files);
    }

    handleFileSelect(e) {
        const files = Array.from(e.target.files);
        this.processFiles(files);
    }

    processFiles(files) {
        this.selectedFiles = files;
        this.displaySelectedFiles();
        
        if (files.length > 0) {
            this.filesPreview.style.display = 'block';
            this.conversionOptions.style.display = 'block';
            this.convertSection.style.display = 'block';
        }
    }

    displaySelectedFiles() {
        if (this.selectedFiles.length === 0) {
            this.filesList.innerHTML = '<p class="text-muted">No files selected</p>';
            return;
        }

        const filesHTML = this.selectedFiles.map((file, index) => {
            const fileSize = this.formatFileSize(file.size);
            const fileIcon = this.getFileIcon(file.name);
            
            return `
                <div class="file-item" data-index="${index}">
                    <div class="file-info">
                        <div class="file-icon">
                            <i class="${fileIcon}"></i>
                        </div>
                        <div class="file-details">
                            <h6>${file.name}</h6>
                            <div class="file-size">${fileSize}</div>
                        </div>
                    </div>
                </div>
            `;
        }).join('');

        this.filesList.innerHTML = filesHTML;
    }

    getFileIcon(filename) {
        const ext = filename.split('.').pop().toLowerCase();
        const iconMap = {
            'pdf': 'fas fa-file-pdf',
            'doc': 'fas fa-file-word',
            'docx': 'fas fa-file-word',
            'xls': 'fas fa-file-excel',
            'xlsx': 'fas fa-file-excel',
            'ppt': 'fas fa-file-powerpoint',
            'pptx': 'fas fa-file-powerpoint',
            'txt': 'fas fa-file-alt',
            'rtf': 'fas fa-file-alt',
            'png': 'fas fa-file-image',
            'jpg': 'fas fa-file-image',
            'jpeg': 'fas fa-file-image',
            'gif': 'fas fa-file-image',
            'bmp': 'fas fa-file-image',
            'tiff': 'fas fa-file-image'
        };
        return iconMap[ext] || 'fas fa-file';
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 B';
        const k = 1024;
        const sizes = ['B', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    async convertFiles() {
        if (this.isConverting || this.selectedFiles.length === 0) return;

        this.isConverting = true;
        this.convertButton.disabled = true;
        this.progressSection.style.display = 'block';

        const formData = new FormData();
        
        // Add files
        this.selectedFiles.forEach((file, index) => {
            formData.append('files[]', file);
        });

        // Add options
        formData.append('conversion_type', this.selectedType);
        formData.append('quality', document.getElementById('qualitySelect').value);
        formData.append('custom_name', document.getElementById('customName').value);

        try {
            // Simulate progress
            this.updateProgress(10, 'Uploading files...');
            
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            this.updateProgress(50, 'Converting files...');

            const result = await response.json();
            
            this.updateProgress(100, 'Conversion completed!');

            if (result.results) {
                this.handleConversionResults(result.results);
            }

        } catch (error) {
            console.error('Conversion error:', error);
            this.showError('Conversion failed. Please try again.');
        }

        setTimeout(() => {
            this.isConverting = false;
            this.convertButton.disabled = false;
            this.progressSection.style.display = 'none';
            this.loadRecentConversions();
        }, 2000);
    }

    updateProgress(percent, text) {
        this.progressBar.style.width = percent + '%';
        this.progressText.textContent = text;
    }

    handleConversionResults(results) {
        const successCount = results.filter(r => r.success).length;
        const totalCount = results.length;

        if (successCount === totalCount) {
            this.showSuccess(`Successfully converted ${successCount} file(s)!`);
            // Auto-download if single file
            if (successCount === 1) {
                const successResult = results.find(r => r.success);
                if (successResult.download_url) {
                    window.open(successResult.download_url, '_blank');
                }
            }
        } else if (successCount > 0) {
            this.showWarning(`Converted ${successCount} out of ${totalCount} files.`);
        } else {
            this.showError('All conversions failed. Please check your files and try again.');
        }
    }

    showSuccess(message) {
        this.showNotification(message, 'success');
    }

    showError(message) {
        this.showNotification(message, 'error');
    }

    showWarning(message) {
        this.showNotification(message, 'warning');
    }

    showNotification(message, type) {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `alert alert-${type === 'error' ? 'danger' : type === 'warning' ? 'warning' : 'success'} position-fixed`;
        notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px; transform: translateX(100%); transition: transform 0.3s ease;';
        notification.innerHTML = `
            <div class="d-flex align-items-center">
                <i class="fas fa-${type === 'error' ? 'exclamation-circle' : type === 'warning' ? 'exclamation-triangle' : 'check-circle'} me-2"></i>
                <span>${message}</span>
                <button type="button" class="btn-close ms-auto" onclick="this.parentElement.parentElement.remove()"></button>
            </div>
        `;

        document.body.appendChild(notification);

        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, 5000);
        
        // Add a subtle animation when notification appears
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 10);
    }

    async loadRecentConversions() {
        try {
            const response = await fetch('/api/recent-conversions');
            const result = await response.json();

            if (result.success && result.conversions) {
                this.displayRecentConversions(result.conversions);
            }
        } catch (error) {
            console.error('Error loading recent conversions:', error);
            this.recentConversions.innerHTML = '<p class="text-muted text-center">Unable to load recent conversions</p>';
        }
    }

    displayRecentConversions(conversions) {
        if (!conversions || conversions.length === 0) {
            this.recentConversions.innerHTML = '<p class="text-muted text-center">No recent conversions</p>';
            return;
        }

        const conversionsHTML = conversions.slice(0, 5).map(conv => {
            const date = new Date(conv.created_at).toLocaleDateString();
            const time = new Date(conv.created_at).toLocaleTimeString();
            const status = conv.status === 'completed' ? 'success' : 'failed';
            const statusIcon = status === 'success' ? 'fa-check-circle text-success' : 'fa-times-circle text-danger';
            
            return `
                <div class="recent-item">
                    <div class="recent-info">
                        <div class="recent-icon">
                            <i class="fas ${statusIcon}"></i>
                        </div>
                        <div class="recent-details">
                            <h6>${conv.original_filename}</h6>
                            <div class="recent-meta">
                                ${date} at ${time} • ${this.formatFileSize(conv.file_size)}
                            </div>
                        </div>
                    </div>
                    <div class="recent-actions">
                        ${status === 'success' ? `
                            <a href="/download/${conv.file_id}" class="btn btn-sm btn-outline-primary" target="_blank">
                                <i class="fas fa-download"></i>
                            </a>
                        ` : ''}
                        <button class="btn btn-sm btn-outline-danger" onclick="window.filyPro.deleteConversion('${conv.file_id}')">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
            `;
        }).join('');

        this.recentConversions.innerHTML = conversionsHTML;
    }

    async deleteConversion(fileId) {
        if (!confirm('Are you sure you want to delete this conversion?')) return;

        // Show loading state
        const deleteButton = document.querySelector(`button[onclick*="${fileId}"]`);
        if (deleteButton) {
            deleteButton.disabled = true;
            deleteButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
        }

        try {
            const response = await fetch(`/api/delete-conversion/${fileId}`, {
                method: 'DELETE'
            });

            const result = await response.json();
            
            if (result.success) {
                this.showSuccess('File deleted successfully');
                // Reload the recent conversions list
                await this.loadRecentConversions();
            } else {
                this.showError(result.error || 'Failed to delete file');
                // Reset button state
                if (deleteButton) {
                    deleteButton.disabled = false;
                    deleteButton.innerHTML = '<i class="fas fa-trash"></i>';
                }
            }
        } catch (error) {
            console.error('Error deleting conversion:', error);
            this.showError('Failed to delete file');
            // Reset button state
            if (deleteButton) {
                deleteButton.disabled = false;
                deleteButton.innerHTML = '<i class="fas fa-trash"></i>';
            }
        }
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.filyPro = new FilyPro();
});