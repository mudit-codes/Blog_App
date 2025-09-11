import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

# ----- App setup -----
app = Flask(__name__, static_folder="static")
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")

# Ensure instance folder exists
os.makedirs(app.instance_path, exist_ok=True)

# SQLite DB inside instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(app.instance_path, "blog.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# ----- Models -----
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', backref=db.backref('posts', lazy=True))

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ----- Login loader -----
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ----- Routes -----
@app.route('/')
def home():
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template('index.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html')  # optional, template can be simple or reuse index

@app.route('/blog')
def blog():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('blog.html', posts=posts)

@app.route('/post/<int:post_id>')
def post_view(post_id):
    post = Post.query.get_or_404(post_id)
    # convert line breaks to <br>
    return render_template('post.html', post=post)

# Create post (only for logged-in users)
@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        if not title or not content:
            flash('Title and content required.', 'danger')
            return redirect(url_for('create'))
        p = Post(title=title, content=content, author=current_user)
        db.session.add(p)
        db.session.commit()
        flash('Post created!', 'success')
        return redirect(url_for('post_view', post_id=p.id))
    return render_template('create.html')

@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    if request.method == 'POST':
        post.title = request.form.get('title', '').strip()
        post.content = request.form.get('content', '').strip()
        db.session.commit()
        flash('Post updated!', 'success')
        return redirect(url_for('post_view', post_id=post.id))
    return render_template('edit.html', post=post)

@app.route('/delete/<int:post_id>', methods=['POST'])
@login_required
def delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user and not current_user.is_admin:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted.', 'info')
    return redirect(url_for('blog'))

# Contact
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        message_text = request.form.get('message', '').strip()
        if not name or not email or not message_text:
            flash('Please fill all fields.', 'danger')
            return redirect(url_for('contact'))
        msg = Message(name=name, email=email, message=message_text)
        db.session.add(msg)
        db.session.commit()
        flash('Thanks for your message!', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')

# --- Auth ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        # checks
        if not username or not email or not password:
            flash('All fields are required.', 'danger')
            return redirect(url_for('register'))
        if len(password) < 6:
            flash('Password must be at least 6 chars.', 'danger')
            return redirect(url_for('register'))
        if User.query.filter_by(username=username).first():
            flash('Username already exists. Choose another.', 'danger')
            return redirect(url_for('register'))
        if User.query.filter_by(email=email).first():
            flash('Email already registered. Try login.', 'danger')
            return redirect(url_for('register'))

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('home'))
        flash('Invalid credentials.', 'danger')
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out.', 'info')
    return redirect(url_for('home'))

# --- Admin pages ---
@app.route('/admin/messages')
@login_required
def admin_messages():
    if not current_user.is_admin:
        abort(403)
    messages = Message.query.order_by(Message.created_at.desc()).all()
    return render_template('admin_messages.html', messages=messages)

@app.route('/admin/users')
@login_required
def admin_users():
    if not current_user.is_admin:
        abort(403)
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin_users.html', users=users)

@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@login_required
def admin_delete_user(user_id):
    if not current_user.is_admin:
        abort(403)
    user = User.query.get_or_404(user_id)
    # prevent deleting yourself or other admins
    if user.is_admin:
        flash('Cannot delete an admin account.', 'danger')
        return redirect(url_for('admin_users'))
    db.session.delete(user)
    db.session.commit()
    flash('User deleted.', 'info')
    return redirect(url_for('admin_users'))

@app.route('/admin/toggle_admin/<int:user_id>', methods=['POST'])
@login_required
def admin_toggle_admin(user_id):
    if not current_user.is_admin:
        abort(403)
    user = User.query.get_or_404(user_id)
    # do not allow demoting yourself
    if user.id == current_user.id:
        flash('You cannot change your own admin status.', 'danger')
        return redirect(url_for('admin_users'))
    user.is_admin = not user.is_admin
    db.session.commit()
    flash('User role updated.', 'success')
    return redirect(url_for('admin_users'))

# ----- Auto-create default admin on first run -----
with app.app_context():
    db.create_all()  # create tables if missing
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', email='admin@example.com', is_admin=True)
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print('✅ Default admin created: admin / admin123')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
