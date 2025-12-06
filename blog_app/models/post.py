"""
Post model for blog content
"""
from datetime import datetime
from .. import db


class Post(db.Model):
    """Blog post model"""
    
    __tablename__ = 'post'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Post content
    title = db.Column(db.String(200), nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    
    # Foreign key
    author_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), 
                         nullable=False, index=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, 
                          nullable=False)
    
    # Relationships
    author = db.relationship('User', back_populates='posts')
    
    @property
    def excerpt(self, length: int = 200) -> str:
        """Return truncated content for previews"""
        if len(self.content) <= length:
            return self.content
        return self.content[:length].rsplit(' ', 1)[0] + '...'
    
    def __repr__(self) -> str:
        return f'<Post {self.id}: {self.title[:30]}>'
