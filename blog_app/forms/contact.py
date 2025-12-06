"""
Contact form with validation
"""
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class ContactForm(FlaskForm):
    """Contact message form"""
    name = StringField(
        'Name',
        validators=[
            DataRequired(message='Name is required'),
            Length(min=1, max=120, message='Name must be 1-120 characters')
        ]
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired(message='Email is required'),
            Email(message='Invalid email address'),
            Length(max=120, message='Email too long')
        ]
    )
    message = TextAreaField(
        'Message',
        validators=[
            DataRequired(message='Message is required'),
            Length(min=10, message='Message must be at least 10 characters')
        ]
    )
    submit = SubmitField('Send Message')
