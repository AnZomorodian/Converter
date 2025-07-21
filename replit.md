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

## Migration Completed (July 21, 2025)

✓ **Successfully migrated from Replit Agent to Replit environment**
✓ **Removed PostgreSQL database integration** - Now using file-based local storage
✓ **Converted all text to English** throughout the application
✓ **Simplified header design** - Removed icons, made brand name bigger and centered
✓ **Enhanced footer design** - Added professional sections with social media links (GitHub, Telegram, Discord)
✓ **Fixed file browser double-click issue** - Improved event handling for file selection
✓ **Updated theme** - Modern purple/blue gradients with enhanced visual effects
✓ **Improved responsive design** - Better mobile compatibility and layout
✓ **Maintained all core functionality** - File conversion, drag-and-drop, progress tracking

## Latest Update (July 21, 2025 - Evening)

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
✓ Removed old supported formats section as requested
✓ Implemented custom fonts: Poppins for headers/brand, Inter for body text
✓ Updated color scheme with modern purple/blue gradients and improved contrast
✓ Fixed LibreOffice integration - all conversions now working properly
✓ Successfully tested Word to PDF conversion with real files
✓ Added system dependency installation for LibreOffice

## Latest Update (July 21, 2025 - Evening)
### 🔥 Major Feature Addition: Advanced Conversion Types
✓ **Added 3 new conversion types**: Image Format Converter, PDF Merge, and Images to PDF
✓ **Enhanced Conversion Options**: Added 6 conversion types total with specialized UI for each
✓ **Image Format Conversion**: Convert between PNG, JPG, WebP, BMP, TIFF with quality settings
✓ **PDF Merging**: Batch process to combine multiple PDF files into one document
✓ **Images to PDF**: Convert multiple images into a single PDF with proper scaling and centering
✓ **Advanced Batch Processing**: Smart handling for different conversion types with appropriate file grouping
✓ **Enhanced UI**: Type-specific options and instructions shown based on selected conversion type
✓ **Improved Converter Functions**: Added convert_image_format(), merge_pdfs(), convert_multiple_images_to_pdf()
✓ **Better Grid Layout**: Expanded conversion type grid to handle 6 options with 300px minimum width
✓ **Smart File Handling**: Skip individual processing for batch types, handle at the end

## Latest Major Updates (July 21, 2025 - Evening)
### 🔧 Enhanced Image Format Converter & GitHub-Ready Features
✓ **Complete Image Format Support**: Enhanced converter to support all major formats (PNG, JPG, BMP, TIFF, WebP, GIF, ICO, TGA, EPS, PDF)
✓ **Fixed BMP, TIFF, JPEG Issues**: Resolved format conversion errors with proper transparency and mode handling
✓ **Advanced Format Handling**: Improved color mode conversion for different target formats with proper fallbacks
✓ **Enhanced README**: Created comprehensive GitHub-ready documentation with badges, installation guides, and feature highlights
✓ **About Us Page**: Built amazing About Us page showcasing DeepInk Team with professional design and team profiles
✓ **Restored Original Design**: Reverted to original purple/blue gradient theme as requested
✓ **Enhanced Footer**: Added About Us link and improved social media integration
✓ **Better Error Handling**: Fixed PIL Image errors and improved format compatibility
✓ **Quality Settings**: Enhanced image quality controls for different output formats
✓ **Format Detection**: Better automatic format detection and conversion optimization

## Migration & Major Enhancements (July 21, 2025)
### 🚀 Replit Migration Completed + Advanced Features Added
✓ **Replit Environment Migration**: Successfully migrated from Replit Agent to standard Replit environment
✓ **Enhanced Image Format Converter**: Now properly changes file extensions (JPG to PNG works correctly)
✓ **Advanced PDF Merge**: Added file ordering, individual PDF password support, output password protection
✓ **Improved Image Conversion**: Support for JPG, PNG, WebP, BMP, TIFF with quality settings
✓ **Password-Protected PDF Support**: Can handle password-protected PDFs in merge operations
✓ **Custom File Ordering**: Users can specify merge order (e.g., 2,1,3 to reorder files)
✓ **Enhanced Frontend**: Advanced settings UI for both image conversion and PDF merge
✓ **PyPDF2 Integration**: Added proper PDF manipulation library for advanced features
✓ **Quality Controls**: Image quality settings from 60% to 95% for optimal file size vs quality
✓ **Transparency Handling**: Proper handling of RGBA images when converting to formats without transparency
✓ **File Extension Correction**: Output files now have correct extensions matching target format

## Major Update (July 21, 2025) - GitHub-Ready Release

### 🚀 Major Features Added
✓ **GitHub-Ready Project Structure**: Complete documentation, README, LICENSE, CONTRIBUTING.md
✓ **Advanced Database Integration**: PostgreSQL models for conversion history, statistics, and file metadata
✓ **Real-time Progress Tracking**: Server-sent events for live conversion updates
✓ **Enhanced Security**: File validation, secure headers, input sanitization
✓ **Advanced File Processing**: Metadata extraction, hash calculation, image dimensions
✓ **Comprehensive API**: RESTful endpoints for stats, health checks, and file management
✓ **Batch Processing**: Advanced queue management and parallel conversions
✓ **Error Handling**: Custom 404/500 pages, proper exception handling
✓ **Development Tools**: Makefile, Docker setup, testing framework
✓ **Monitoring**: Health checks, system stats, performance metrics
✓ **Professional Deployment**: Docker Compose, Nginx config, production setup

### 🔧 Technical Improvements
✓ **Enhanced Converter**: Better LibreOffice integration, quality settings, password protection
✓ **Advanced JavaScript**: Drag-and-drop, keyboard shortcuts, real-time updates
✓ **Database Models**: ConversionHistory, SystemStats, FileMetadata tracking
✓ **Utility Functions**: File validation, cleanup, progress tracking, format detection
✓ **API Routes**: Comprehensive REST API with authentication and rate limiting
✓ **Security Enhancements**: CSRF protection, secure cookies, file validation
✓ **Performance**: Caching, async processing, optimized database queries
✓ **Logging**: Structured logging, error tracking, performance monitoring

### 🎨 UI/UX Enhancements
✓ **Professional Design**: Modern gradients, animations, responsive layout
✓ **Advanced Features**: File preview, batch upload, progress tracking
✓ **Error Pages**: Beautiful 404/500 error pages with recovery options
✓ **Accessibility**: Keyboard navigation, screen reader support, high contrast
✓ **Mobile Optimization**: Touch-friendly interface, responsive design

### 📚 Documentation & DevOps
✓ **Comprehensive README**: Installation, features, API docs, deployment guide
✓ **Contributing Guide**: Development setup, coding standards, contribution process
✓ **Change Log**: Detailed version history and feature tracking
✓ **License**: MIT license for open source distribution
✓ **Docker Support**: Multi-stage builds, health checks, production config
✓ **Development Tools**: Makefile for common tasks, testing setup
✓ **Monitoring**: Prometheus, Grafana, health endpoints

### 🔒 Security & Reliability
✓ **Input Validation**: Comprehensive file type and content validation
✓ **Secure Headers**: CSRF, XSS protection, secure cookie settings
✓ **Error Handling**: Graceful degradation, proper exception management
✓ **Rate Limiting**: API throttling and abuse prevention
✓ **Data Protection**: Secure file handling, automatic cleanup
✓ **Audit Logging**: Comprehensive logging for security monitoring