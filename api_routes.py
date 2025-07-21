from flask import jsonify, request, Response, render_template, current_app
from app import app, db
from models import ConversionHistory, SystemStats, FileMetadata
from utils import cleanup_old_files, format_file_size
from datetime import datetime, timedelta
from sqlalchemy import func
import json
import logging
import os
import subprocess


@app.route('/api/stats')
def get_usage_stats():
    """Get usage statistics and analytics"""
    try:
        # Get today's stats
        today = datetime.utcnow().date()
        today_stats = SystemStats.query.filter_by(date=today).first()
        
        # Get recent conversions
        recent_conversions = ConversionHistory.query.filter(
            ConversionHistory.created_at >= datetime.utcnow() - timedelta(days=7)
        ).order_by(ConversionHistory.created_at.desc()).limit(50).all()
        
        # Calculate summary statistics
        total_conversions = ConversionHistory.query.count()
        successful_conversions = ConversionHistory.query.filter_by(status='completed').count()
        
        # Most popular formats
        popular_formats = db.session.query(
            ConversionHistory.file_extension,
            func.count(ConversionHistory.id).label('count')
        ).group_by(ConversionHistory.file_extension).order_by(
            func.count(ConversionHistory.id).desc()
        ).limit(5).all()
        
        # Conversion types
        conversion_types = db.session.query(
            ConversionHistory.conversion_type,
            func.count(ConversionHistory.id).label('count')
        ).group_by(ConversionHistory.conversion_type).order_by(
            func.count(ConversionHistory.id).desc()
        ).all()
        
        return jsonify({
            'total_conversions': total_conversions,
            'successful_conversions': successful_conversions,
            'success_rate': (successful_conversions / total_conversions * 100) if total_conversions > 0 else 0,
            'today_stats': today_stats.to_dict() if today_stats else None,
            'recent_conversions': [conv.to_dict() for conv in recent_conversions],
            'popular_formats': [{'format': fmt[0], 'count': fmt[1]} for fmt in popular_formats],
            'conversion_types': [{'type': ct[0], 'count': ct[1]} for ct in conversion_types]
        })
        
    except Exception as e:
        logging.error(f"Error fetching stats: {e}")
        return jsonify({'error': 'Failed to fetch statistics'}), 500


