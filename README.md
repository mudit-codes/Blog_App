# Flask Blog App

A full-featured blog web application built with **Flask**, **SQLite**, and **Bootstrap 5**.  
This project is perfect for learning Flask, showcasing a portfolio, or even deploying a small production blog.

---

## Features

### User Features
- Register & login
- Create, edit, and delete own posts
- View all posts
- Contact form to send messages

### Admin Features
- Admin login (default: `admin / admin123`)
- View and manage all users
- Promote/demote users to/from admin
- View messages sent through contact form
- Delete users (non-admins)
- Access control (only admin can see admin pages)

### General
- Responsive design with Bootstrap 5
- Flash messages for actions (success, error, info)
- Secure password storage with hashing (Werkzeug)
- Blog posts with timestamps and authors
- SQLite database inside `instance/blog.db`

---