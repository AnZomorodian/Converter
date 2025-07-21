import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.middleware.proxy_fix import ProxyFix
from models import db

# Set up enhanced logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Database configuration
database_url = os.environ.get("DATABASE_URL")
if database_url:
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
else:
    # Fallback to SQLite for development
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///fily_pro.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Configure upload settings
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['CONVERTED_FOLDER'] = 'converted'
app.config['TEMP_FOLDER'] = 'temp'

# Security settings
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 43200  # 12 hours
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Ensure directories exist
for folder in [app.config['UPLOAD_FOLDER'], app.config['CONVERTED_FOLDER'], app.config['TEMP_FOLDER']]:
    os.makedirs(folder, exist_ok=True)

# Initialize database
db.init_app(app)

with app.app_context():
    # Create tables
    db.create_all()
    logging.info("Database tables created successfully")

# Import routes after app creation
from routes import *
from api_routes import *


