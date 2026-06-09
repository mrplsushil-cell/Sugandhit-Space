from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Booking, Order, ReviewRating

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/')
@login_required
def index():
    # Get user statistics
    total_orders = Order.query.filter_by(user_id=current_user.id).count()
    total_bookings = Booking.query.filter_by(user_id=current_user.id).count()
    
    # Get recent orders
    recent_orders = Order.query.filter_by(user_id=current_user.id).order_by(
        Order.created_at.desc()
    ).limit(5).all()
    
    # Get upcoming bookings
    from datetime import datetime
    upcoming_bookings = Booking.query.filter(
        Booking.user_id == current_user.id,
        Booking.booking_date >= datetime.now(),
        Booking.status != 'cancelled'
    ).order_by(Booking.booking_date.asc()).limit(5).all()
    
    return render_template('dashboard/index.html',
                         total_orders=total_orders,
                         total_bookings=total_bookings,
                         recent_orders=recent_orders,
                         upcoming_bookings=upcoming_bookings)

@dashboard_bp.route('/orders')
@login_required
def my_orders():
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')
    
    query = Order.query.filter_by(user_id=current_user.id)
    
    if status:
        query = query.filter_by(status=status)
    
    orders = query.order_by(Order.created_at.desc()).paginate(page=page, per_page=10)
    
    return render_template('dashboard/my_orders.html', orders=orders, selected_status=status)

@dashboard_bp.route('/bookings')
@login_required
def my_bookings():
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')
    
    query = Booking.query.filter_by(user_id=current_user.id)
    
    if status:
        query = query.filter_by(status=status)
    
    bookings = query.order_by(Booking.booking_date.desc()).paginate(page=page, per_page=10)
    
    return render_template('dashboard/my_bookings.html', bookings=bookings, selected_status=status)

@dashboard_bp.route('/wishlist')
@login_required
def wishlist():
    # TODO: Implement wishlist functionality
    return render_template('dashboard/wishlist.html')

@dashboard_bp.route('/reviews')
@login_required
def my_reviews():
    page = request.args.get('page', 1, type=int)
    reviews = ReviewRating.query.filter_by(user_id=current_user.id).paginate(page=page, per_page=10)
    
    return render_template('dashboard/my_reviews.html', reviews=reviews)

@dashboard_bp.route('/profile')
@login_required
def profile():
    return render_template('dashboard/profile.html', user=current_user)

@dashboard_bp.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    current_user.name = request.form.get('name', current_user.name)
    current_user.phone = request.form.get('phone', current_user.phone)
    current_user.address = request.form.get('address', current_user.address)
    current_user.city = request.form.get('city', current_user.city)
    current_user.pincode = request.form.get('pincode', current_user.pincode)
    
    db.session.commit()
    flash('Profile updated successfully!', 'success')
    
    return redirect(url_for('dashboard.profile'))

@dashboard_bp.route('/password')
@login_required
def change_password():
    return render_template('dashboard/change_password.html')

@dashboard_bp.route('/password/update', methods=['POST'])
@login_required
def update_password():
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    
    if not current_user.check_password(old_password):
        flash('Current password is incorrect', 'danger')
    elif new_password != confirm_password:
        flash('New passwords do not match', 'danger')
    elif len(new_password) < 6:
        flash('New password must be at least 6 characters', 'danger')
    else:
        current_user.set_password(new_password)
        db.session.commit()
        flash('Password changed successfully!', 'success')
        return redirect(url_for('dashboard.profile'))
    
    return redirect(url_for('dashboard.change_password'))

@dashboard_bp.route('/addresses')
@login_required
def addresses():
    # TODO: Implement multiple addresses functionality
    return render_template('dashboard/addresses.html', user=current_user)

@dashboard_bp.route('/notifications')
@login_required
def notifications():
    # TODO: Implement notifications functionality
    return render_template('dashboard/notifications.html')

@dashboard_bp.route('/help')
@login_required
def help_center():
    faqs = [
        {
            'question': 'How do I track my order?',
            'answer': 'Go to "My Orders" in your dashboard and click on the order to see real-time tracking.'
        },
        {
            'question': 'Can I change my order after placing it?',
            'answer': 'You can modify orders within 1 hour of placement. Contact support for assistance.'
        },
        {
            'question': 'How do I reschedule a booking?',
            'answer': 'Go to "My Bookings" and click on the booking to reschedule. You can change the date/time up to 24 hours before.'
        }
    ]
    
    return render_template('dashboard/help_center.html', faqs=faqs)
