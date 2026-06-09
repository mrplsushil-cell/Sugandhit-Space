from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from functools import wraps
from models import db, User, Order, Plant, Service, Booking, SupportTicket, DeliveryTracking, UserRole
from datetime import datetime, timedelta

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if current_user.role != 'admin':
            flash('Admin access required', 'danger')
            return redirect(url_for('main.home'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    # Calculate statistics
    total_orders = Order.query.count()
    total_revenue = db.session.query(db.func.sum(Order.total_amount)).filter(
        Order.payment_status == 'completed'
    ).scalar() or 0
    
    pending_orders = Order.query.filter_by(status='pending').count()
    total_customers = User.query.filter_by(role='customer').count()
    
    # Recent orders
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()
    
    # Revenue chart data (last 7 days)
    revenue_data = []
    for i in range(6, -1, -1):
        date = datetime.now() - timedelta(days=i)
        date_str = date.strftime('%Y-%m-%d')
        revenue = db.session.query(db.func.sum(Order.total_amount)).filter(
            Order.payment_status == 'completed',
            db.func.date(Order.created_at) == date_str
        ).scalar() or 0
        revenue_data.append({'date': date_str, 'revenue': float(revenue)})
    
    stats = {
        'total_orders': total_orders,
        'total_revenue': float(total_revenue),
        'pending_orders': pending_orders,
        'total_customers': total_customers
    }
    
    return render_template('admin/dashboard.html',
                         stats=stats,
                         recent_orders=recent_orders,
                         revenue_data=revenue_data)

@admin_bp.route('/orders')
@admin_required
def orders():
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')
    search = request.args.get('search', '')
    
    query = Order.query
    
    if status:
        query = query.filter_by(status=status)
    
    if search:
        query = query.filter(
            Order.order_number.ilike(f'%{search}%') |
            User.name.ilike(f'%{search}%')
        ).join(User)
    
    orders = query.order_by(Order.created_at.desc()).paginate(page=page, per_page=20)
    
    return render_template('admin/orders.html', orders=orders, selected_status=status)

@admin_bp.route('/order/<int:order_id>')
@admin_required
def order_detail(order_id):
    order = Order.query.get_or_404(order_id)
    tracking = DeliveryTracking.query.filter_by(order_id=order_id).first()
    
    return render_template('admin/order_detail.html', order=order, tracking=tracking)

@admin_bp.route('/order/<int:order_id>/update-status', methods=['POST'])
@admin_required
def update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status')
    
    if new_status in ['pending', 'confirmed', 'processing', 'shipped', 'delivered', 'cancelled']:
        order.status = new_status
        db.session.commit()
        flash('Order status updated!', 'success')
    
    return redirect(url_for('admin.order_detail', order_id=order_id))

@admin_bp.route('/customers')
@admin_required
def customers():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    query = User.query.filter_by(role='customer')
    
    if search:
        query = query.filter(
            User.name.ilike(f'%{search}%') |
            User.email.ilike(f'%{search}%')
        )
    
    customers = query.order_by(User.created_at.desc()).paginate(page=page, per_page=20)
    
    return render_template('admin/customers.html', customers=customers, search_query=search)

@admin_bp.route('/plants')
@admin_required
def plants():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    query = Plant.query
    
    if search:
        query = query.filter(Plant.name.ilike(f'%{search}%'))
    
    plants = query.order_by(Plant.name.asc()).paginate(page=page, per_page=20)
    
    return render_template('admin/plants.html', plants=plants, search_query=search)

@admin_bp.route('/plant/create', methods=['GET', 'POST'])
@admin_required
def create_plant():
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price', type=float)
        quantity = request.form.get('quantity', type=int)
        category = request.form.get('category')
        description = request.form.get('description')
        care_tips = request.form.get('care_tips')
        
        plant = Plant(
            name=name,
            price=price,
            quantity=quantity,
            category=category,
            description=description,
            care_tips=care_tips,
            is_active=True
        )
        
        db.session.add(plant)
        db.session.commit()
        
        flash('Plant added successfully!', 'success')
        return redirect(url_for('admin.plants'))
    
    return render_template('admin/create_plant.html')

@admin_bp.route('/plant/<int:plant_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_plant(plant_id):
    plant = Plant.query.get_or_404(plant_id)
    
    if request.method == 'POST':
        plant.name = request.form.get('name', plant.name)
        plant.price = request.form.get('price', plant.price, type=float)
        plant.quantity = request.form.get('quantity', plant.quantity, type=int)
        plant.category = request.form.get('category', plant.category)
        plant.description = request.form.get('description', plant.description)
        plant.care_tips = request.form.get('care_tips', plant.care_tips)
        
        db.session.commit()
        flash('Plant updated successfully!', 'success')
        return redirect(url_for('admin.plants'))
    
    return render_template('admin/edit_plant.html', plant=plant)

@admin_bp.route('/plant/<int:plant_id>/delete', methods=['POST'])
@admin_required
def delete_plant(plant_id):
    plant = Plant.query.get_or_404(plant_id)
    plant.is_active = False
    db.session.commit()
    
    flash('Plant deleted successfully!', 'success')
    return redirect(url_for('admin.plants'))

@admin_bp.route('/services')
@admin_required
def services():
    services_list = Service.query.all()
    return render_template('admin/services.html', services=services_list)

@admin_bp.route('/bookings')
@admin_required
def bookings():
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')
    
    query = Booking.query
    
    if status:
        query = query.filter_by(status=status)
    
    bookings = query.order_by(Booking.created_at.desc()).paginate(page=page, per_page=20)
    
    return render_template('admin/bookings.html', bookings=bookings)

@admin_bp.route('/support-tickets')
@admin_required
def support_tickets():
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')
    
    query = SupportTicket.query
    
    if status:
        query = query.filter_by(status=status)
    
    tickets = query.order_by(SupportTicket.created_at.desc()).paginate(page=page, per_page=20)
    
    return render_template('admin/support_tickets.html', tickets=tickets)

@admin_bp.route('/ticket/<int:ticket_id>/respond', methods=['POST'])
@admin_required
def respond_to_ticket(ticket_id):
    ticket = SupportTicket.query.get_or_404(ticket_id)
    response = request.form.get('response')
    
    ticket.response = response
    ticket.status = 'resolved'
    db.session.commit()
    
    flash('Response sent successfully!', 'success')
    return redirect(url_for('admin.support_tickets'))

@admin_bp.route('/analytics')
@admin_required
def analytics():
    # Revenue by category
    category_revenue = db.session.query(
        Plant.category,
        db.func.sum(OrderItem.price * OrderItem.quantity).label('revenue')
    ).join(OrderItem).join(Order).filter(
        Order.payment_status == 'completed'
    ).group_by(Plant.category).all()
    
    return render_template('admin/analytics.html', category_revenue=category_revenue)
