import os
import uuid
from datetime import datetime
from flask import render_template, request, jsonify, send_file, current_app, Response, stream_template
from werkzeug.utils import secure_filename
from app import app, db
from converter import convert_to_pdf
from models import ConversionHistory, SystemStats, FileMetadata
from utils import (
    calculate_file_hash, get_file_mime_type, get_image_dimensions,
    count_document_pages, count_words_in_text, validate_file_security,
    format_file_size, cleanup_old_files, set_conversion_progress,
    get_conversion_progress
)
from pathlib import Path
import logging
import json
import time

ALLOWED_EXTENSIONS = {
    'docx', 'doc', 'xlsx', 'xls', 'pptx', 'ppt', 
    'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'txt',
    'pdf', 'rtf', 'odt', 'ods', 'odp', 'csv',
    'html', 'htm', 'xml', 'json', 'md', 'py', 'js', 'css'
}

# PDF operation modes
PDF_OPERATIONS = {
    'pdf-to-word': 'Convert PDF to Word',
    'pdf-password': 'Add Password to PDF', 
    'pdf-merge': 'Merge Multiple PDFs',
    'any-to-pdf': 'Convert Any File to PDF'
}

def allowed_file(filename):
    if not filename or '.' not in filename:
        return False
    parts = filename.rsplit('.', 1)
    if len(parts) < 2:
        return False
    return parts[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file selected'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not supported'}), 400
        
        # Generate unique filename
        file_id = str(uuid.uuid4())
        original_filename = secure_filename(file.filename or 'untitled')
        
        # Handle file extension safely
        parts = original_filename.rsplit('.', 1)
        if len(parts) < 2:
            return jsonify({'error': 'File must have an extension'}), 400
        file_extension = parts[1].lower()
        upload_filename = f"{file_id}.{file_extension}"
        
        # Save uploaded file
        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], upload_filename)
        file.save(upload_path)
        
        logging.info(f"File uploaded: {upload_filename}")
        
        # Get file size for progress tracking
        file_size = os.path.getsize(upload_path)
        
        return jsonify({
            'file_id': file_id,
            'original_filename': original_filename,
            'file_size': file_size,
            'file_extension': file_extension,
            'message': 'File uploaded successfully'
        })
    
    except Exception as e:
        logging.error(f"Upload error: {str(e)}")
        return jsonify({'error': 'Upload failed'}), 500

@app.route('/batch-upload', methods=['POST'])
def batch_upload():
    """Handle multiple file uploads"""
    try:
        files = request.files.getlist('files')
        if not files:
            return jsonify({'error': 'No files selected'}), 400
        
        results = []
        for file in files:
            if file.filename and allowed_file(file.filename):
                file_id = str(uuid.uuid4())
                original_filename = secure_filename(file.filename)
                parts = original_filename.rsplit('.', 1)
                if len(parts) >= 2:
                    file_extension = parts[1].lower()
                    upload_filename = f"{file_id}.{file_extension}"
                    upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], upload_filename)
                    file.save(upload_path)
                    file_size = os.path.getsize(upload_path)
                    
                    results.append({
                        'file_id': file_id,
                        'original_filename': original_filename,
                        'file_size': file_size,
                        'file_extension': file_extension
                    })
        
        return jsonify({
            'files': results,
            'message': f'Successfully uploaded {len(results)} files'
        })
    
    except Exception as e:
        logging.error(f"Batch upload error: {str(e)}")
        return jsonify({'error': 'Batch upload failed'}), 500

@app.route('/convert', methods=['POST'])
def convert_file():
    try:
        data = request.get_json()
        file_id = data.get('file_id')
        original_filename = data.get('original_filename')
        
        if not file_id or not original_filename:
            return jsonify({'error': 'Missing file information'}), 400
        
        # Find the uploaded file
        upload_files = os.listdir(current_app.config['UPLOAD_FOLDER'])
        upload_file = None
        for f in upload_files:
            if f.startswith(file_id):
                upload_file = f
                break
        
        if not upload_file:
            return jsonify({'error': 'File not found'}), 404
        
        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], upload_file)
        
        # Get conversion options
        password = data.get('password', None)
        quality = data.get('quality', 'high')
        output_name = data.get('output_name', None)
        
        # Convert to PDF
        if output_name:
            # Ensure PDF extension
            if not output_name.lower().endswith('.pdf'):
                output_name += '.pdf'
            pdf_filename = f"{file_id}_{secure_filename(output_name)}"
        else:
            pdf_filename = f"{file_id}.pdf"
        pdf_path = os.path.join(current_app.config['CONVERTED_FOLDER'], pdf_filename)
        
        success = convert_to_pdf(upload_path, pdf_path, original_filename, password=password, quality=quality)
        
        if success:
            # Clean up uploaded file
            os.remove(upload_path)
            
            return jsonify({
                'file_id': file_id,
                'pdf_filename': pdf_filename,
                'message': 'Conversion successful'
            })
        else:
            return jsonify({'error': 'Conversion failed'}), 500
    
    except Exception as e:
        logging.error(f"Conversion error: {str(e)}")
        return jsonify({'error': 'Conversion failed'}), 500

