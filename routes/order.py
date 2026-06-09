from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import login_required, current_user
from models import db, Order, OrderItem, Plant, DeliveryTracking, Payment
from datetime import datetime, timedelta
import uuid

order_bp = Blueprint('order', __name__, url_prefix='/order')

@order_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart = session.get('cart', {})
    
    if not cart:
        flash('Your cart is empty', 'warning')
        return redirect(url_for('catalog.index'))
    
    if request.method == 'POST':
        delivery_address = request.form.get('delivery_address')
        city = request.form.get('city')
        pincode = request.form.get('pincode')
        phone = request.form.get('phone')
        
        if not all([delivery_address, city, pincode, phone]):
            flash('Please fill all required fields', 'danger')
            return render_template('order/checkout.html', cart=cart)
        
        # Create order
        order = Order(
            order_number=f"ORD-{uuid.uuid4().hex[:8].upper()}",
            user_id=current_user.id,
            delivery_address=f"{delivery_address}, {city}, {pincode}",
            total_amount=0,
            tax=0,
            delivery_charge=0
        )
        
        # Add items to order
        total_amount = 0
        for plant_id, item in cart.items():
            plant = Plant.query.get(int(plant_id))
            if plant:
                order_item = OrderItem(
                    plant_id=int(plant_id),
                    quantity=item['quantity'],
                    price=item['price']
                )
                order.items.append(order_item)
                total_amount += item['price'] * item['quantity']
        
        # Calculate tax and delivery
        tax = round(total_amount * 0.05, 2)  # 5% tax
        delivery_charge = 50 if total_amount < 1000 else 0
        
        order.total_amount = total_amount + tax + delivery_charge
        order.tax = tax
        order.delivery_charge = delivery_charge
        
        db.session.add(order)
        db.session.commit()
        
        # Create delivery tracking
        delivery_tracking = DeliveryTracking(
            order_id=order.id,
            current_location='Order Confirmed',
            status='pending',
            estimated_delivery=datetime.now() + timedelta(days=3)
        )
        db.session.add(delivery_tracking)
        db.session.commit()
        
        # Clear cart
        session['cart'] = {}
        session.modified = True
        
        return redirect(url_for('payment.initiate_payment', order_id=order.id))
    
    # Calculate totals
    total_amount = 0
    cart_items = []
    
    for plant_id, item in cart.items():
        item_total = item['price'] * item['quantity']
        total_amount += item_total
        cart_items.append({
            'plant_id': plant_id,
            'name': item['name'],
            'price': item['price'],
            'quantity': item['quantity'],
            'total': item_total
        })
    
    tax = round(total_amount * 0.05, 2)
    delivery_charge = 50 if total_amount < 1000 else 0
    final_total = total_amount + tax + delivery_charge
    
    return render_template('order/checkout.html',
                         cart_items=cart_items,
                         subtotal=total_amount,
                         tax=tax,
                         delivery_charge=delivery_charge,
                         total=final_total)

@order_bp.route('/<int:order_id>')
@login_required
def order_detail(order_id):
    order = Order.query.get_or_404(order_id)
    
    # Check if user owns this order
    if order.user_id != current_user.id:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('main.home'))
    
    tracking = DeliveryTracking.query.filter_by(order_id=order_id).first()
    
    return render_template('order/order_detail.html',
                         order=order,
                         tracking=tracking)

@order_bp.route('/<int:order_id>/cancel', methods=['POST'])
@login_required
def cancel_order(order_id):
    order = Order.query.get_or_404(order_id)
    
    # Check if user owns this order
    if order.user_id != current_user.id:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('main.home'))
    
    # Can only cancel if not already shipped
    if order.status in ['pending', 'confirmed', 'processing']:
        order.status = 'cancelled'
        db.session.commit()
        flash('Order cancelled successfully!', 'success')
    else:
        flash('Cannot cancel order in current status', 'danger')
    
    return redirect(url_for('order.order_detail', order_id=order_id))

@order_bp.route('/<int:order_id>/track')
@login_required
def track_order(order_id):
    order = Order.query.get_or_404(order_id)
    
    # Check if user owns this order
    if order.user_id != current_user.id:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    tracking = DeliveryTracking.query.filter_by(order_id=order_id).first()
    
    return jsonify({
        'order_number': order.order_number,
        'status': order.status,
        'current_location': tracking.current_location if tracking else 'N/A',
        'delivery_status': tracking.status if tracking else 'N/A',
        'delivery_person': tracking.delivery_person if tracking else 'N/A',
        'estimated_delivery': tracking.estimated_delivery.strftime('%Y-%m-%d %H:%M') if tracking and tracking.estimated_delivery else 'N/A'
    })
