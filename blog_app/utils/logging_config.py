"""
Logging configuration for the application
"""
import logging
from logging.handlers import RotatingFileHandler
import os


def configure_logging(app):
    """Configure application logging"""
    
    # Skip logging configuration in testing mode
    if app.config.get('TESTING'):
        return
    
    # Create logs directory if it doesn't exist
    logs_dir = os.path.join(app.instance_path, 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    
    # Configure file handler with rotation
    log_file = os.path.join(logs_dir, 'blog_app.log')
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=1024 * 1024,  # 1MB
        backupCount=10
    )
    
    # Set log format
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )
    file_handler.setFormatter(formatter)
    
    # Set log level based on debug mode
    if app.debug:
        file_handler.setLevel(logging.DEBUG)
        app.logger.setLevel(logging.DEBUG)
    else:
        file_handler.setLevel(logging.INFO)
        app.logger.setLevel(logging.INFO)
    
    # Add handler to app logger
    app.logger.addHandler(file_handler)
    
    # Log application startup
    app.logger.info('Blog application startup')
