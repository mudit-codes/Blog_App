"""
Flask Blog Application
Optimized and modular structure for better maintainability and performance
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import os

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()


def create_app(config_name=None):
    """Application factory pattern for better testing and configuration"""
    app = Flask(__name__, 
                static_folder="../static",
                template_folder="../templates")
    
    # Load configuration
    from .config import get_config
    config = get_config(config_name)
    app.config.from_object(config)
    
    # Ensure instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    # Configure login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # Register blueprints
    from .views import main, auth, admin
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(admin.bp)
    
    # Register error handlers
    from .utils import error_handlers
    error_handlers.register_error_handlers(app)
    
    # User loader
    from .models.user import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))
    
    # Initialize database and default admin
    with app.app_context():
        db.create_all()
        _create_default_admin()
    
    return app


def _create_default_admin():
    """Create default admin user if not exists"""
    from .models.user import User
    
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@example.com',
            is_admin=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print('✅ Default admin created: admin / admin123')
