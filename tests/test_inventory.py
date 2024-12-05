# tests/test_inventory.py
import json

def test_add_goods_success(client, session):
    payload = {
        "name": "Test Gadget",
        "category": "Electronics",
        "pricePerItem": 299.99,
        "description": "A test electronic gadget.",
        "countInStock": 50
    }
    response = client.post('/api/inventory/', json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data['name'] == 'Test Gadget'
    assert data['id'] is not None

def test_add_goods_missing_fields(client, session):
    payload = {
        "name": "Incomplete Gadget",
        # Missing category, pricePerItem, etc.
    }
    response = client.post('/api/inventory/', json=payload)
    assert response.status_code == 400  # Assuming your endpoint handles missing fields
    data = response.get_json()
    assert 'error' in data

def test_deduct_goods_success(client, session):
    # First, add a good
    add_payload = {
        "name": "Deductible Gadget",
        "category": "Accessories",
        "pricePerItem": 49.99,
        "description": "A gadget to test deduction.",
        "countInStock": 100
    }
    response = client.post('/api/inventory/', json=add_payload)
    assert response.status_code == 201
    data = response.get_json()
    item_id = data['id']

    # Deduct goods
    deduct_payload = {
        "itemId": item_id,
        "quantity": 10
    }
    response = client.post('/api/inventory/deduct', json=deduct_payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data['count_in_stock'] == 90

def test_deduct_goods_not_enough_stock(client, session):
    # Add a good with limited stock
    add_payload = {
        "name": "Limited Stock Gadget",
        "category": "Electronics",
        "pricePerItem": 199.99,
        "description": "A gadget with limited stock.",
        "countInStock": 5
    }
    response = client.post('/api/inventory/', json=add_payload)
    assert response.status_code == 201
    data = response.get_json()
    item_id = data['id']

    # Attempt to deduct more than available
    deduct_payload = {
        "itemId": item_id,
        "quantity": 10
    }
    response = client.post('/api/inventory/deduct', json=deduct_payload)
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'Not enough stock'

def test_deduct_goods_not_found(client, session):
    deduct_payload = {
        "itemId": 9999,  # Assuming this ID doesn't exist
        "quantity": 1
    }
    response = client.post('/api/inventory/deduct', json=deduct_payload)
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == 'Item not found'

def test_update_goods_success(client, session):
    # Add a good
    add_payload = {
        "name": "Updatable Gadget",
        "category": "Clothes",
        "pricePerItem": 59.99,
        "description": "A gadget that can be updated.",
        "countInStock": 30
    }
    response = client.post('/api/inventory/', json=add_payload)
    assert response.status_code == 201
    data = response.get_json()
    item_id = data['id']

    # Update the good's price and stock
    update_payload = {
        "pricePerItem": 69.99,
        "countInStock": 25
    }
    response = client.put(f'/api/inventory/{item_id}', json=update_payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'Updatable Gadget'

    # Verify updates
    response = client.get('/api/sales/goods')  # Assuming /sales/goods returns all goods
    assert response.status_code == 200
    goods = response.get_json()
    updated_good = next((g for g in goods if g['name'] == 'Updatable Gadget'), None)
    assert updated_good is not None
    assert updated_good['price'] == 69.99
    assert updated_good['quantity'] == 25

def test_update_goods_not_found(client, session):
    update_payload = {
        "pricePerItem": 99.99
    }
    response = client.put('/api/inventory/9999', json=update_payload)  # Non-existent ID
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == 'Item not found'

def test_inventory_health_check(client, session):
    response = client.get('/api/inventory/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ok'
    assert data['service'] == 'Inventory Service'
