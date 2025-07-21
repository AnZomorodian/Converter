# 🚀 Fily Pro - Advanced File Converter

<div align="center">
  
![Fily Pro Logo](https://img.shields.io/badge/Fily-Pro-purple?style=for-the-badge&logo=files&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![LibreOffice](https://img.shields.io/badge/LibreOffice-0E85CD?style=for-the-badge&logo=libreoffice&logoColor=white)

**A powerful, modern web application for converting files between various formats with advanced features and beautiful UI.**

[🌐 Live Demo](https://your-demo-url.com) | [📚 Documentation](#) | [🛠️ Installation](#installation) | [🤝 Contributing](#contributing)

</div>

---

## ✨ Features

### 🔄 **Multi-Format Conversion**
- **📄 Document to PDF**: Word, Excel, PowerPoint, OpenDocument formats
- **🖼️ Image Format Converter**: Convert between PNG, JPG, WebP, BMP, TIFF, GIF, ICO, TGA, EPS
- **📑 PDF Operations**: Merge multiple PDFs with password protection and custom ordering
- **📸 Images to PDF**: Combine multiple images into a single PDF document

### 🎨 **Modern Interface**
- **🎯 Drag & Drop**: Intuitive file upload with visual feedback
- **📱 Responsive Design**: Works flawlessly on desktop, tablet, and mobile
- **🌈 Beautiful UI**: Replit-inspired black and minimal design with smooth animations
- **⚡ Real-time Progress**: Live conversion status with animated progress bars

### 🔧 **Advanced Options**
- **⚙️ Quality Settings**: Choose conversion quality from 60% to 95%
- **🔒 Password Protection**: Secure your PDF files with custom passwords
- **📋 Batch Processing**: Convert multiple files simultaneously
- **📊 Conversion History**: Track and manage recent conversions
- **🗂️ File Ordering**: Custom file sequence for PDF merging

### 🛡️ **Security & Performance**
- **🔐 File Validation**: Comprehensive security checks
- **📏 Size Limits**: 50MB maximum file size
- **🧹 Auto Cleanup**: Automatic temporary file management
- **⚡ Fast Processing**: Optimized conversion algorithms

---

## 🏗️ Installation

### 🐍 **Local Development**

```bash
# Clone the repository
git clone https://github.com/deepink-team/fily-pro.git
cd fily-pro

# Install dependencies (use uv or pip)
pip install flask flask-sqlalchemy pillow pypdf2 python-docx python-pptx openpyxl pandas reportlab gunicorn

# Install LibreOffice for document conversion
# Ubuntu/Debian
sudo apt-get install libreoffice-headless

# macOS
brew install --cask libreoffice

# Run the application
python main.py
```

### 🐳 **Docker Deployment**

```bash
# Using Docker
docker build -t fily-pro .
docker run -p 5000:5000 fily-pro

# Using Docker Compose
docker-compose up -d
```

### ☁️ **Cloud Deployment**

#### **Replit**
1. Import this repository to Replit
2. Dependencies will be automatically installed
3. Click "Run" to start the application

#### **Heroku**
```bash
# Create Heroku app
heroku create your-app-name

# Add LibreOffice buildpack
heroku buildpacks:add --index 1 https://github.com/ello/heroku-buildpack-libreoffice

# Deploy
git push heroku main
```

---

## 🚦 Quick Start

1. **🎯 Choose Conversion Type**
   ```
   Document to PDF → Image Converter → PDF Merge → Images to PDF
   ```

2. **📁 Upload Files**
   - Drag & drop files into the upload area
   - Or click "Choose Files" to browse

3. **⚙️ Configure Settings**
   - Select target format (for image conversion)
   - Set quality level
   - Add password protection (for PDFs)

4. **🚀 Convert & Download**
   - Click "Convert Files"
   - Download individual files or all as ZIP

---

## 📊 Supported Formats

<table>
<tr>
<td>

**📄 Documents**
- Microsoft Office (DOC, DOCX, XLS, XLSX, PPT, PPTX)
- OpenDocument (ODT, ODS, ODP)
- Text formats (TXT, RTF, CSV)

</td>
<td>

**🖼️ Images**
- Common formats (PNG, JPG, JPEG, GIF, BMP)
- Advanced formats (TIFF, WebP, ICO, TGA, EPS)
- Graphics (SVG support coming soon)

</td>
</tr>
<tr>
<td>

**🌐 Web & Code**
- Web formats (HTML, XML)
- Documentation (Markdown, JSON)
- Source code (Python, JavaScript, CSS)

</td>
<td>

**📑 PDF Operations**
- PDF merging with custom order
- Password protection
- Quality optimization
- Batch processing

</td>
</tr>
</table>

---

## 🛠️ API Reference

### **Core Endpoints**

```http
GET  /                     # Main application interface
POST /upload               # File upload and conversion
GET  /download/<file_id>   # Download converted files
DELETE /delete/<file_id>   # Delete conversion records
```

### **Status Endpoints**

```http
GET /health               # Health check
GET /stats               # Conversion statistics
```

---

## 🏗️ Architecture

```
┌─ Frontend (Bootstrap + Vanilla JS)
├─ Flask Application
│  ├─ Routes (URL handling)
│  ├─ Converter (Format processing)
│  ├─ Storage (File management)
│  └─ Utils (Helper functions)
├─ LibreOffice (Document conversion)
└─ PIL/Pillow (Image processing)
```

---

## 🤝 Contributing

We love contributions! Here's how to get started:

1. **🍴 Fork** the repository
2. **🌿 Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **💻 Code** your changes
4. **✅ Test** thoroughly
5. **📤 Submit** a pull request

### **🧪 Development Setup**

```bash
# Install development dependencies
pip install flask flask-sqlalchemy pillow pypdf2 python-docx
pip install pytest black flake8

# Run tests
pytest

# Format code
black .

# Lint code
flake8 .
```

---

## 📈 Performance

- **⚡ Fast Conversion**: Optimized algorithms for quick processing
- **🔄 Batch Processing**: Handle multiple files efficiently
- **💾 Memory Management**: Smart memory usage for large files
- **🧹 Auto Cleanup**: Automatic temporary file cleanup

---

## 🔒 Security

- **🛡️ File Validation**: Comprehensive format and content checking
- **📏 Size Limits**: 50MB maximum file size
- **🔐 Secure Processing**: Sandboxed conversion environment
- **🧹 Data Privacy**: Automatic file cleanup after conversion

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🎉 Acknowledgments

<div align="center">

**🚀 Built with passion by [DeepInk Team](https://github.com/deepink-team)**

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/deepink-team)
[![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/deepink_team)

*Special thanks to the open-source community and all contributors!*

</div>

---

<div align="center">

**⭐ Star this repo if you find it useful! ⭐**

</div>

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