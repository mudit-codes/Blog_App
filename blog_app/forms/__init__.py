"""
Forms for the blog application with proper validation
"""
from .auth import LoginForm, RegisterForm
from .post import PostForm
from .contact import ContactForm

__all__ = ['LoginForm', 'RegisterForm', 'PostForm', 'ContactForm']
