# 🚀 Fily Pro - Professional File Converter

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-v3.11+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-v3.1+-green.svg)](https://flask.palletsprojects.com/)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/user/fily-pro)

A powerful, modern web application for converting various file formats to PDF with advanced features including batch processing, password protection, and merge capabilities.

## ✨ Features

### 🔄 **Multi-Format Support**
- **Documents**: DOC, DOCX, RTF, ODT, TXT, MD
- **Spreadsheets**: XLS, XLSX, ODS, CSV
- **Presentations**: PPT, PPTX, ODP
- **Images**: PNG, JPG, JPEG, GIF, BMP, TIFF
- **Web & Data**: HTML, XML, JSON, CSS, JS, Python files
- **Archives**: PDF processing and manipulation

### 🎯 **Advanced Conversion Options**
- **Any-to-PDF**: Convert any supported file to PDF
- **PDF-to-Word**: Extract and convert PDF content to Word documents
- **PDF Password Protection**: Secure your PDFs with encryption
- **PDF Merge**: Combine multiple PDFs into one document
- **Quality Settings**: High, Medium, Low quality options
- **Batch Processing**: Upload and convert multiple files simultaneously

### 🛡️ **Security & Performance**
- File type validation and sanitization
- Secure filename handling with UUID generation
- 50MB file size limit per upload
- Session-based security with environment variables
- PostgreSQL database support for scalability
- LibreOffice headless conversion for reliability

### 🎨 **Modern UI/UX**
- Responsive Bootstrap 5 design
- Drag-and-drop file upload
- Real-time conversion progress
- Beautiful animations and transitions
- Mobile-friendly interface
- Professional gradient themes

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- LibreOffice (for document conversions)
- PostgreSQL (optional, for advanced features)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/fily-pro.git
   cd fily-pro
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install LibreOffice** (system dependency)
   ```bash
   # Ubuntu/Debian
   sudo apt-get install libreoffice
   
   # macOS
   brew install --cask libreoffice
   
   # Windows
   # Download from https://www.libreoffice.org/
   ```

4. **Set environment variables**
   ```bash
   export SESSION_SECRET="your-secret-key-here"
   export DATABASE_URL="postgresql://user:pass@localhost/dbname"  # Optional
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

6. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

## 🏗️ Architecture

```
├── app.py              # Flask application configuration
├── main.py             # Application entry point
├── routes.py           # URL routing and request handlers
├── converter.py        # File conversion engine
├── models.py           # Database models (optional)
├── requirements.txt    # Python dependencies
├── static/
│   ├── css/           # Custom stylesheets
│   └── js/            # JavaScript functionality
├── templates/
│   └── index.html     # Main application template
├── uploads/           # Temporary file storage
└── converted/         # Converted file output
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `SESSION_SECRET` | Flask session encryption key | Yes | None |
| `DATABASE_URL` | PostgreSQL connection string | No | None |
| `MAX_CONTENT_LENGTH` | Maximum file size (bytes) | No | 52428800 (50MB) |

### Application Settings

```python
# File size limits
MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB

# Supported file extensions
ALLOWED_EXTENSIONS = {
    'docx', 'doc', 'xlsx', 'xls', 'pptx', 'ppt',
    'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff',
    'txt', 'pdf', 'rtf', 'odt', 'ods', 'odp',
    'csv', 'html', 'htm', 'xml', 'json', 'md',
    'py', 'js', 'css'
}
```

## 📚 API Documentation

### Upload Single File
```http
POST /upload
Content-Type: multipart/form-data

file: [binary file data]
```

### Upload Multiple Files
```http
POST /batch-upload
Content-Type: multipart/form-data

files[]: [binary file data]
files[]: [binary file data]
```

### Convert File
```http
POST /convert
Content-Type: application/json

{
  "file_id": "uuid-string",
  "original_filename": "document.docx",
  "conversion_type": "any-to-pdf",
  "quality": "high",
  "password": "optional-password"
}
```

### Download Converted File
```http
GET /download/<file_id>
```

## 🧪 Testing

Run the test suite:
```bash
python -m pytest tests/
```

Run with coverage:
```bash
python -m pytest --cov=. tests/
```

## 🚀 Deployment

### Replit Deployment
This application is optimized for Replit deployment:

1. Import the repository to Replit
2. Set environment variables in Replit Secrets
3. Run the application using the provided workflow

### Docker Deployment
```dockerfile
FROM python:3.11-slim

# Install LibreOffice
RUN apt-get update && apt-get install -y libreoffice

# Copy application
WORKDIR /app
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Run application
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
```

### Production Considerations
- Use a proper WSGI server (Gunicorn, uWSGI)
- Set up reverse proxy (Nginx, Apache)
- Configure SSL/TLS certificates
- Implement proper logging and monitoring
- Set up file cleanup cron jobs
- Use cloud storage for file persistence

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 Python style guide
- Add tests for new features
- Update documentation for API changes
- Use type hints where appropriate
- Maintain backward compatibility

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **LibreOffice** - Document conversion engine
- **Flask** - Web framework
- **Bootstrap** - UI framework
- **Font Awesome** - Icon library
- **ReportLab** - PDF generation library

## 📞 Support

- **Documentation**: [Wiki](https://github.com/yourusername/fily-pro/wiki)
- **Issues**: [GitHub Issues](https://github.com/yourusername/fily-pro/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/fily-pro/discussions)

## 🗺️ Roadmap

- [ ] **v2.0**: OCR support for scanned documents
- [ ] **v2.1**: Cloud storage integration (AWS S3, Google Drive)
- [ ] **v2.2**: API rate limiting and authentication
- [ ] **v2.3**: Advanced PDF editing features
- [ ] **v2.4**: Real-time collaboration features
- [ ] **v2.5**: Mobile app development

---

**Made with ❤️ by the DeepInk Team**

[![GitHub stars](https://img.shields.io/github/stars/yourusername/fily-pro.svg?style=social&label=Star)](https://github.com/yourusername/fily-pro)
[![GitHub forks](https://img.shields.io/github/forks/yourusername/fily-pro.svg?style=social&label=Fork)](https://github.com/yourusername/fily-pro/fork)