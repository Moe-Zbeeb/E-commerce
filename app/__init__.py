from flask import Flask
from app.extensions import db
from app.app import migrate# Ensure these are imported

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints here
    from app.routes.customers import customer_bp
    app.register_blueprint(customer_bp, url_prefix='/api/customers')

    return app