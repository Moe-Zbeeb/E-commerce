# tests/test_sales.py
import json

def test_display_goods_success(client, session):
    # Add some goods
    goods = [
        {
            "name": "Sale Gadget 1",
            "category": "Electronics",
            "pricePerItem": 150.0,
            "description": "First sale gadget.",
            "countInStock": 10
        },
        {
            "name": "Sale Gadget 2",
            "category": "Accessories",
            "pricePerItem": 75.0,
            "description": "Second sale gadget.",
            "countInStock": 0  # Out of stock
        }
    ]
    for good in goods:
        client.post('/api/inventory/', json=good)

    response = client.get('/api/sales/goods')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1  # Only one good is in stock
    assert data[0]['name'] == 'Sale Gadget 1'

def test_get_good_details_success(client, session):
    # Add a good
    good_payload = {
        "name": "Detailed Gadget",
        "category": "Food",
        "pricePerItem": 25.0,
        "description": "A gadget with details.",
        "countInStock": 20
    }
    client.post('/api/inventory/', json=good_payload)

    response = client.get('/api/sales/goods/Detailed Gadget')
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'Detailed Gadget'
    assert data['category'] == 'Food'
    assert data['price'] == 25.0
    assert data['quantity'] == 20

def test_get_good_details_not_found(client, session):
    response = client.get('/api/sales/goods/NonExistentGadget')
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == 'Good not found'

def test_make_sale_success(client, session):
    # Register a customer
    customer_payload = {
        "full_name": "Sale User",
        "username": "saleuser",
        "password": "salepassword",
        "age": 30,
        "address": "555 Sale St",
        "gender": "Male",
        "marital_status": "Married"
    }
    client.post('/api/customers/register', json=customer_payload)

    # Charge the customer's wallet
    charge_payload = {
        "amount": 500.0
    }
    client.post('/api/customers/saleuser/charge', json=charge_payload)

    # Add a good
    good_payload = {
        "name": "Sale Item",
        "category": "Electronics",
        "pricePerItem": 100.0,
        "description": "Item for sale.",
        "countInStock": 5
    }
    client.post('/api/inventory/', json=good_payload)

    # Make a purchase
    purchase_payload = {
        "username": "saleuser",
        "good_name": "Sale Item",
        "quantity": 3
    }
    response = client.post('/api/sales/purchase', json=purchase_payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Purchase successful'
    assert data['remaining_balance'] == 200.0

def test_make_sale_insufficient_balance(client, session):
    # Register a customer
    customer_payload = {
        "full_name": "Low Balance User",
        "username": "lowbalanceuser",
        "password": "lowbalancepassword",
        "age": 22,
        "address": "666 Low St",
        "gender": "Female",
        "marital_status": "Single"
    }
    client.post('/api/customers/register', json=customer_payload)

    # Charge the customer's wallet with insufficient funds
    charge_payload = {
        "amount": 50.0
    }
    client.post('/api/customers/lowbalanceuser/charge', json=charge_payload)

    # Add a good
    good_payload = {
        "name": "Expensive Item",
        "category": "Electronics",
        "pricePerItem": 100.0,
        "description": "An expensive item.",
        "countInStock": 10
    }
    client.post('/api/inventory/', json=good_payload)

    # Attempt to make a purchase exceeding balance
    purchase_payload = {
        "username": "lowbalanceuser",
        "good_name": "Expensive Item",
        "quantity": 1
    }
    response = client.post('/api/sales/purchase', json=purchase_payload)
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'Insufficient wallet balance'

def test_make_sale_not_enough_stock(client, session):
    # Register a customer
    customer_payload = {
        "full_name": "Stock User",
        "username": "stockuser",
        "password": "stockpassword",
        "age": 29,
        "address": "777 Stock St",
        "gender": "Male",
        "marital_status": "Single"
    }
    client.post('/api/customers/register', json=customer_payload)

    # Charge the customer's wallet
    charge_payload = {
        "amount": 1000.0
    }
    client.post('/api/customers/stockuser/charge', json=charge_payload)

    # Add a good with limited stock
    good_payload = {
        "name": "Limited Stock Item",
        "category": "Accessories",
        "pricePerItem": 50.0,
        "description": "Limited stock item.",
        "countInStock": 2
    }
    client.post('/api/inventory/', json=good_payload)

    # Attempt to purchase more than available stock
    purchase_payload = {
        "username": "stockuser",
        "good_name": "Limited Stock Item",
        "quantity": 5
    }
    response = client.post('/api/sales/purchase', json=purchase_payload)
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'Not enough stock available'

def test_make_sale_customer_not_found(client, session):
    purchase_payload = {
        "username": "nonexistentuser",
        "good_name": "Any Item",
        "quantity": 1
    }
    response = client.post('/api/sales/purchase', json=purchase_payload)
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == 'Customer not found'

def test_make_sale_good_not_found(client, session):
    # Register a customer
    customer_payload = {
        "full_name": "Good User",
        "username": "gooduser",
        "password": "goodpassword",
        "age": 31,
        "address": "888 Good St",
        "gender": "Female",
        "marital_status": "Married"
    }
    client.post('/api/customers/register', json=customer_payload)

    # Charge the customer's wallet
    charge_payload = {
        "amount": 500.0
    }
    client.post('/api/customers/gooduser/charge', json=charge_payload)

    # Attempt to purchase a non-existent good
    purchase_payload = {
        "username": "gooduser",
        "good_name": "NonExistentGood",
        "quantity": 1
    }
    response = client.post('/api/sales/purchase', json=purchase_payload)
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == 'Good not found'

def test_purchase_history_success(client, session):
    # Register and charge a customer
    customer_payload = {
        "full_name": "History User",
        "username": "historyuser",
        "password": "historypassword",
        "age": 26,
        "address": "999 History St",
        "gender": "Male",
        "marital_status": "Single"
    }
    client.post('/api/customers/register', json=customer_payload)
    charge_payload = {
        "amount": 500.0
    }
    client.post('/api/customers/historyuser/charge', json=charge_payload)

    # Add a good
    good_payload = {
        "name": "History Item",
        "category": "Food",
        "pricePerItem": 50.0,
        "description": "Item for history testing.",
        "countInStock": 10
    }
    client.post('/api/inventory/', json=good_payload)

    # Make a purchase
    purchase_payload = {
        "username": "historyuser",
        "good_name": "History Item",
        "quantity": 2
    }
    client.post('/api/sales/purchase', json=purchase_payload)

    # Fetch purchase history
    response = client.get('/api/sales/history/historyuser')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['good_name'] == 'History Item'
    assert data[0]['quantity'] == 2
    assert data[0]['total_price'] == 100.0
    assert 'timestamp' in data[0]

def test_purchase_history_customer_not_found(client, session):
    response = client.get('/api/sales/history/nonexistentuser')
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == 'Customer not found'

def test_sales_health_check(client, session):
    response = client.get('/api/sales/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ok'
    assert data['service'] == 'Sales Service'
