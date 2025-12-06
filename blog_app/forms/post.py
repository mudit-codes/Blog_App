"""
Post forms with validation
"""
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    """Blog post creation and editing form"""
    title = StringField(
        'Title',
        validators=[
            DataRequired(message='Title is required'),
            Length(min=1, max=200, message='Title must be 1-200 characters')
        ]
    )
    content = TextAreaField(
        'Content',
        validators=[
            DataRequired(message='Content is required'),
            Length(min=1, message='Content cannot be empty')
        ]
    )
    submit = SubmitField('Save Post')