@app.route('/download/<file_id>')
def download_file(file_id):
    try:
        # Try with .pdf extension first
        pdf_filename = f"{file_id}.pdf"
        pdf_path = os.path.join(current_app.config['CONVERTED_FOLDER'], pdf_filename)
        
        # If not found, try without extension (in case file_id already includes .pdf)
        if not os.path.exists(pdf_path):
            pdf_path = os.path.join(current_app.config['CONVERTED_FOLDER'], file_id)
            pdf_filename = file_id
        
        # If still not found, search for any file starting with file_id
        if not os.path.exists(pdf_path):
            converted_folder = current_app.config['CONVERTED_FOLDER']
            for filename in os.listdir(converted_folder):
                if filename.startswith(file_id):
                    pdf_path = os.path.join(converted_folder, filename)
                    pdf_filename = filename
                    break
        
        if not os.path.exists(pdf_path):
            return jsonify({'error': 'File not found'}), 404
        
        return send_file(pdf_path, as_attachment=True, download_name=f"converted_{pdf_filename}")
    
    except Exception as e:
        logging.error(f"Download error: {str(e)}")
        return jsonify({'error': 'Download failed'}), 500

@app.route('/preview/<file_id>')
def preview_file(file_id):
    """Generate preview image for uploaded file"""
    try:
        upload_files = os.listdir(current_app.config['UPLOAD_FOLDER'])
        upload_file = None
        for f in upload_files:
            if f.startswith(file_id):
                upload_file = f
                break
        
        if not upload_file:
            return jsonify({'error': 'File not found'}), 404
        
        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], upload_file)
        file_extension = Path(upload_path).suffix.lower()
        
        # Generate preview based on file type
        if file_extension in ['.png', '.jpg', '.jpeg', '.gif', '.bmp']:
            return send_file(upload_path, mimetype='image/*')
        elif file_extension == '.txt':
            with open(upload_path, 'r', encoding='utf-8') as f:
                content = f.read()[:500] + '...' if len(f.read()) > 500 else f.read()
            return jsonify({'preview': content, 'type': 'text'})
        else:
            return jsonify({'preview': 'Preview not available for this file type', 'type': 'info'})
    
    except Exception as e:
        logging.error(f"Preview error: {str(e)}")
        return jsonify({'error': 'Preview failed'}), 500

@app.route('/history')
def conversion_history():
    """Get conversion history"""
    try:
        converted_files = []
        if os.path.exists(current_app.config['CONVERTED_FOLDER']):
            for file in os.listdir(current_app.config['CONVERTED_FOLDER']):
                if file.endswith('.pdf'):
                    file_path = os.path.join(current_app.config['CONVERTED_FOLDER'], file)
                    stat = os.stat(file_path)
                    converted_files.append({
                        'filename': file,
                        'size': stat.st_size,
                        'created': stat.st_mtime
                    })
        
        # Sort by creation time (newest first) and limit to 5
        converted_files.sort(key=lambda x: x['created'], reverse=True)
        
        return jsonify({'files': converted_files[:5]})  # Last 5 files
    
    except Exception as e:
        logging.error(f"History error: {str(e)}")
        return jsonify({'error': 'Failed to load history'}), 500

@app.route('/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    """Delete a converted file"""
    try:
        # Ensure filename is safe
        filename = secure_filename(filename)
        if not filename.endswith('.pdf'):
            filename += '.pdf'
            
        file_path = os.path.join(current_app.config['CONVERTED_FOLDER'], filename)
        
        if os.path.exists(file_path):
            os.remove(file_path)
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'File not found'}), 404
    
    except Exception as e:
        logging.error(f"File deletion error: {str(e)}")
        return jsonify({'error': 'Failed to delete file'}), 500

@app.errorhandler(413)
def too_large(e):
    return jsonify({'error': 'File too large. Maximum size is 50MB.'}), 413
