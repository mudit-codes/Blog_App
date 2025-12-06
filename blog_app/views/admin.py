"""
Admin views for managing users and messages
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort, current_app
from flask_login import login_required
from sqlalchemy import desc

from .. import db
from ..models import User, Message
from ..utils.decorators import admin_required

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/messages')
@login_required
@admin_required
def messages():
    """View all contact messages with pagination"""
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config.get('MESSAGES_PER_PAGE', 20)
    
    pagination = Message.query.order_by(desc(Message.created_at)).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('admin_messages.html', 
                         messages=pagination.items, 
                         pagination=pagination)


@bp.route('/users')
@login_required
@admin_required
def users():
    """View all users with pagination"""
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config.get('USERS_PER_PAGE', 20)
    
    pagination = User.query.order_by(desc(User.created_at)).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('admin_users.html', 
                         users=pagination.items, 
                         pagination=pagination)


@bp.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    """Delete a user (admin only)"""
    user = db.session.get(User, user_id)
    if not user:
        abort(404)
    
    # Prevent deleting admin accounts
    if user.is_admin:
        flash('Cannot delete an admin account.', 'danger')
        return redirect(url_for('admin.users'))
    
    db.session.delete(user)
    db.session.commit()
    
    flash(f'User {user.username} has been deleted.', 'info')
    return redirect(url_for('admin.users'))


@bp.route('/toggle_admin/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def toggle_admin(user_id):
    """Toggle user admin status"""
    from flask_login import current_user
    
    user = db.session.get(User, user_id)
    if not user:
        abort(404)
    
    # Prevent changing own admin status
    if user.id == current_user.id:
        flash('You cannot change your own admin status.', 'danger')
        return redirect(url_for('admin.users'))
    
    user.is_admin = not user.is_admin
    db.session.commit()
    
    status = 'promoted to admin' if user.is_admin else 'removed from admin'
    flash(f'User {user.username} has been {status}.', 'success')
    return redirect(url_for('admin.users'))


@bp.route('/mark_message_read/<int:message_id>', methods=['POST'])
@login_required
@admin_required
def mark_message_read(message_id):
    """Mark a message as read"""
    message = db.session.get(Message, message_id)
    if not message:
        abort(404)
    
    message.is_read = True
    db.session.commit()
    
    flash('Message marked as read.', 'success')
    return redirect(url_for('admin.messages'))


@bp.route('/delete_message/<int:message_id>', methods=['POST'])
@login_required
@admin_required
def delete_message(message_id):
    """Delete a message"""
    message = db.session.get(Message, message_id)
    if not message:
        abort(404)
    
    db.session.delete(message)
    db.session.commit()
    
    flash('Message deleted successfully.', 'info')
    return redirect(url_for('admin.messages'))
