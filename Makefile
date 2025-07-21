# Fily Pro Development Makefile

.PHONY: help install dev test lint format clean build deploy

# Default target
help:
	@echo "Fily Pro Development Commands"
	@echo "============================="
	@echo "install     Install all dependencies"
	@echo "dev         Start development server"
	@echo "test        Run test suite"
	@echo "lint        Run code quality checks"
	@echo "format      Format code with black and isort"
	@echo "clean       Clean up temporary files"
	@echo "build       Build production application"
	@echo "deploy      Deploy to production"
	@echo "setup       Initial project setup"

# Development setup
install:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

setup: install
	mkdir -p uploads converted temp logs
	python -c "from app import app, db; app.app_context().push(); db.create_all()"
	@echo "✓ Fily Pro setup complete!"

# Development server
dev:
	python main.py

# Production server
prod:
	gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 main:app

# Testing
test:
	python -m pytest tests/ -v

test-coverage:
	python -m pytest tests/ --cov=. --cov-report=html --cov-report=term

# Code quality
lint:
	flake8 . --exclude=venv,__pycache__
	black --check .
	isort --check-only .
	mypy .

format:
	black .
	isort .

# Security checks
security:
	bandit -r . -x tests/
	safety check

# Database operations
db-init:
	python -c "from app import app, db; app.app_context().push(); db.create_all()"

db-reset:
	python -c "from app import app, db; app.app_context().push(); db.drop_all(); db.create_all()"

db-migrate:
	python -c "from app import app, db; app.app_context().push(); db.create_all()"

# File cleanup
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf dist
	rm -rf *.egg-info
	rm -f .coverage
	rm -f app.log

clean-files:
	rm -rf uploads/* converted/* temp/*
	@echo "✓ Cleaned up temporary files"

# Build and deployment
build:
	python setup.py sdist bdist_wheel

docker-build:
	docker build -t fily-pro:latest .

docker-run:
	docker run -p 5000:5000 -e SESSION_SECRET=dev-secret fily-pro:latest

# Development utilities
check-deps:
	pip-check
	safety check

update-deps:
	pip-review --auto

# Documentation
docs:
	python -m pydoc -w .
	@echo "✓ Documentation generated"

# Performance testing
load-test:
	locust -f tests/load_test.py --host=http://localhost:5000

# Backup and restore
backup:
	mkdir -p backups
	cp fily_pro.db backups/fily_pro_$(shell date +%Y%m%d_%H%M%S).db
	@echo "✓ Database backed up"

# Health checks
health:
	curl -f http://localhost:5000/api/system-health || exit 1

# Log management
logs:
	tail -f app.log

logs-error:
	grep ERROR app.log | tail -20

# System information
info:
	@echo "System Information"
	@echo "=================="
	@echo "Python: $(shell python --version)"
	@echo "Flask: $(shell python -c 'import flask; print(flask.__version__)')"
	@echo "LibreOffice: $(shell libreoffice --version 2>/dev/null || echo 'Not installed')"
	@echo "Disk Usage:"
	@du -sh uploads converted temp logs 2>/dev/null || echo "No data"
	@echo "Memory Usage:"
	@ps aux | grep python | grep -v grep | head -5

# Quick start for new developers
quickstart: setup
	@echo "🚀 Fily Pro Quick Start"
	@echo "======================"
	@echo "1. Run 'make dev' to start development server"
	@echo "2. Visit http://localhost:5000"
	@echo "3. Upload files and test conversions"
	@echo "4. Check 'make help' for more commands"

# CI/CD helpers
ci-test: install test lint security

ci-deploy: build
	@echo "Deploying to production..."
	# Add deployment commands here