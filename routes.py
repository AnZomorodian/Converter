import os
import uuid
from flask import render_template, request, jsonify, send_file, current_app
from werkzeug.utils import secure_filename
from app import app
from converter import convert_to_pdf
import logging

ALLOWED_EXTENSIONS = {
    'docx', 'doc', 'xlsx', 'xls', 'pptx', 'ppt', 
    'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'txt'
}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        file_extension = original_filename.rsplit('.', 1)[1].lower()
        upload_filename = f"{file_id}.{file_extension}"
        
        # Save uploaded file
        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], upload_filename)
        file.save(upload_path)
        
        logging.info(f"File uploaded: {upload_filename}")
        
        return jsonify({
            'file_id': file_id,
            'original_filename': original_filename,
            'message': 'File uploaded successfully'
        })
    
    except Exception as e:
        logging.error(f"Upload error: {str(e)}")
        return jsonify({'error': 'Upload failed'}), 500

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
        
        # Convert to PDF
        pdf_filename = f"{file_id}.pdf"
        pdf_path = os.path.join(current_app.config['CONVERTED_FOLDER'], pdf_filename)
        
        success = convert_to_pdf(upload_path, pdf_path, original_filename)
        
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
        pdf_filename = f"{file_id}.pdf"
        pdf_path = os.path.join(current_app.config['CONVERTED_FOLDER'], pdf_filename)
        
        if not os.path.exists(pdf_path):
            return jsonify({'error': 'File not found'}), 404
        
        return send_file(pdf_path, as_attachment=True, download_name=f"converted_{pdf_filename}")
    
    except Exception as e:
        logging.error(f"Download error: {str(e)}")
        return jsonify({'error': 'Download failed'}), 500

@app.errorhandler(413)
def too_large(e):
    return jsonify({'error': 'File too large. Maximum size is 50MB.'}), 413
