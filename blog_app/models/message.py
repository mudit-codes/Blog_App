"""
Message model for contact form submissions
"""
from datetime import datetime
from .. import db


class Message(db.Model):
    """Contact form message model"""
    
    __tablename__ = 'message'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Sender information
    name = db.Column(db.String(120), nullable=False, index=True)
    email = db.Column(db.String(120), nullable=False, index=True)
    
    # Message content
    message = db.Column(db.Text, nullable=False)
    
    # Timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Status tracking
    is_read = db.Column(db.Boolean, default=False, nullable=False, index=True)
    
    def __repr__(self) -> str:
        return f'<Message {self.id} from {self.name}>'
