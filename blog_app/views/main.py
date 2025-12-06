"""
Main views for blog functionality
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, current_app
from flask_login import login_required, current_user
from sqlalchemy import desc

from .. import db
from ..models import Post, Message
from ..forms import PostForm, ContactForm

bp = Blueprint('main', __name__)


@bp.route('/')
def home():
    """Home page with latest posts"""
    posts = Post.query.order_by(desc(Post.created_at)).limit(5).all()
    return render_template('index.html', posts=posts)


@bp.route('/about')
def about():
    """About page"""
    return render_template('about.html')


@bp.route('/blog')
def blog():
    """Blog listing with pagination"""
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config.get('POSTS_PER_PAGE', 10)
    
    pagination = Post.query.order_by(desc(Post.created_at)).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('blog.html', posts=pagination.items, pagination=pagination)


@bp.route('/post/<int:post_id>')
def post_view(post_id):
    """View individual post"""
    post = db.session.get(Post, post_id)
    if not post:
        abort(404)
    return render_template('post.html', post=post)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Create new post"""
    form = PostForm()
    
    if form.validate_on_submit():
        post = Post(
            title=form.title.data.strip(),
            content=form.content.data.strip(),
            author=current_user
        )
        db.session.add(post)
        db.session.commit()
        
        flash('Post created successfully!', 'success')
        return redirect(url_for('main.post_view', post_id=post.id))
    
    return render_template('create.html', form=form)


@bp.route('/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit(post_id):
    """Edit existing post"""
    post = db.session.get(Post, post_id)
    if not post:
        abort(404)
    
    # Check authorization
    if post.author != current_user:
        abort(403)
    
    form = PostForm(obj=post)
    
    if form.validate_on_submit():
        post.title = form.title.data.strip()
        post.content = form.content.data.strip()
        db.session.commit()
        
        flash('Post updated successfully!', 'success')
        return redirect(url_for('main.post_view', post_id=post.id))
    
    return render_template('edit.html', form=form, post=post)


@bp.route('/delete/<int:post_id>', methods=['POST'])
@login_required
def delete(post_id):
    """Delete a post"""
    post = db.session.get(Post, post_id)
    if not post:
        abort(404)
    
    # Check authorization (author or admin)
    if post.author != current_user and not current_user.is_admin:
        abort(403)
    
    db.session.delete(post)
    db.session.commit()
    
    flash('Post deleted successfully.', 'info')
    return redirect(url_for('main.blog'))


@bp.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact form"""
    form = ContactForm()
    
    if form.validate_on_submit():
        message = Message(
            name=form.name.data.strip(),
            email=form.email.data.strip().lower(),
            message=form.message.data.strip()
        )
        db.session.add(message)
        db.session.commit()
        
        flash('Thank you for your message! We will get back to you soon.', 'success')
        return redirect(url_for('main.contact'))
    
    return render_template('contact.html', form=form)
