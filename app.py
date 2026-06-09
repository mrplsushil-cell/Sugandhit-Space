from flask import Flask, render_template, redirect, url_for, request, jsonify, flash
from flask_login import LoginManager, login_required, current_user, logout_user
from flask_jwt_extended import JWTManager
from config import config
from models import db, User, Service, Plant, Order, Booking, SupportTicket
import os
from datetime import datetime

def create_app(config_name='development'):
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    jwt = JWTManager(app)
    
    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.main import main_bp
    from routes.catalog import catalog_bp
    from routes.booking import booking_bp
    from routes.order import order_bp
    from routes.payment import payment_bp
    from routes.support import support_bp
    from routes.admin import admin_bp
    from routes.dashboard import dashboard_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(catalog_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(payment_bp)
    app.register_blueprint(support_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(dashboard_bp)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def server_error(e):
        return render_template('500.html'), 500
    
    @app.context_processor
    def inject_user():
        return {'current_user': current_user}
    
    @app.template_filter('currency')
    def currency_filter(value):
        try:
            value = float(value)
            return f"₹{value:,.2f}"
        except (ValueError, TypeError):
            return f"₹{value}"
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
