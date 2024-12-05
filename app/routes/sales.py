from flask import Blueprint, request, jsonify
from app.models import Customer, Goods, Sales
from app.extensions import db, limiter
from app.messaging import publish_message  

# Define the blueprint
sales_bp = Blueprint('sales_bp', __name__)

# ===============================
# Service 3 - Sales Endpoints
# ===============================

# Apply rate limit to the "Display Goods" route
@limiter.limit("10 per minute")  # Allow 10 requests per minute
@sales_bp.route('/goods', methods=['GET'])
def display_goods():
    goods = Goods.query.all()
    return jsonify([
        {'name': good.name, 'price': good.price, 'quantity': good.quantity}
        for good in goods if good.quantity > 0
    ]), 200

# 2. Get goods details
@sales_bp.route('/goods/<good_name>', methods=['GET'])
def get_good_details(good_name):
    good = Goods.query.filter_by(name=good_name).first()
    if not good:
        return jsonify({'error': 'Good not found'}), 404
    return jsonify({
        'id': good.id,
        'name': good.name,
        'price': good.price,
        'quantity': good.quantity
    }), 200


# 3. Make a sale

@sales_bp.route('/purchase', methods=['POST'])
def make_sale():
    data = request.get_json()
    username = data.get('username')
    good_name = data.get('good_name')
    quantity = data.get('quantity', 1)

    # Fetch customer and good
    customer = Customer.query.filter_by(username=username).first()
    good = Goods.query.filter_by(name=good_name).first()

    # Validations
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    if not good:
        return jsonify({'error': 'Good not found'}), 404
    if good.quantity < quantity:
        return jsonify({'error': 'Not enough stock available'}), 400
    total_price = good.price * quantity
    if customer.wallet_balance < total_price:
        return jsonify({'error': 'Insufficient wallet balance'}), 400

    # Process Sale
    customer.wallet_balance -= total_price
    good.quantity -= quantity
    sale = Sales(customer_id=customer.id, good_id=good.id, quantity=quantity, total_price=total_price)
    db.session.add(sale)
    db.session.commit()

    # Send a notification to RabbitMQ
    message = f"Sale completed: {username} purchased {quantity} x {good_name} for ${total_price:.2f}"
    publish_message(message)

    return jsonify({'message': 'Purchase successful', 'remaining_balance': customer.wallet_balance}), 200


# 4. Purchase history
@sales_bp.route('/history/<username>', methods=['GET'])
def purchase_history(username):
    customer = Customer.query.filter_by(username=username).first()
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    sales = Sales.query.filter_by(customer_id=customer.id).all()
    return jsonify([
        {
            'good_name': Goods.query.get(sale.good_id).name,
            'quantity': sale.quantity,
            'total_price': sale.total_price,
            'timestamp': sale.timestamp
        }
        for sale in sales
    ]), 200
    
@sales_bp.route('/health', methods=['GET'])
def sales_health_check():
    """Check if the Sales Service is healthy."""
    try:
        # Example: Check database connectivity
        db.session.execute('SELECT 1')
        return {"status": "ok", "service": "Sales Service"}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500
    
