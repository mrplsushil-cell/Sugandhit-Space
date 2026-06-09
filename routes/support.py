from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from models import db, SupportTicket
import uuid
from datetime import datetime

support_bp = Blueprint('support', __name__, url_prefix='/support')

@support_bp.route('/')
def index():
    return render_template('support/index.html')

@support_bp.route('/ticket/create', methods=['GET', 'POST'])
@login_required
def create_ticket():
    if request.method == 'POST':
        subject = request.form.get('subject')
        message = request.form.get('message')
        category = request.form.get('category', 'query')
        priority = request.form.get('priority', 'medium')
        
        if not subject or not message:
            flash('Subject and message are required', 'danger')
            return render_template('support/create_ticket.html')
        
        ticket = SupportTicket(
            ticket_number=f"TKT-{uuid.uuid4().hex[:8].upper()}",
            user_id=current_user.id,
            subject=subject,
            message=message,
            category=category,
            priority=priority,
            status='open'
        )
        
        db.session.add(ticket)
        db.session.commit()
        
        flash('Support ticket created successfully!', 'success')
        return redirect(url_for('support.ticket_detail', ticket_id=ticket.id))
    
    return render_template('support/create_ticket.html')

@support_bp.route('/ticket/<int:ticket_id>')
@login_required
def ticket_detail(ticket_id):
    ticket = SupportTicket.query.get_or_404(ticket_id)
    
    # Check if user owns this ticket
    if ticket.user_id != current_user.id:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('support.index'))
    
    return render_template('support/ticket_detail.html', ticket=ticket)

@support_bp.route('/tickets')
@login_required
def my_tickets():
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')
    
    query = SupportTicket.query.filter_by(user_id=current_user.id)
    
    if status:
        query = query.filter_by(status=status)
    
    tickets = query.order_by(SupportTicket.created_at.desc()).paginate(page=page, per_page=10)
    
    return render_template('support/my_tickets.html', tickets=tickets, selected_status=status)

@support_bp.route('/ticket/<int:ticket_id>/close', methods=['POST'])
@login_required
def close_ticket(ticket_id):
    ticket = SupportTicket.query.get_or_404(ticket_id)
    
    if ticket.user_id != current_user.id:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    ticket.status = 'closed'
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Ticket closed successfully'})

@support_bp.route('/faq')
def faq():
    faqs = [
        {
            'id': 1,
            'question': 'How do I place an order?',
            'answer': 'Browse our catalog, add items to your cart, and proceed to checkout. Fill in your delivery details and choose a payment method.'
        },
        {
            'id': 2,
            'question': 'What are your delivery timelines?',
            'answer': 'Standard delivery takes 2-3 business days. Express delivery (1 day) is available for an additional fee.'
        },
        {
            'id': 3,
            'question': 'How can I track my order?',
            'answer': 'You can track your order in real-time from your dashboard. We provide live location updates for deliveries.'
        },
        {
            'id': 4,
            'question': 'What is your return policy?',
            'answer': 'Plants can be returned within 7 days if damaged. We offer replacement or full refund.'
        },
        {
            'id': 5,
            'question': 'Do you provide plant care tips?',
            'answer': 'Yes! Each plant comes with care instructions. Book our expert consultation for personalized advice.'
        },
        {
            'id': 6,
            'question': 'Can I cancel or modify my booking?',
            'answer': 'You can cancel/modify bookings 24 hours before the scheduled time with no penalty.'
        },
        {
            'id': 7,
            'question': 'What payment methods do you accept?',
            'answer': 'We accept UPI, Debit/Credit Cards, Net Banking through Razorpay, and Cash on Delivery.'
        },
        {
            'id': 8,
            'question': 'Are your plants organic?',
            'answer': 'Most of our plants are grown using organic methods. Check the product details for specific information.'
        }
    ]
    
    return render_template('support/faq.html', faqs=faqs)

@support_bp.route('/chat')
@login_required
def chat():
    return render_template('support/chat.html')

@support_bp.route('/chat/send', methods=['POST'])
@login_required
def send_chat_message():
    """Send chat message (simplified - for demo)"""
    data = request.get_json()
    message = data.get('message')
    
    if not message:
        return jsonify({'success': False, 'message': 'Message cannot be empty'}), 400
    
    # In a real app, this would save to database and integrate with a chat service
    # For now, we'll return a mock response
    
    return jsonify({
        'success': True,
        'timestamp': datetime.now().isoformat(),
        'response': f'Thank you for your message: "{message}". Our team will respond shortly.'
    })
