"""
Helper functions for common operations
"""
from flask import current_app
from .. import cache
from ..models import Post


@cache.cached(timeout=60, key_prefix='recent_posts')
def get_recent_posts(limit=5):
    """Get recent posts with caching"""
    return Post.query.order_by(Post.created_at.desc()).limit(limit).all()


def log_action(action, details=None):
    """Log user actions for audit trail"""
    if current_app.config.get('TESTING'):
        return
    
    message = f"Action: {action}"
    if details:
        message += f" - Details: {details}"
    
    current_app.logger.info(message)