@app.route('/api/conversion-history')
def get_conversion_history():
    """Get user's conversion history"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        conversions = ConversionHistory.query.order_by(
            ConversionHistory.created_at.desc()
        ).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return jsonify({
            'conversions': [conv.to_dict() for conv in conversions.items],
            'total': conversions.total,
            'pages': conversions.pages,
            'current_page': page,
            'has_next': conversions.has_next,
            'has_prev': conversions.has_prev
        })
        
    except Exception as e:
        logging.error(f"Error fetching conversion history: {e}")
        return jsonify({'error': 'Failed to fetch conversion history'}), 500


@app.route('/api/file-metadata/<file_id>')
def get_file_metadata(file_id):
    """Get detailed metadata for a file"""
    try:
        metadata = FileMetadata.query.filter_by(file_id=file_id).first()
        if not metadata:
            return jsonify({'error': 'File metadata not found'}), 404
        
        return jsonify(metadata.to_dict())
        
    except Exception as e:
        logging.error(f"Error fetching file metadata: {e}")
        return jsonify({'error': 'Failed to fetch file metadata'}), 500


@app.route('/api/cleanup-old-files', methods=['POST'])
def cleanup_old_files_api():
    """Clean up old uploaded and converted files"""
    try:
        max_age_hours = request.json.get('max_age_hours', 24) if request.is_json else 24
        
        # Clean up file system
        cleanup_old_files(current_app.config['UPLOAD_FOLDER'], max_age_hours)
        cleanup_old_files(current_app.config['CONVERTED_FOLDER'], max_age_hours)
        
        # Clean up database records for files older than 7 days
        cutoff_date = datetime.utcnow() - timedelta(days=7)
        old_conversions = ConversionHistory.query.filter(
            ConversionHistory.created_at < cutoff_date
        ).all()
        
        for conversion in old_conversions:
            db.session.delete(conversion)
        
        db.session.commit()
        
        return jsonify({
            'message': f'Cleaned up files older than {max_age_hours} hours',
            'cleaned_records': len(old_conversions)
        })
        
    except Exception as e:
        logging.error(f"Error during cleanup: {e}")
        return jsonify({'error': 'Cleanup failed'}), 500


@app.route('/api/system-health')
def system_health():
    """Check system health and status"""
    try:
        # Check database connection
        try:
            db.session.execute('SELECT 1')
            db_status = 'healthy'
        except Exception:
            db_status = 'unhealthy'
        
        # Check file system
        upload_folder_exists = os.path.exists(current_app.config['UPLOAD_FOLDER'])
        converted_folder_exists = os.path.exists(current_app.config['CONVERTED_FOLDER'])
        
        # Check LibreOffice availability
        import subprocess
        try:
            result = subprocess.run(['libreoffice', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            libreoffice_status = 'available' if result.returncode == 0 else 'unavailable'
            libreoffice_version = result.stdout.strip() if result.returncode == 0 else None
        except Exception:
            libreoffice_status = 'unavailable'
            libreoffice_version = None
        
        # Get disk usage
        upload_folder = current_app.config['UPLOAD_FOLDER']
        converted_folder = current_app.config['CONVERTED_FOLDER']
        
        upload_size = sum(os.path.getsize(os.path.join(upload_folder, f)) 
                         for f in os.listdir(upload_folder) 
                         if os.path.isfile(os.path.join(upload_folder, f)))
        
        converted_size = sum(os.path.getsize(os.path.join(converted_folder, f)) 
                           for f in os.listdir(converted_folder) 
                           if os.path.isfile(os.path.join(converted_folder, f)))
        
        return jsonify({
            'status': 'healthy' if all([
                db_status == 'healthy',
                upload_folder_exists,
                converted_folder_exists,
                libreoffice_status == 'available'
            ]) else 'degraded',
            'database': db_status,
            'file_system': {
                'upload_folder': upload_folder_exists,
                'converted_folder': converted_folder_exists,
                'upload_size': format_file_size(upload_size),
                'converted_size': format_file_size(converted_size)
            },
            'libreoffice': {
                'status': libreoffice_status,
                'version': libreoffice_version
            },
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        logging.error(f"Error checking system health: {e}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500


@app.route('/api/conversion-progress/<file_id>')
def get_conversion_progress_api(file_id):
    """Get real-time conversion progress for a file"""
    try:
        progress = get_conversion_progress(file_id)
        if progress:
            return jsonify(progress.to_dict())
        else:
            # Check database for completed conversion
            conversion = ConversionHistory.query.filter_by(file_id=file_id).first()
            if conversion:
                return jsonify({
                    'file_id': file_id,
                    'progress': 100 if conversion.status == 'completed' else 0,
                    'status': conversion.status,
                    'message': conversion.error_message or 'Conversion completed',
                    'duration': 0
                })
            else:
                return jsonify({'error': 'Conversion not found'}), 404
                
    except Exception as e:
        logging.error(f"Error fetching conversion progress: {e}")
        return jsonify({'error': 'Failed to fetch progress'}), 500


@app.route('/stream-progress')
def stream_progress():
    """Server-Sent Events stream for real-time progress updates"""
    def generate():
        try:
            while True:
                # Get all active conversions
                active_conversions = ConversionHistory.query.filter(
                    ConversionHistory.status.in_(['pending', 'converting'])
                ).all()
                
                for conversion in active_conversions:
                    progress = get_conversion_progress(conversion.file_id)
                    if progress:
                        yield f"data: {json.dumps(progress.to_dict())}\n\n"
                
                time.sleep(1)  # Update every second
                
        except GeneratorExit:
            pass
        except Exception as e:
            logging.error(f"Error in progress stream: {e}")
            yield f"data: {json.dumps({'error': 'Stream error'})}\n\n"
    
    return Response(generate(), mimetype='text/plain', headers={
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'text/event-stream'
    })


@app.route('/api/supported-formats')
def get_supported_formats():
    """Get list of supported file formats with details"""
    formats = {
        'documents': {
            'extensions': ['.doc', '.docx', '.rtf', '.odt', '.txt', '.md'],
            'description': 'Text documents and word processing files',
            'mime_types': [
                'application/msword',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'application/rtf',
                'application/vnd.oasis.opendocument.text',
                'text/plain',
                'text/markdown'
            ]
        },
        'spreadsheets': {
            'extensions': ['.xls', '.xlsx', '.ods', '.csv'],
            'description': 'Spreadsheets and data files',
            'mime_types': [
                'application/vnd.ms-excel',
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                'application/vnd.oasis.opendocument.spreadsheet',
                'text/csv'
            ]
        },
        'presentations': {
            'extensions': ['.ppt', '.pptx', '.odp'],
            'description': 'Presentation files',
            'mime_types': [
                'application/vnd.ms-powerpoint',
                'application/vnd.openxmlformats-officedocument.presentationml.presentation',
                'application/vnd.oasis.opendocument.presentation'
            ]
        },
        'images': {
            'extensions': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'],
            'description': 'Image files',
            'mime_types': [
                'image/jpeg',
                'image/png',
                'image/gif',
                'image/bmp',
                'image/tiff'
            ]
        },
        'web': {
            'extensions': ['.html', '.htm', '.xml'],
            'description': 'Web and markup files',
            'mime_types': [
                'text/html',
                'application/xml',
                'text/xml'
            ]
        },
        'code': {
            'extensions': ['.py', '.js', '.css', '.json'],
            'description': 'Code and data files',
            'mime_types': [
                'text/x-python',
                'application/javascript',
                'text/css',
                'application/json'
            ]
        }
    }
    
    return jsonify({
        'formats': formats,
        'total_formats': sum(len(category['extensions']) for category in formats.values()),
        'max_file_size': current_app.config.get('MAX_CONTENT_LENGTH', 50 * 1024 * 1024)
    })


@app.errorhandler(413)
def file_too_large(error):
    """Handle file too large error"""
    return jsonify({
        'error': 'File too large',
        'message': 'Maximum file size is 50MB',
        'max_size': current_app.config.get('MAX_CONTENT_LENGTH', 50 * 1024 * 1024)
    }), 413


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    if request.path.startswith('/api/'):
        return jsonify({'error': 'API endpoint not found'}), 404
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    db.session.rollback()
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Internal server error'}), 500
    return render_template('500.html'), 500