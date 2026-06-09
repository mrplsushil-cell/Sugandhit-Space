from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import db, Service, Booking, User
from datetime import datetime, timedelta

booking_bp = Blueprint('booking', __name__, url_prefix='/booking')

@booking_bp.route('/')
def index():
    services = Service.query.filter_by(is_active=True).all()
    categories = db.session.query(Service.category).filter_by(is_active=True).distinct().all()
    
    return render_template('booking/index.html',
                         services=services,
                         categories=[c[0] for c in categories if c[0]])

@booking_bp.route('/service/<int:service_id>')
def service_detail(service_id):
    service = Service.query.get_or_404(service_id)
    
    return render_template('booking/service_detail.html', service=service)

@booking_bp.route('/book/<int:service_id>', methods=['GET', 'POST'])
@login_required
def book_service(service_id):
    service = Service.query.get_or_404(service_id)
    
    if request.method == 'POST':
        booking_date_str = request.form.get('booking_date')
        time_str = request.form.get('time')
        notes = request.form.get('notes', '')
        
        try:
            booking_datetime_str = f"{booking_date_str} {time_str}"
            booking_datetime = datetime.strptime(booking_datetime_str, '%Y-%m-%d %H:%M')
            
            # Validate booking date is in future
            if booking_datetime <= datetime.now():
                flash('Please select a future date and time', 'danger')
                return render_template('booking/book_service.html', service=service)
            
            # Create booking
            booking = Booking(
                user_id=current_user.id,
                service_id=service_id,
                booking_date=booking_datetime,
                notes=notes,
                status='pending'
            )
            
            db.session.add(booking)
            db.session.commit()
            
            flash('Booking confirmed! Our expert will contact you soon.', 'success')
            return redirect(url_for('dashboard.my_bookings'))
        
        except ValueError:
            flash('Invalid date or time format', 'danger')
    
    # Calculate min and max booking dates
    min_date = datetime.now() + timedelta(days=1)
    max_date = datetime.now() + timedelta(days=30)
    
    return render_template('booking/book_service.html',
                         service=service,
                         min_date=min_date.strftime('%Y-%m-%d'),
                         max_date=max_date.strftime('%Y-%m-%d'))

@booking_bp.route('/available-times', methods=['GET'])
def get_available_times():
    """Get available time slots for a date"""
    date_str = request.args.get('date')
    
    # Generate time slots (9 AM to 6 PM, 2-hour slots)
    time_slots = [
        '09:00', '10:00', '11:00', '12:00',
        '14:00', '15:00', '16:00', '17:00', '18:00'
    ]
    
    return jsonify({'times': time_slots})

@booking_bp.route('/cancel/<int:booking_id>', methods=['POST'])
@login_required
def cancel_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    
    # Check if user owns this booking
    if booking.user_id != current_user.id:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('main.home'))
    
    # Check if booking is within 24 hours
    time_diff = booking.booking_date - datetime.now()
    if time_diff.total_seconds() < 86400:  # 24 hours
        flash('Cannot cancel booking within 24 hours of scheduled time', 'danger')
    else:
        booking.status = 'cancelled'
        db.session.commit()
        flash('Booking cancelled successfully!', 'success')
    
    return redirect(url_for('dashboard.my_bookings'))

@booking_bp.route('/reschedule/<int:booking_id>', methods=['GET', 'POST'])
@login_required
def reschedule_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    
    # Check if user owns this booking
    if booking.user_id != current_user.id:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('main.home'))
    
    if request.method == 'POST':
        new_date_str = request.form.get('new_date')
        new_time_str = request.form.get('new_time')
        
        try:
            new_datetime_str = f"{new_date_str} {new_time_str}"
            new_datetime = datetime.strptime(new_datetime_str, '%Y-%m-%d %H:%M')
            
            if new_datetime <= datetime.now():
                flash('Please select a future date and time', 'danger')
                return redirect(url_for('booking.reschedule_booking', booking_id=booking_id))
            
            booking.booking_date = new_datetime
            db.session.commit()
            
            flash('Booking rescheduled successfully!', 'success')
            return redirect(url_for('dashboard.my_bookings'))
        
        except ValueError:
            flash('Invalid date or time format', 'danger')
    
    min_date = datetime.now() + timedelta(days=1)
    max_date = datetime.now() + timedelta(days=30)
    
    return render_template('booking/reschedule_booking.html',
                         booking=booking,
                         min_date=min_date.strftime('%Y-%m-%d'),
                         max_date=max_date.strftime('%Y-%m-%d'))
