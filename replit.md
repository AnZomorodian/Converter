# File to PDF Converter

## Overview

This is a Flask-based web application that converts various file formats (Word documents, Excel spreadsheets, PowerPoint presentations, images, and text files) to PDF format. The application provides a simple drag-and-drop interface for file uploads and uses LibreOffice for document conversions.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

The application follows a traditional Flask web application architecture with a clean separation of concerns:

- **Frontend**: Bootstrap-based responsive UI with drag-and-drop functionality
- **Backend**: Flask web framework with file upload and conversion capabilities
- **File Processing**: LibreOffice headless mode for document conversions
- **Storage**: Local file system for temporary file storage

## Key Components

### 1. Flask Application (`app.py`)
- Main application configuration and initialization
- Sets up file upload limits (50MB max)
- Configures upload and converted file directories
- Implements ProxyFix middleware for deployment behind reverse proxies

### 2. Route Handlers (`routes.py`)
- `/` - Serves the main upload interface
- `/upload` - Handles file uploads with validation
- File type validation for supported formats (DOC, DOCX, XLS, XLSX, PPT, PPTX, images, TXT)
- UUID-based file naming to prevent conflicts

### 3. Conversion Engine (`converter.py`)
- Modular conversion system supporting multiple file formats
- LibreOffice headless mode for Office document conversions
- Separate conversion functions for different file types
- Error handling and logging for conversion failures

### 4. Frontend Interface
- **HTML Template** (`templates/index.html`): Bootstrap-based responsive design
- **CSS Styling** (`static/css/style.css`): Custom styling with gradient backgrounds and hover effects
- **JavaScript** (`static/js/main.js`): Drag-and-drop functionality and AJAX file uploads

## Data Flow

1. **File Upload**: User selects or drags a file to the upload area
2. **Validation**: Server validates file type and size constraints
3. **Storage**: File is saved with a unique UUID-based filename
4. **Conversion**: Appropriate converter is called based on file extension
5. **Response**: Converted PDF is made available for download
6. **Cleanup**: Temporary files are managed (implementation pending)

## External Dependencies

### System Dependencies
- **LibreOffice**: Required for converting Office documents (Word, Excel, PowerPoint)
- **Python Packages**: Flask, Werkzeug for web framework functionality

### Frontend Dependencies
- **Bootstrap 5.3.0**: UI framework for responsive design
- **Font Awesome 6.0.0**: Icon library for visual elements

## Deployment Strategy

The application is configured for flexible deployment:

- **Development**: Direct Flask development server (`app.run()`)
- **Production**: WSGI-compatible with ProxyFix middleware for reverse proxy deployment
- **Environment Configuration**: Uses environment variables for sensitive settings (SESSION_SECRET)
- **File System**: Requires persistent storage for upload and converted directories

### Key Deployment Considerations

1. **File Storage**: Currently uses local file system - may need cloud storage for scalability
2. **LibreOffice Dependency**: Must be installed on deployment environment
3. **Resource Management**: No automatic cleanup of temporary files implemented
4. **Security**: File type validation prevents most malicious uploads
5. **Scalability**: Single-threaded conversion process may become bottleneck

## Technical Notes

- **File Size Limit**: 50MB maximum per upload
- **Supported Formats**: DOC/DOCX, XLS/XLSX, PPT/PPTX, common image formats, TXT, CSV, PDF, RTF, ODT, ODS, ODP
- **Conversion Timeout**: 60-second timeout for LibreOffice operations
- **Error Handling**: Comprehensive logging for debugging conversion issues
- **File Naming**: UUID-based system prevents filename conflicts
- **Batch Processing**: Support for multiple file uploads and conversions
- **Quality Options**: High, medium, and low quality conversion settings
- **Password Protection**: Basic framework (implementation pending)
- **File Preview**: Text and image preview capabilities
- **Conversion History**: Track and display recent conversions

## Recent Changes (July 2025)

✓ Fixed file upload bug with missing extensions that caused "list index out of range" error
✓ Added batch file upload and conversion capability
✓ Enhanced supported file formats (CSV, PDF, RTF, ODT, ODS, ODP, HTML, XML, JSON, MD, PY, JS, CSS)
✓ Implemented conversion options (quality settings, password protection framework, custom output names)
✓ Added file preview functionality for images and text files
✓ Created conversion history tracking and display (limited to last 5 files)
✓ Improved error handling and validation
✓ Enhanced UI with options area and better progress tracking
✓ Added transparent footer with Fily branding, DeepInk Team credit, GitHub/Telegram icons
✓ Improved drag & drop area with animated pulse effect and format badges
✓ Enhanced drag & drop functionality to handle single and multiple files properly
✓ Fixed multiple file dialog bug preventing duplicate upload dialogs
✓ Added delete functionality for recent conversions with trash icon
✓ Redesigned header with "Fily Pro" branding and dropdown conversion menu
✓ Added PDF-to-PDF conversion modes (PDF to Word, Password Protection, Merge PDFs)
✓ Enhanced hero section with animated floating icon and feature badges
✓ Improved responsive design and mobile compatibility
✓ Fixed download system with enhanced file search and error handling
✓ Reorganized main page with conversion type selection first, then file upload
✓ Added visual conversion type selector with 4 main options
✓ Improved user flow: Choose conversion type → Upload files → Configure → Convert
✓ Enhanced file finding algorithm for downloads to prevent "File not found" errors
✓ Removed conversion dropdown from header for cleaner navigation
✓ Added back button to return to conversion type selection
✓ Moved supported formats section above conversion type chooser
✓ Enhanced CSS animations and visual effects for better user experience
✓ Fixed Word to PDF conversion error with better file handling
✓ Added smooth transitions and hover effects throughout the interface
✓ Added system dependency installation for LibreOffice