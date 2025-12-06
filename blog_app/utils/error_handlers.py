"""
Custom error handlers for the application
"""
from flask import render_template


def register_error_handlers(app):
    """Register custom error handlers"""
    
    @app.errorhandler(403)
    def forbidden(error):
        """Handle 403 Forbidden errors"""
        return render_template('errors/403.html'), 403
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 Not Found errors"""
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 Internal Server errors"""
        from .. import db
        db.session.rollback()  # Rollback any failed transactions
        return render_template('errors/500.html'), 500
