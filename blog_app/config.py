"""
Configuration management for different environments
"""
import os
from pathlib import Path


class Config:
    """Base configuration with common settings"""
    
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-please-change-in-production')
    
    # Database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,  # Verify connections before use
        'pool_recycle': 3600,   # Recycle connections after 1 hour
    }
    
    # Pagination
    POSTS_PER_PAGE = 10
    MESSAGES_PER_PAGE = 20
    USERS_PER_PAGE = 20
    
    # Session
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
    
    # Flask-Login
    REMEMBER_COOKIE_SECURE = False  # Set to True in production with HTTPS
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 86400  # 24 hours


class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True
    TESTING = False
    
    @property
    def SQLALCHEMY_DATABASE_URI(self):
        instance_path = Path(__file__).parent.parent / 'instance'
        instance_path.mkdir(exist_ok=True)
        return f'sqlite:///{instance_path / "blog.db"}'


class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG = False
    TESTING = False
    
    # Override these in production
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    
    @property
    def SQLALCHEMY_DATABASE_URI(self):
        # Use DATABASE_URL from environment (for services like Heroku)
        db_url = os.environ.get('DATABASE_URL')
        if db_url:
            # Fix for Heroku postgres URL
            if db_url.startswith('postgres://'):
                db_url = db_url.replace('postgres://', 'postgresql://', 1)
            return db_url
        
        # Fallback to SQLite in instance folder
        instance_path = Path(__file__).parent.parent / 'instance'
        instance_path.mkdir(exist_ok=True)
        return f'sqlite:///{instance_path / "blog.db"}'


class TestingConfig(Config):
    """Testing environment configuration"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


def get_config(config_name=None):
    """Get configuration class based on environment"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    configs = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig,
    }
    
    return configs.get(config_name, DevelopmentConfig)()
