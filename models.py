from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
import os


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class ConversionHistory(db.Model):
    """Track conversion history for analytics and user experience"""
    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.String(36), unique=True, nullable=False)  # UUID
    original_filename = db.Column(db.String(255), nullable=False)
    file_extension = db.Column(db.String(10), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)  # in bytes
    conversion_type = db.Column(db.String(50), nullable=False)
    quality_setting = db.Column(db.String(20), default='high')
    status = db.Column(db.String(20), default='pending')  # pending, completed, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    error_message = db.Column(db.Text)
    ip_address = db.Column(db.String(45))  # Support IPv6
    user_agent = db.Column(db.String(500))
    
    def __repr__(self):
        return f'<ConversionHistory {self.original_filename}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'file_id': self.file_id,
            'original_filename': self.original_filename,
            'file_extension': self.file_extension,
            'file_size': self.file_size,
            'conversion_type': self.conversion_type,
            'quality_setting': self.quality_setting,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'error_message': self.error_message
        }


class SystemStats(db.Model):
    """Track system statistics and usage metrics"""
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=datetime.utcnow().date, unique=True)
    total_conversions = db.Column(db.Integer, default=0)
    successful_conversions = db.Column(db.Integer, default=0)
    failed_conversions = db.Column(db.Integer, default=0)
    total_file_size = db.Column(db.BigInteger, default=0)  # in bytes
    avg_conversion_time = db.Column(db.Float, default=0)  # in seconds
    most_popular_format = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<SystemStats {self.date}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date.isoformat(),
            'total_conversions': self.total_conversions,
            'successful_conversions': self.successful_conversions,
            'failed_conversions': self.failed_conversions,
            'total_file_size': self.total_file_size,
            'avg_conversion_time': self.avg_conversion_time,
            'most_popular_format': self.most_popular_format,
            'success_rate': (self.successful_conversions / self.total_conversions * 100) if self.total_conversions > 0 else 0
        }


class FileMetadata(db.Model):
    """Store additional metadata about uploaded files"""
    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.String(36), unique=True, nullable=False)
    mime_type = db.Column(db.String(100))
    checksum = db.Column(db.String(64))  # SHA-256 hash
    page_count = db.Column(db.Integer)  # For documents
    word_count = db.Column(db.Integer)  # For text documents
    image_dimensions = db.Column(db.String(20))  # WxH for images
    has_password = db.Column(db.Boolean, default=False)
    language_detected = db.Column(db.String(10))  # Language code
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<FileMetadata {self.file_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'file_id': self.file_id,
            'mime_type': self.mime_type,
            'checksum': self.checksum,
            'page_count': self.page_count,
            'word_count': self.word_count,
            'image_dimensions': self.image_dimensions,
            'has_password': self.has_password,
            'language_detected': self.language_detected,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }