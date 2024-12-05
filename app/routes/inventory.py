from flask import Blueprint, request, jsonify
from app.models import InventoryItem
from app.extensions import db

inventory_bp = Blueprint('inventory_bp', __name__)

# Add goods
@inventory_bp.route('/', methods=['POST'])
def add_goods():
    data = request.get_json()
    new_item = InventoryItem(
        name=data['name'],
        category=data['category'],
        price_per_item=data['pricePerItem'],
        description=data['description'],
        count_in_stock=data['countInStock']
    )
    db.session.add(new_item)
    db.session.commit()
    return jsonify({'id': new_item.id, 'name': new_item.name}), 201

# Deduct goods
@inventory_bp.route('/deduct', methods=['POST'])
def deduct_goods():
    data = request.get_json()
    item = InventoryItem.query.get(data['itemId'])
    if item and item.count_in_stock >= data['quantity']:
        item.count_in_stock -= data['quantity']
        db.session.commit()
        return jsonify({'id': item.id, 'count_in_stock': item.count_in_stock}), 200
    elif not item:
        return jsonify({'error': 'Item not found'}), 404
    else:
        return jsonify({'error': 'Not enough stock'}), 400

# Update goods
@inventory_bp.route('/<int:item_id>', methods=['PUT'])
def update_goods(item_id):
    data = request.get_json()
    item = InventoryItem.query.get(item_id)
    if item:
        item.name = data.get('name', item.name)
        item.category = data.get('category', item.category)
        item.price_per_item = data.get('pricePerItem', item.price_per_item)
        item.description = data.get('description', item.description)
        item.count_in_stock = data.get('countInStock', item.count_in_stock)
        db.session.commit()
        return jsonify({'id': item.id, 'name': item.name}), 200
    else:
        return jsonify({'error': 'Item not found'}), 404
    
@inventory_bp.route('/health', methods=['GET'])
def inventory_health_check():
    """Check if the Inventory Service is healthy."""
    try:
        # Example: Check database connectivity
        db.session.execute('SELECT 1')
        return {"status": "ok", "service": "Inventory Service"}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500