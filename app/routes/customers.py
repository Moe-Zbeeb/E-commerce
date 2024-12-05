from flask import Blueprint, request, jsonify
from app.models import Customer 
from app.extensions import db
from sqlalchemy.sql import text 
customer_bp = Blueprint('customer_bp', __name__)

# Register a new customer
@customer_bp.route('/register', methods=['POST'])
def register_customer():
    data = request.get_json()
    if Customer.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already taken'}), 400

    new_customer = Customer(
        full_name=data['full_name'],
        username=data['username'],
        password=data['password'],  # In real apps, hash passwords!
        age=data['age'],
        address=data['address'],
        gender=data['gender'],
        marital_status=data['marital_status']
    )
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'message': 'Customer registered successfully'}), 201

# Get all customers
@customer_bp.route('/', methods=['GET'])
def get_all_customers():
    customers = Customer.query.all()
    return jsonify([{
        'id': customer.id,
        'full_name': customer.full_name,
        'username': customer.username,
        'wallet_balance': customer.wallet_balance
    } for customer in customers]), 200

# Get customer by username
@customer_bp.route('/<username>', methods=['GET'])
def get_customer(username):
    customer = Customer.query.filter_by(username=username).first()
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    return jsonify({
        'id': customer.id,
        'full_name': customer.full_name,
        'username': customer.username,
        'age': customer.age,
        'address': customer.address,
        'gender': customer.gender,
        'marital_status': customer.marital_status,
        'wallet_balance': customer.wallet_balance
    }), 200

# Update customer information
@customer_bp.route('/<username>', methods=['PUT'])
def update_customer(username):
    customer = Customer.query.filter_by(username=username).first()
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    data = request.get_json()
    for key, value in data.items():
        if hasattr(customer, key):
            setattr(customer, key, value)
    db.session.commit()
    return jsonify({'message': 'Customer updated successfully'}), 200

# Delete customer
@customer_bp.route('/<username>', methods=['DELETE'])
def delete_customer(username):
    customer = Customer.query.filter_by(username=username).first()
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': 'Customer deleted successfully'}), 200

# Charge wallet
@customer_bp.route('/<username>/charge', methods=['POST'])
def charge_wallet(username):
    customer = Customer.query.filter_by(username=username).first()
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    amount = request.get_json().get('amount', 0)
    customer.wallet_balance += amount
    db.session.commit()
    return jsonify({'message': f'{amount} charged to wallet', 'new_balance': customer.wallet_balance}), 200

# Deduct wallet
@customer_bp.route('/<username>/deduct', methods=['POST'])
def deduct_wallet(username):
    customer = Customer.query.filter_by(username=username).first()
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    amount = request.get_json().get('amount', 0)
    if customer.wallet_balance < amount:
        return jsonify({'error': 'Insufficient balance'}), 400
    customer.wallet_balance -= amount
    db.session.commit()
    return jsonify({'message': f'{amount} deducted from wallet', 'new_balance': customer.wallet_balance}), 200

@customer_bp.route('/health', methods=['GET'])
def customer_health_check():
    """Check if the Customer Service is healthy."""
    try:
        # Example: Check database connectivity
        db.session.execute(text('SELECT 1'))  # Explicitly wrap 'SELECT 1' with text()
        return {"status": "ok", "service": "Customer Service"}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500