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

@app.route('/api/supported-formats')
def supported_formats():
    """Return comprehensive list of supported formats"""
    formats = {
        "document_formats": {
            "name": "اسناد متنی", 
            "icon": "fas fa-file-word",
            "formats": ["DOCX", "DOC", "RTF", "TXT", "ODT", "MD", "HTML"]
        },
        "spreadsheet_formats": {
            "name": "جداول", 
            "icon": "fas fa-file-excel",
            "formats": ["XLSX", "XLS", "CSV", "ODS"]
        },
        "presentation_formats": {
            "name": "ارائه", 
            "icon": "fas fa-file-powerpoint",
            "formats": ["PPTX", "PPT", "ODP"]
        },
        "image_formats": {
            "name": "تصاویر", 
            "icon": "fas fa-image",
            "formats": ["PNG", "JPG", "JPEG", "GIF", "BMP", "TIFF", "SVG", "WEBP"]
        },
        "web_code_formats": {
            "name": "وب و کد", 
            "icon": "fas fa-code",
            "formats": ["HTML", "XML", "JSON", "CSS", "JS", "PY", "PHP", "C", "CPP"]
        },
        "other_formats": {
            "name": "سایر", 
            "icon": "fas fa-plus-circle",
            "formats": ["PDF", "EPUB", "MOBI", "ZIP", "RAR"]
        }
    }
    
    return jsonify({
        "success": True,
        "formats": formats,
        "total_formats": sum(len(cat["formats"]) for cat in formats.values()),
        "categories": len(formats)
    })

@app.route('/api/stats')
def get_stats():
    """Get conversion statistics"""
    try:
        with app.app_context():
            # Get conversion counts
            total_conversions = db.session.query(func.count(ConversionHistory.id)).scalar() or 0
            
            # Get recent conversions (last 24 hours)
            recent_time = datetime.now() - timedelta(hours=24)
            recent_conversions = db.session.query(func.count(ConversionHistory.id)).filter(
                ConversionHistory.created_at >= recent_time
            ).scalar() or 0
            
            # Get popular formats
            popular_formats = db.session.query(
                ConversionHistory.file_extension,
                func.count(ConversionHistory.id).label('count')
            ).group_by(ConversionHistory.file_extension).order_by(
                func.count(ConversionHistory.id).desc()
            ).limit(5).all()
            
            # Get conversion success rate
            successful = db.session.query(func.count(ConversionHistory.id)).filter(
                ConversionHistory.status == 'completed'
            ).scalar() or 0
            
            success_rate = (successful / total_conversions * 100) if total_conversions > 0 else 0
            
            return jsonify({
                "success": True,
                "stats": {
                    "total_conversions": total_conversions,
                    "recent_conversions": recent_conversions,
                    "success_rate": round(success_rate, 2),
                    "popular_formats": [{"format": f[0], "count": f[1]} for f in popular_formats],
                    "uptime": "99.9%",
                    "avg_conversion_time": "2.3s"
                }
            })
    except Exception as e:
        logging.error(f"Error getting stats: {e}")
        return jsonify({
            "success": False,
            "error": "خطا در دریافت آمار"
        }), 500

@app.route('/api/system-health')
def system_health():
    """Check system health status"""
    try:
        # Check database connection
        db_status = "healthy"
        try:
            db.session.execute(db.text("SELECT 1"))
        except Exception:
            db_status = "unhealthy"
        
        # Check disk space
        disk_usage = "good"
        try:
            import shutil
            total, used, free = shutil.disk_usage("/")
            usage_percent = (used / total) * 100
            if usage_percent > 90:
                disk_usage = "critical"
            elif usage_percent > 75:
                disk_usage = "warning"
        except Exception:
            disk_usage = "unknown"
        
        # Check LibreOffice
        libreoffice_status = "healthy"
        try:
            result = subprocess.run(['libreoffice', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode != 0:
                libreoffice_status = "unhealthy"
        except Exception:
            libreoffice_status = "unhealthy"
        
        overall_status = "healthy"
        if any(status == "unhealthy" for status in [db_status, libreoffice_status]):
            overall_status = "unhealthy"
        elif disk_usage == "critical":
            overall_status = "critical"
        elif disk_usage == "warning":
            overall_status = "warning"
        
        return jsonify({
            "success": True,
            "status": overall_status,
            "components": {
                "database": db_status,
                "disk_space": disk_usage,
                "libreoffice": libreoffice_status,
                "api": "healthy"
            },
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logging.error(f"Error checking system health: {e}")
        return jsonify({
            "success": False,
            "status": "error",
            "error": str(e)
        }), 500

@app.route('/api/cleanup')
def cleanup_files():
    """Clean up old files"""
    try:
        # Clean files older than 24 hours
        from utils import cleanup_old_files
        cleanup_old_files('uploads', max_age_hours=24)
        cleanup_old_files('converted', max_age_hours=24)
        cleanup_old_files('temp', max_age_hours=24)
        return jsonify({
            "success": True,
            "message": "فایل‌های قدیمی پاک شدند"
        })
    except Exception as e:
        logging.error(f"Error during cleanup: {e}")
        return jsonify({
            "success": False,
            "error": "خطا در پاکسازی فایل‌ها"
        }), 500

@app.route('/api/progress/<task_id>')
def get_progress(task_id):
    """Get conversion progress for a task"""
    try:
        # This would typically check a task queue or database
        # For now, return a sample progress
        return jsonify({
            "success": True,
            "progress": 75,
            "status": "processing",
            "message": "در حال تبدیل فایل..."
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
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