import os
import uuid
import json
import logging
from datetime import datetime
from flask import render_template, request, redirect, url_for, flash, jsonify, send_file, session
from werkzeug.utils import secure_filename
from app import app
from converter import convert_to_pdf, convert_image_format, merge_pdfs, convert_multiple_images_to_pdf
from storage import storage

@app.route('/privacy')
def privacy():
    """Privacy Policy page"""
    return render_template('privacy.html')

@app.route('/terms')
def terms():
    """Terms of Service page"""
    return render_template('terms.html')

# Allowed file extensions
ALLOWED_EXTENSIONS = {
    'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 
    'txt', 'rtf', 'odt', 'ods', 'odp', 'csv',
    'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'tif', 'webp', 
    'ico', 'tga', 'jp2', 'jpeg2000', 'eps', 'svg', 'psd',
    'md', 'html', 'pdf'
}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Main page with file upload interface"""
    recent_conversions = storage.get_recent_conversions(5)
    return render_template('index.html', recent_conversions=recent_conversions)

@app.route('/upload', methods=['POST'])
def upload_files():
    """Handle file upload and conversion"""
    if 'files[]' not in request.files:
        return jsonify({'success': False, 'error': 'No files selected'})
    
    files = request.files.getlist('files[]')
    conversion_type = request.form.get('conversion_type', 'document-to-pdf')
    quality = request.form.get('quality', 'high')
    custom_name = request.form.get('custom_name', '')
    
    if not files or all(file.filename == '' for file in files):
        return jsonify({'success': False, 'error': 'No files selected'})
    
    results = []
    uploaded_files = []  # Keep track of uploaded files for batch processing
    
    for file in files:
        if file and allowed_file(file.filename):
            try:
                # Generate unique filename
                file_id = str(uuid.uuid4())
                filename = secure_filename(file.filename or 'unknown_file')
                file_extension = filename.rsplit('.', 1)[1].lower() if '.' in filename else 'unknown'
                
                # Save original file
                original_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{file_id}_{filename}")
                file.save(original_path)
                uploaded_files.append({
                    'path': original_path,
                    'id': file_id,
                    'name': filename,
                    'extension': file_extension
                })
                
                # Handle different conversion types
                if conversion_type == 'image-converter':
                    # Image format conversion
                    target_format = request.form.get('target_format', 'jpg')
                    img_quality = int(request.form.get('image_quality', 95))
                    output_filename = custom_name if custom_name else f"{file_id}_converted"
                    converted_path = os.path.join(app.config['CONVERTED_FOLDER'], output_filename)
                    success, final_path = convert_image_format(original_path, converted_path, target_format, quality=img_quality)
                    if success and final_path:
                        converted_path = final_path
                elif conversion_type == 'merge-pdf':
                    # PDF merging - skip individual processing
                    continue
                elif conversion_type == 'images-to-pdf':
                    # Images to PDF - skip individual processing
                    continue
                else:
                    # Regular PDF conversion
                    output_filename = custom_name if custom_name else f"{file_id}_converted.pdf"
                    converted_path = os.path.join(app.config['CONVERTED_FOLDER'], output_filename)
                    success = convert_to_pdf(original_path, converted_path, filename, quality=quality)
                
                if conversion_type in ['merge-pdf', 'images-to-pdf']:
                    # Skip individual file processing for batch types
                    continue
                elif success and os.path.exists(converted_path):
                    # Store conversion record
                    conversion_data = {
                        'file_id': file_id,
                        'original_filename': filename,
                        'file_extension': file_extension,
                        'file_size': os.path.getsize(original_path),
                        'conversion_type': conversion_type,
                        'quality_setting': quality,
                        'status': 'completed',
                        'converted_path': converted_path,
                        'created_at': datetime.now().isoformat()
                    }
                    storage.add_conversion(conversion_data)
                    
                    results.append({
                        'success': True,
                        'filename': filename,
                        'download_url': url_for('download_file', file_id=file_id),
                        'file_id': file_id
                    })
                    
                    logging.info(f"Successfully converted {filename} to PDF")
                    
                else:
                    # Store failed conversion
                    conversion_data = {
                        'file_id': file_id,
                        'original_filename': filename,
                        'file_extension': file_extension,
                        'file_size': os.path.getsize(original_path),
                        'conversion_type': conversion_type,
                        'quality_setting': quality,
                        'status': 'failed',
                        'error_message': 'Conversion failed',
                        'created_at': datetime.now().isoformat()
                    }
                    storage.add_conversion(conversion_data)
                    
                    results.append({
                        'success': False,
                        'filename': filename,
                        'error': 'Conversion failed'
                    })
                    
            except Exception as e:
                logging.error(f"Error processing file {file.filename}: {str(e)}")
                results.append({
                    'success': False,
                    'filename': file.filename,
                    'error': str(e)
                })
        else:
            results.append({
                'success': False,
                'filename': file.filename,
                'error': 'File type not supported'
            })
    
    # Handle batch processing for special conversion types
    if conversion_type == 'merge-pdf' and uploaded_files:
        # Merge PDFs
        pdf_files = [f for f in uploaded_files if f['extension'] == 'pdf']
        if len(pdf_files) > 1:
            batch_id = str(uuid.uuid4())
            output_filename = custom_name if custom_name else f"{batch_id}_merged.pdf"
            merged_path = os.path.join(app.config['CONVERTED_FOLDER'], output_filename)
            
            # Get advanced merge settings
            file_order = request.form.get('file_order')  # Comma-separated indices
            pdf_passwords = {}  # Dictionary for password-protected PDFs
            
            # Parse file order if provided
            order_indices = None
            if file_order:
                try:
                    order_indices = [int(x.strip()) for x in file_order.split(',') if x.strip().isdigit()]
                except:
                    order_indices = None
            
            # Get passwords for each file if provided
            for i, pdf_file in enumerate(pdf_files):
                password_key = f'pdf_password_{i}'
                password = request.form.get(password_key)
                if password:
                    pdf_passwords[pdf_file['path']] = password
            
            pdf_paths = [f['path'] for f in pdf_files]
            success = merge_pdfs(pdf_paths, merged_path, file_order=order_indices, passwords=pdf_passwords)
            
            if success:
                results.append({
                    'success': True,
                    'filename': 'Merged PDF',
                    'download_url': url_for('download_file', file_id=batch_id),
                    'file_id': batch_id
                })
            else:
                results.append({
                    'success': False,
                    'filename': 'PDF Merge',
                    'error': 'Failed to merge PDF files'
                })
        else:
            results.append({
                'success': False,
                'filename': 'PDF Merge',
                'error': 'Need at least 2 PDF files to merge'
            })
            
    elif conversion_type == 'images-to-pdf' and uploaded_files:
        # Convert multiple images to PDF
        image_files = [f for f in uploaded_files if f['extension'] in ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff']]
        if len(image_files) > 0:
            batch_id = str(uuid.uuid4())
            output_filename = custom_name if custom_name else f"{batch_id}_images.pdf"
            images_pdf_path = os.path.join(app.config['CONVERTED_FOLDER'], output_filename)
            
            image_paths = [f['path'] for f in image_files]
            success = convert_multiple_images_to_pdf(image_paths, images_pdf_path, quality)
            
            if success:
                results.append({
                    'success': True,
                    'filename': f'Images to PDF ({len(image_files)} images)',
                    'download_url': url_for('download_file', file_id=batch_id),
                    'file_id': batch_id
                })
            else:
                results.append({
                    'success': False,
                    'filename': 'Images to PDF',
                    'error': 'Failed to convert images to PDF'
                })
        else:
            results.append({
                'success': False,
                'filename': 'Images to PDF',
                'error': 'No valid image files found'
            })
    
    return jsonify({'results': results})

@app.route('/download/<file_id>')
def download_file(file_id):
    """Download converted PDF file"""
    try:
        # Search for the converted file
        converted_folder = app.config['CONVERTED_FOLDER']
        for filename in os.listdir(converted_folder):
            if filename.startswith(file_id):
                file_path = os.path.join(converted_folder, filename)
                if os.path.exists(file_path):
                    return send_file(file_path, as_attachment=True, download_name=filename)
        
        return jsonify({'success': False, 'error': 'File not found'}), 404
        
    except Exception as e:
        logging.error(f"Error downloading file {file_id}: {str(e)}")
        return jsonify({'success': False, 'error': 'Download failed'}), 500

@app.route('/api/recent-conversions')
def get_recent_conversions():
    """Get recent conversion history"""
    try:
        conversions = storage.get_recent_conversions(10)
        return jsonify({
            'success': True,
            'conversions': conversions
        })
    except Exception as e:
        logging.error(f"Error getting recent conversions: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to get recent conversions'
        }), 500

@app.route('/api/stats')
def get_stats():
    """Get conversion statistics"""
    try:
        stats = storage.get_stats()
        return jsonify({
            'success': True,
            'stats': stats
        })
    except Exception as e:
        logging.error(f"Error getting stats: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to get statistics'
        }), 500

@app.route('/api/supported-formats')
def get_supported_formats():
    """Get supported file formats"""
    formats = {
        "documents": {
            "name": "Documents",
            "icon": "fas fa-file-word",
            "formats": ["DOC", "DOCX", "RTF", "TXT", "ODT", "MD"]
        },
        "spreadsheets": {
            "name": "Spreadsheets", 
            "icon": "fas fa-file-excel",
            "formats": ["XLS", "XLSX", "CSV", "ODS"]
        },
        "presentations": {
            "name": "Presentations",
            "icon": "fas fa-file-powerpoint", 
            "formats": ["PPT", "PPTX", "ODP"]
        },
        "images": {
            "name": "Images",
            "icon": "fas fa-image",
            "formats": ["PNG", "JPG", "JPEG", "GIF", "BMP", "TIFF"]
        },
        "other_formats": {
            "name": "Other", 
            "icon": "fas fa-plus-circle",
            "formats": ["HTML", "XML"]
        }
    }
    
    return jsonify({
        "success": True,
        "formats": formats,
        "total_formats": sum(len(cat["formats"]) for cat in formats.values()),
        "categories": len(formats)
    })

@app.route('/api/delete-conversion/<file_id>', methods=['DELETE'])
def delete_conversion(file_id):
    """Delete a conversion record and associated files"""
    try:
        files_deleted = 0
        
        # Remove files from both folders
        for folder in [app.config['UPLOAD_FOLDER'], app.config['CONVERTED_FOLDER']]:
            if os.path.exists(folder):
                for filename in os.listdir(folder):
                    if filename.startswith(file_id):
                        file_path = os.path.join(folder, filename)
                        if os.path.exists(file_path):
                            os.remove(file_path)
                            files_deleted += 1
                            logging.info(f"Deleted file: {file_path}")
        
        # Remove from storage records
        storage.delete_conversion(file_id)
        
        return jsonify({
            'success': True,
            'message': f'Successfully deleted {files_deleted} file(s)',
            'files_deleted': files_deleted
        })
        
    except Exception as e:
        logging.error(f"Error deleting conversion {file_id}: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Failed to delete file: {str(e)}'
        }), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    if request.path.startswith('/api/'):
        return jsonify({
            "success": False,
            "error": "API endpoint not found",
            "code": 404
        }), 404
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    if request.path.startswith('/api/'):
        return jsonify({
            "success": False,
            "error": "Internal server error",
            "code": 500
        }), 500
    return render_template('500.html'), 500

@app.errorhandler(413)
def too_large(error):
    return jsonify({
        "success": False,
        "error": "File too large. Maximum size is 50MB",
        "code": 413
    }), 413