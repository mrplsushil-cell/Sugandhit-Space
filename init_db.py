#!/usr/bin/env python
"""
Database initialization script - creates tables and adds sample data
Run this after first installation: python init_db.py
"""

from app import create_app
from models import db, User, Service, Plant, UserRole
from datetime import datetime

def init_db():
    """Initialize database with tables and sample data"""
    app = create_app()
    
    with app.app_context():
        # Create all tables
        print("Creating database tables...")
        db.create_all()
        print("✓ Database tables created successfully")
        
        # Check if admin exists
        admin = User.query.filter_by(email='admin@sugandhit.com').first()
        if not admin:
            print("\nCreating admin user...")
            admin = User(
                name='Admin User',
                email='admin@sugandhit.com',
                phone='9999999999',
                role='admin'
            )
            admin.set_password('admin@123')
            db.session.add(admin)
            print("✓ Admin user created (email: admin@sugandhit.com, password: admin@123)")
        
        # Check if sample services exist
        services_count = Service.query.count()
        if services_count == 0:
            print("\nAdding sample services...")
            services = [
                Service(
                    name='Garden Maintenance (Monthly)',
                    description='Professional monthly garden maintenance including watering, pruning, and pest control',
                    category='maintenance',
                    price=5000,
                    duration='1 visit/month',
                    is_active=True
                ),
                Service(
                    name='Expert Garden Visit',
                    description='One-time expert consultation visit for garden inspection and advice',
                    category='visit',
                    price=2000,
                    duration='1-2 hours',
                    is_active=True
                ),
                Service(
                    name='Custom Garden Design',
                    description='Professional landscaping and custom garden design for balcony, terrace, or garden',
                    category='design',
                    price=15000,
                    duration='3-5 days',
                    is_active=True
                ),
                Service(
                    name='Herbal Plantation',
                    description='Organic herb plantation service with soil preparation and plant care',
                    category='plantation',
                    price=3000,
                    duration='1 day',
                    is_active=True
                ),
            ]
            db.session.add_all(services)
            print(f"✓ Added {len(services)} sample services")
        
        # Check if sample plants exist
        plants_count = Plant.query.count()
        if plants_count == 0:
            print("\nAdding sample plants...")
            plants = [
                Plant(
                    name='Money Plant',
                    scientific_name='Epipremnum aureum',
                    description='Popular indoor plant that brings good luck and positive energy',
                    price=299,
                    quantity=50,
                    category='indoor',
                    care_tips='Water weekly, keep in indirect light, humid environment preferred',
                    is_active=True
                ),
                Plant(
                    name='Snake Plant',
                    scientific_name='Sansevieria trifasciata',
                    description='Hardy succulent with air-purifying properties, low maintenance',
                    price=499,
                    quantity=30,
                    category='indoor',
                    care_tips='Water every 2-3 weeks, can tolerate low light',
                    is_active=True
                ),
                Plant(
                    name='Tulsi (Holy Basil)',
                    scientific_name='Ocimum sanctum',
                    description='Medicinal herb with spiritual significance',
                    price=199,
                    quantity=100,
                    category='herb',
                    care_tips='Needs sunlight, moderate watering',
                    is_active=True
                ),
                Plant(
                    name='Tomato Plant',
                    scientific_name='Solanum lycopersicum',
                    description='Organic tomato plant for home gardening',
                    price=149,
                    quantity=40,
                    category='vegetable',
                    care_tips='Needs 6-8 hours of sunlight, water regularly',
                    is_active=True
                ),
                Plant(
                    name='Jasmine',
                    scientific_name='Jasminum sambac',
                    description='Fragrant flowering plant with white blooms',
                    price=399,
                    quantity=25,
                    category='outdoor',
                    care_tips='Needs sunlight, regular watering, monthly fertilizer',
                    is_active=True
                ),
                Plant(
                    name='Pothos',
                    scientific_name='Epipremnum pinnatum',
                    description='Climbing plant perfect for walls and trellises',
                    price=349,
                    quantity=35,
                    category='indoor',
                    care_tips='Adapts to various light conditions, water moderately',
                    is_active=True
                ),
            ]
            db.session.add_all(plants)
            print(f"✓ Added {len(plants)} sample plants")
        
        db.session.commit()
        print("\n✅ Database initialization complete!")
        print("\n🌿 Sugandhit Space is ready to run!")
        print("Use 'python app.py' to start the application")

if __name__ == '__main__':
    init_db()
