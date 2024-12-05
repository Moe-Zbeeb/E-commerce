import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from app.extensions import db, limiter, logger  # Updated import paths
from app.routes.customers import customer_bp  # Updated import paths
from app.routes.inventory import inventory_bp  # Updated import paths
from app.routes.sales import sales_bp  # Updated import paths
from app.routes.review import review_bp 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
limiter.init_app(app)  # Attach limiter to app
migrate = Migrate(app, db)

@app.errorhandler(429)
def rate_limit_exceeded(e):
    return jsonify({'error': 'Rate limit exceeded'}), 429

# Register blueprints
app.register_blueprint(customer_bp, url_prefix='/api/customers')
app.register_blueprint(inventory_bp, url_prefix='/api/inventory')
app.register_blueprint(sales_bp, url_prefix='/api/sales')
app.register_blueprint(review_bp, url_prefix='/api/reviews')

@app.route('/health', methods=['GET'])
def global_health_check():
    """Check if the Flask app is running."""
    return {"status": "ok", "message": "App is running"}, 200

@app.before_request
def log_request_info():
    logger.info(f"Request: {request.method} {request.url} - Data: {request.get_json()}")

@app.after_request
def log_response_info(response):
    logger.info(f"Response: {response.status} - Data: {response.get_data(as_text=True)}")
    return response
    
if __name__ == "__main__":
    app.run(debug=True)