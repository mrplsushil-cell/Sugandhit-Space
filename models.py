from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from enum import Enum

db = SQLAlchemy()

class UserRole(Enum):
    CUSTOMER = 'customer'
    EXPERT = 'expert'
    ADMIN = 'admin'

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(255))
    role = db.Column(db.String(20), default=UserRole.CUSTOMER.value)
    address = db.Column(db.Text)
    city = db.Column(db.String(50))
    pincode = db.Column(db.String(10))
    profile_image = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'role': self.role,
            'city': self.city
        }

class Service(db.Model):
    __tablename__ = 'services'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50), nullable=False)  # maintenance, design, visit, plantation
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(255))
    duration = db.Column(db.String(50))  # e.g., "1-2 hours", "Monthly"
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'price': self.price,
            'image': self.image,
            'duration': self.duration
        }

class Plant(db.Model):
    __tablename__ = 'plants'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    scientific_name = db.Column(db.String(120))
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, default=0)
    image = db.Column(db.String(255))
    category = db.Column(db.String(50))  # indoor, outdoor, herb, flowering
    care_tips = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    order_items = db.relationship('OrderItem', backref='plant', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'quantity': self.quantity,
            'image': self.image,
            'category': self.category
        }

class Booking(db.Model):
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    booking_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, completed, cancelled
    notes = db.Column(db.Text)
    expert_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    customer = db.relationship('User', foreign_keys=[user_id], backref='customer_bookings')
    expert = db.relationship('User', foreign_keys=[expert_id], backref='expert_bookings')
    service = db.relationship('Service', backref='bookings')
    
    def to_dict(self):
        return {
            'id': self.id,
            'service_name': self.service.name,
            'booking_date': self.booking_date.isoformat(),
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(20), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    tax = db.Column(db.Float, default=0)
    delivery_charge = db.Column(db.Float, default=0)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, processing, shipped, delivered, cancelled
    payment_status = db.Column(db.String(20), default='pending')  # pending, completed, failed
    delivery_address = db.Column(db.Text)
    delivery_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = db.relationship('User', backref='orders')
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')
    payment = db.relationship('Payment', backref='order', uselist=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_number': self.order_number,
            'total_amount': self.total_amount,
            'status': self.status,
            'payment_status': self.payment_status,
            'created_at': self.created_at.isoformat()
        }

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    plant_id = db.Column(db.Integer, db.ForeignKey('plants.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    
    def to_dict(self):
        return {
            'plant_name': self.plant.name,
            'quantity': self.quantity,
            'price': self.price
        }

class Payment(db.Model):
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    razorpay_payment_id = db.Column(db.String(100))
    razorpay_order_id = db.Column(db.String(100))
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), default='INR')
    status = db.Column(db.String(20), default='pending')  # pending, completed, failed
    method = db.Column(db.String(50))  # upi, card, netbanking, wallet
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class DeliveryTracking(db.Model):
    __tablename__ = 'delivery_tracking'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False, unique=True)
    current_location = db.Column(db.String(200))
    delivery_person = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    status = db.Column(db.String(50), default='pending')  # pending, dispatched, out_for_delivery, delivered
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    estimated_delivery = db.Column(db.DateTime)
    
    order = db.relationship('Order', backref='tracking')

class SupportTicket(db.Model):
    __tablename__ = 'support_tickets'
    
    id = db.Column(db.Integer, primary_key=True)
    ticket_number = db.Column(db.String(20), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50))  # complaint, feedback, query
    status = db.Column(db.String(20), default='open')  # open, in_progress, resolved, closed
    priority = db.Column(db.String(20), default='medium')  # low, medium, high
    response = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = db.relationship('User', backref='support_tickets')

class ReviewRating(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))
    plant_id = db.Column(db.Integer, db.ForeignKey('plants.id'))
    rating = db.Column(db.Float, nullable=False)  # 1-5
    review_text = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='reviews')
