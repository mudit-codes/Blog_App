# Flask Blog App - Optimized Edition

A **fully optimized** and **production-ready** blog web application built with **Flask**, **SQLite**, and **Bootstrap 5**.  
This project showcases best practices in Flask development with a modular architecture, proper security, and performance optimizations.

---

## 🚀 What's New - Optimized Version

### Architecture Improvements
- **Modular Structure**: Organized code into blueprints, models, forms, and utilities
- **Application Factory Pattern**: Better configuration management and testing support
- **Separation of Concerns**: Clear separation between business logic, data models, and presentation
- **Scalable Design**: Easy to extend and maintain

### Security Enhancements
- **CSRF Protection**: Flask-WTF forms with CSRF tokens
- **Input Validation**: Comprehensive form validation using WTForms
- **Secure Session Management**: Properly configured session cookies
- **SQL Injection Prevention**: Using SQLAlchemy ORM with parameterized queries
- **Password Security**: Werkzeug password hashing with best practices

### Performance Optimizations
- **Database Indexes**: Added indexes on frequently queried fields
- **Efficient Queries**: Optimized database queries with proper joins and lazy loading
- **Pagination**: Implemented pagination for blog posts, users, and messages
- **Connection Pooling**: Configured SQLAlchemy connection pool for better performance

### Code Quality
- **Type Hints**: Added throughout the codebase for better IDE support
- **Error Handling**: Custom error pages (403, 404, 500)
- **Documentation**: Comprehensive docstrings and comments
- **DRY Principle**: Eliminated code duplication

---

## Features

### User Features
- **Authentication**: Secure register & login with validation
- **Post Management**: Create, edit, and delete own posts with rich forms
- **Browse Content**: View all posts with pagination
- **Contact**: Send messages through validated contact form

### Admin Features
- **Admin Dashboard**: Dedicated admin panel (default: `admin / admin123`)
- **User Management**: View, promote/demote, and delete users
- **Message Tracking**: View and manage contact form submissions with read/unread status
- **Access Control**: Protected admin routes with decorator
- **Pagination**: All admin lists are paginated for performance

### General Features
- **Responsive Design**: Bootstrap 5 with custom styling
- **Flash Messages**: User-friendly notifications for all actions
- **Secure Storage**: Hashed passwords with Werkzeug
- **Timestamps**: Automatic creation and update timestamps
- **Error Pages**: Custom error handlers for better UX
- **Form Validation**: Client and server-side validation
- **Database Migrations**: Flask-Migrate for schema management

---