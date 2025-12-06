"""
Authentication forms with validation
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import (
    DataRequired, Email, Length, EqualTo, ValidationError
)
from ..models.user import User


class LoginForm(FlaskForm):
    """User login form"""
    username = StringField(
        'Username',
        validators=[
            DataRequired(message='Username is required'),
            Length(min=3, max=80, message='Username must be 3-80 characters')
        ]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(message='Password is required')]
    )
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    """User registration form"""
    username = StringField(
        'Username',
        validators=[
            DataRequired(message='Username is required'),
            Length(min=3, max=80, message='Username must be 3-80 characters')
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
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message='Password is required'),
            Length(min=6, message='Password must be at least 6 characters')
        ]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(message='Please confirm your password'),
            EqualTo('password', message='Passwords must match')
        ]
    )
    submit = SubmitField('Register')
    
    def validate_username(self, field):
        """Check if username is already taken"""
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already exists. Please choose another.')
    
    def validate_email(self, field):
        """Check if email is already registered"""
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email already registered. Please try logging in.')
