from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///ecommerce.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)
    CORS(app)
    
    # Register blueprints
    from app.routes.customers import customer_bp
    from app.routes.inventory import inventory_bp
    from app.routes.sales import sales_bp
    from app.routes.review import review_bp
    
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
        logger.info(f"Response: {response.status} - Data: {response.get_data(as_text=True)}")
        return response
    
    return app
