from flask import Blueprint, render_template, request
from models import db, Service, Plant, User, Booking, Order
from flask_login import current_user

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    # Get featured services
    featured_services = Service.query.filter_by(is_active=True).limit(6).all()
    
    # Get featured plants
    featured_plants = Plant.query.filter_by(is_active=True).limit(8).all()
    
    # Get statistics for homepage
    total_customers = User.query.filter_by(role='customer').count()
    total_services = Service.query.filter_by(is_active=True).count()
    total_plants = Plant.query.filter_by(is_active=True).count()
    
    return render_template('home.html', 
                         featured_services=featured_services,
                         featured_plants=featured_plants,
                         stats={
                             'customers': total_customers,
                             'services': total_services,
                             'plants': total_plants
                         })

@main_bp.route('/about')
def about():
    return render_template('about.html')

@main_bp.route('/services')
def services():
    category = request.args.get('category', '')
    services_list = Service.query.filter_by(is_active=True)
    
    if category:
        services_list = services_list.filter_by(category=category)
    
    services_list = services_list.all()
    categories = db.session.query(Service.category).filter_by(is_active=True).distinct().all()
    
    return render_template('services.html', 
                         services=services_list,
                         categories=[c[0] for c in categories],
                         selected_category=category)

@main_bp.route('/faq')
def faq():
    faqs = [
        {
            'question': 'How do I book a service?',
            'answer': 'You can book a service by visiting our Booking page. Select the service you want, choose your preferred date and time, and confirm your booking. Our expert will contact you soon.'
        },
        {
            'question': 'What payment methods do you accept?',
            'answer': 'We accept UPI, Credit/Debit Cards, Net Banking through Razorpay. You can also choose Cash on Delivery for plant deliveries.'
        },
        {
            'question': 'How long does delivery take?',
            'answer': 'Standard delivery takes 2-3 business days. Express delivery is available for an additional charge.'
        },
        {
            'question': 'Can I cancel or reschedule a booking?',
            'answer': 'Yes, you can cancel or reschedule up to 24 hours before your booking. No cancellation fee applies for cancellations made within this period.'
        },
        {
            'question': 'Do you provide plant care tips?',
            'answer': 'Yes! Each plant comes with detailed care instructions. We also provide expert consultation services if you need personalized advice.'
        },
        {
            'question': 'What is your return policy?',
            'answer': 'Plants can be returned within 7 days if they arrive damaged. We offer replacement or full refund in such cases.'
        }
    ]
    
    return render_template('faq.html', faqs=faqs)

@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Handle contact form submission
        from models import SupportTicket
        import uuid
        
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        # Create a support ticket
        ticket = SupportTicket(
            ticket_number=f"TKT-{uuid.uuid4().hex[:8].upper()}",
            user_id=current_user.id if current_user.is_authenticated else None,
            subject=subject,
            message=message,
            category='query'
        )
        
        db.session.add(ticket)
        db.session.commit()
        
        from flask import flash
        flash('Your message has been received. We will contact you soon!', 'success')
        return render_template('contact.html', success=True)
    
    return render_template('contact.html')

@main_bp.route('/testimonials')
def testimonials():
    testimonials = [
        {
            'name': 'Rajesh Kumar',
            'city': 'Bangalore',
            'comment': 'Sugandhit Space transformed my balcony into a beautiful garden. The expert was very knowledgeable!',
            'rating': 5
        },
        {
            'name': 'Priya Singh',
            'city': 'Delhi',
            'comment': 'Great service and on-time delivery. The plants arrived in perfect condition.',
            'rating': 5
        },
        {
            'name': 'Amit Patel',
            'city': 'Mumbai',
            'comment': 'Monthly maintenance plan is excellent. My garden looks fantastic now!',
            'rating': 4.5
        }
    ]
    
    return render_template('testimonials.html', testimonials=testimonials)
