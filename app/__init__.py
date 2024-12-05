# File: /home/mohammad/E-commerce-1/app/__init__.py
from dotenv import load_dotenv
import os
from flask import Flask, request
from flask_cors import CORS  # Ensure Flask-CORS is imported
from app.extensions import db, migrate, limiter, logger  # Ensure all extensions are imported
from app.routes.customers import customer_bp
from app.routes.inventory import inventory_bp
from app.routes.sales import sales_bp
from app.routes.review import review_bp
from flask_session import Session  # For session management

# Load environment variables from .env
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///ecommerce.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_REDIS'] = Redis(host=os.getenv('REDIS_HOST', 'localhost'), port=6379)
    
    # Flask-Profiler Configuration
    app.config["flask_profiler"] = {
        "enabled": True,
        "storage": {
            "engine": "sqlite"  # Consistent with app.py
        },
        "basicAuth": {
            "enabled": False,
        },
        "ignore": ["^/static/.*"],
    }
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)
    CORS(app)
    Session(app)
    
    # Initialize Flask-Profiler
    from flask_profiler import Profiler
    Profiler(app)
    
    # Register blueprints
    app.register_blueprint(customer_bp, url_prefix='/api/customers')
    app.register_blueprint(inventory_bp, url_prefix='/api/inventory')
    app.register_blueprint(sales_bp, url_prefix='/api/sales')
    app.register_blueprint(review_bp, url_prefix='/api/reviews')
    
    # Health check route
    @app.route('/health', methods=['GET'])
    def global_health_check():
        """Check if the Flask app is running."""
        return {"status": "ok", "message": "App is running"}, 200
    
    # Error handler for rate limiting
    @app.errorhandler(429)
    def rate_limit_exceeded(e):
        return {"error": "Rate limit exceeded"}, 429
    
    # Logging
    @app.before_request
    def log_request_info():
        logger.info(f"Request: {request.method} {request.url} - Data: {request.get_json()}")
    
    @app.after_request
    def log_response_info(response):
        if hasattr(request, 'start_time'):
            elapsed_time = time.time() - request.start_time
            logger.info(f"Time taken: {elapsed_time:.4f}s for {request.method} {request.path}")
        logger.info(f"Response: {response.status} - Data: {response.get_data(as_text=True)}")
        return response
    
    return app
