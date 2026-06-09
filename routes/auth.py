from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User, UserRole
from werkzeug.security import generate_password_hash
import re

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_valid_phone(phone):
    pattern = r'^[0-9]{10}$'
    return re.match(pattern, phone) is not None

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        phone = request.form.get('phone', '').strip()
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        role = request.form.get('role', 'customer')
        
        # Validation
        errors = []
        
        if not name or len(name) < 3:
            errors.append('Name must be at least 3 characters long')
        
        if not email or not is_valid_email(email):
            errors.append('Please enter a valid email address')
        
        if User.query.filter_by(email=email).first():
            errors.append('Email already registered')
        
        if not phone or not is_valid_phone(phone):
            errors.append('Please enter a valid 10-digit phone number')
        
        if not password or len(password) < 6:
            errors.append('Password must be at least 6 characters long')
        
        if password != confirm_password:
            errors.append('Passwords do not match')
        
        if role not in ['customer', 'expert']:
            role = 'customer'
        
        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('auth/register.html')
        
        # Create new user
        user = User(
            name=name,
            email=email,
            phone=phone,
            role=role
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password')
        remember_me = request.form.get('remember_me') is not None
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            if not user.is_active:
                flash('Your account has been deactivated', 'warning')
                return render_template('auth/login.html')
            
            login_user(user, remember=remember_me)
            
            # Redirect based on role
            if user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(request.args.get('next') or url_for('main.home'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully', 'info')
    return redirect(url_for('main.home'))

@auth_bp.route('/profile')
@login_required
def profile():
    return render_template('auth/profile.html', user=current_user)

@auth_bp.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    current_user.name = request.form.get('name', current_user.name)
    current_user.phone = request.form.get('phone', current_user.phone)
    current_user.address = request.form.get('address', current_user.address)
    current_user.city = request.form.get('city', current_user.city)
    current_user.pincode = request.form.get('pincode', current_user.pincode)
    
    db.session.commit()
    flash('Profile updated successfully!', 'success')
    return redirect(url_for('auth.profile'))

@auth_bp.route('/change-password', methods=['POST'])
@login_required
def change_password():
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    
    if not current_user.check_password(old_password):
        flash('Current password is incorrect', 'danger')
    elif new_password != confirm_password:
        flash('New passwords do not match', 'danger')
    elif len(new_password) < 6:
        flash('New password must be at least 6 characters long', 'danger')
    else:
        current_user.set_password(new_password)
        db.session.commit()
        flash('Password changed successfully!', 'success')
    
    return redirect(url_for('auth.profile'))
