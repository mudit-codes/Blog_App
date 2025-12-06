"""
User model with authentication capabilities
"""
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .. import db


class User(UserMixin, db.Model):
    """User model for authentication and authorization"""
    
    __tablename__ = 'user'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # User credentials
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(200), nullable=False)
    
    # User role
    is_admin = db.Column(db.Boolean, default=False, nullable=False, index=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Relationships
    posts = db.relationship('Post', back_populates='author', lazy='dynamic', 
                           cascade='all, delete-orphan')
    
    def set_password(self, password: str) -> None:
        """Hash and set user password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password: str) -> bool:
        """Verify password against stored hash"""
        return check_password_hash(self.password_hash, password)
    
    @property
    def post_count(self) -> int:
        """Get count of user's posts (cached to avoid extra queries)"""
        return self.posts.count()
    
    def __repr__(self) -> str:
        return f'<User {self.username}>'
