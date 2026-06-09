from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import login_required, current_user
from models import db, Order, Payment
try:
    import razorpay
except ImportError:
    razorpay = None
import hmac
import hashlib

payment_bp = Blueprint('payment', __name__, url_prefix='/payment')

def get_razorpay_client():
    """Initialize Razorpay client"""
    if razorpay is None:
        raise ImportError("Razorpay package not available. Install with: pip install razorpay")
    client = razorpay.Client(
        auth=(current_app.config['RAZORPAY_KEY_ID'], 
              current_app.config['RAZORPAY_KEY_SECRET'])
    )
    return client

@payment_bp.route('/initiate/<int:order_id>')
@login_required
def initiate_payment(order_id):
    order = Order.query.get_or_404(order_id)
    
    # Check if user owns this order
    if order.user_id != current_user.id:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('main.home'))
    
    # Create Razorpay order
    try:
        client = get_razorpay_client()
        
        razorpay_order = client.order.create(dict(
            amount=int(order.total_amount * 100),  # Amount in paise
            currency='INR',
            receipt=order.order_number,
            payment_capture=1
        ))
        
        # Store Razorpay order ID
        payment = Payment(
            order_id=order_id,
            razorpay_order_id=razorpay_order['id'],
            amount=order.total_amount,
            currency='INR',
            status='pending'
        )
        db.session.add(payment)
        db.session.commit()
        
        return render_template('payment/razorpay.html',
                             order=order,
                             razorpay_order_id=razorpay_order['id'],
                             razorpay_key_id=current_app.config['RAZORPAY_KEY_ID'],
                             amount=int(order.total_amount * 100),
                             user_email=current_user.email,
                             user_phone=current_user.phone)
    
    except Exception as e:
        flash(f'Error initiating payment: {str(e)}', 'danger')
        return redirect(url_for('order.order_detail', order_id=order_id))

@payment_bp.route('/verify', methods=['POST'])
@login_required
def verify_payment():
    """Verify Razorpay payment"""
    data = request.get_json()
    
    razorpay_payment_id = data.get('razorpay_payment_id')
    razorpay_order_id = data.get('razorpay_order_id')
    razorpay_signature = data.get('razorpay_signature')
    order_id = data.get('order_id')
    
    # Find the order and payment
    order = Order.query.get(order_id)
    payment = Payment.query.filter_by(razorpay_order_id=razorpay_order_id).first()
    
    if not order or not payment:
        return jsonify({'success': False, 'message': 'Order or payment not found'}), 404
    
    # Verify signature
    message = razorpay_order_id + '|' + razorpay_payment_id
    expected_signature = hmac.new(
        current_app.config['RAZORPAY_KEY_SECRET'].encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()
    
    if razorpay_signature == expected_signature:
        # Payment verified
        payment.razorpay_payment_id = razorpay_payment_id
        payment.status = 'completed'
        order.payment_status = 'completed'
        order.status = 'confirmed'
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Payment successful!',
            'redirect_url': url_for('order.order_detail', order_id=order_id)
        })
    else:
        # Signature verification failed
        payment.status = 'failed'
        db.session.commit()
        
        return jsonify({
            'success': False,
            'message': 'Payment verification failed'
        }), 400

@payment_bp.route('/callback', methods=['POST'])
def payment_callback():
    """Razorpay payment callback"""
    # This is handled by the frontend verify endpoint
    return jsonify({'success': True})

@payment_bp.route('/success/<int:order_id>')
@login_required
def payment_success(order_id):
    order = Order.query.get_or_404(order_id)
    
    if order.user_id != current_user.id:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('main.home'))
    
    return render_template('payment/success.html', order=order)

@payment_bp.route('/failed/<int:order_id>')
@login_required
def payment_failed(order_id):
    order = Order.query.get_or_404(order_id)
    
    if order.user_id != current_user.id:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('main.home'))
    
    return render_template('payment/failed.html', order=order)

@payment_bp.route('/methods', methods=['GET'])
def get_payment_methods():
    """Get available payment methods"""
    methods = [
        {'id': 'upi', 'name': 'UPI', 'icon': '📱'},
        {'id': 'card', 'name': 'Debit/Credit Card', 'icon': '💳'},
        {'id': 'netbanking', 'name': 'Net Banking', 'icon': '🏦'},
        {'id': 'cod', 'name': 'Cash on Delivery', 'icon': '💵'}
    ]
    
    return jsonify({'methods': methods})
