# tests/test_customers.py
import json

def test_register_customer_success(client, session):
    payload = {
        "full_name": "Test User",
        "username": "testuser",
        "password": "testpassword",
        "age": 25,
        "address": "123 Test Street",
        "gender": "Non-binary",
        "marital_status": "Single"
    }
    response = client.post('/api/customers/register', json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Customer registered successfully'
    

def test_register_customer(test_client):
    response = test_client.post("/api/customers/register", json={
        "full_name": "Test User",
        "username": "testuser",
        "password": "testpass",
        "age": 25,
        "address": "123 Test St",
        "gender": "Male",
        "marital_status": "Single"
    })
    assert response.status_code == 201
    assert response.json["message"] == "Customer registered successfully"

def test_get_customer(test_client):
    response = test_client.get("/api/customers/testuser")
    assert response.status_code == 200
    assert response.json["username"] == "testuser"
    
    
def test_register_customer_duplicate_username(client, session):
    # First registration
    payload = {
        "full_name": "Test User",
        "username": "duplicateuser",
        "password": "testpassword",
        "age": 25,
        "address": "123 Test Street",
        "gender": "Non-binary",
        "marital_status": "Single"
    }
    response = client.post('/api/customers/register', json=payload)
    assert response.status_code == 201

    # Attempt duplicate registration
    response = client.post('/api/customers/register', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'Username already taken'

def test_get_all_customers(client, session):
    # Register two customers
    customers = [
        {
            "full_name": "User One",
            "username": "userone",
            "password": "password1",
            "age": 30,
            "address": "456 First Ave",
            "gender": "Male",
            "marital_status": "Married"
        },
        {
            "full_name": "User Two",
            "username": "usertwo",
            "password": "password2",
            "age": 22,
            "address": "789 Second Ave",
            "gender": "Female",
            "marital_status": "Single"
        }
    ]
    for customer in customers:
        client.post('/api/customers/register', json=customer)

    response = client.get('/api/customers/')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2
    assert data[0]['username'] == 'userone'
    assert data[1]['username'] == 'usertwo'

def test_get_customer_by_username_success(client, session):
    # Register a customer
    payload = {
        "full_name": "Unique User",
        "username": "uniqueuser",
        "password": "uniquepassword",
        "age": 28,
        "address": "321 Unique St",
        "gender": "Female",
        "marital_status": "Single"
    }
    client.post('/api/customers/register', json=payload)

    # Fetch the customer
    response = client.get('/api/customers/uniqueuser')
    assert response.status_code == 200
    data = response.get_json()
    assert data['username'] == 'uniqueuser'
    assert data['full_name'] == 'Unique User'
    assert data['wallet_balance'] == 0.0

def test_get_customer_by_username_not_found(client, session):
    response = client.get('/api/customers/nonexistentuser')
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == 'Customer not found'

def test_update_customer_success(client, session):
    # Register a customer
    payload = {
        "full_name": "Update User",
        "username": "updateuser",
        "password": "updatepassword",
        "age": 35,
        "address": "654 Update St",
        "gender": "Male",
        "marital_status": "Married"
    }
    client.post('/api/customers/register', json=payload)

    # Update the customer's address and age
    update_payload = {
        "address": "987 Updated Ave",
        "age": 36
    }
    response = client.put('/api/customers/updateuser', json=update_payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Customer updated successfully'

    # Verify the update
    response = client.get('/api/customers/updateuser')
    data = response.get_json()
    assert data['address'] == '987 Updated Ave'
    assert data['age'] == 36

def test_update_customer_not_found(client, session):
    update_payload = {
        "address": "No Where Ave",
        "age": 40
    }
    response = client.put('/api/customers/nonexistentuser', json=update_payload)
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == 'Customer not found'

def test_delete_customer_success(client, session):
    # Register a customer
    payload = {
        "full_name": "Delete User",
        "username": "deleteuser",
        "password": "deletepassword",
        "age": 40,
        "address": "111 Delete St",
        "gender": "Female",
        "marital_status": "Divorced"
    }
    client.post('/api/customers/register', json=payload)

    # Delete the customer
    response = client.delete('/api/customers/deleteuser')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Customer deleted successfully'

    # Verify deletion
    response = client.get('/api/customers/deleteuser')
    assert response.status_code == 404

def test_delete_customer_not_found(client, session):
    response = client.delete('/api/customers/nonexistentuser')
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == 'Customer not found'

def test_charge_wallet_success(client, session):
    # Register a customer
    payload = {
        "full_name": "Charge User",
        "username": "chargeuser",
        "password": "chargepassword",
        "age": 27,
        "address": "222 Charge St",
        "gender": "Male",
        "marital_status": "Single"
    }
    client.post('/api/customers/register', json=payload)

    # Charge the wallet
    charge_payload = {
        "amount": 250.0
    }
    response = client.post('/api/customers/chargeuser/charge', json=charge_payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == '250.0 charged to wallet'
    assert data['new_balance'] == 250.0

def test_charge_wallet_customer_not_found(client, session):
    charge_payload = {
        "amount": 100.0
    }
    response = client.post('/api/customers/nonexistentuser/charge', json=charge_payload)
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == 'Customer not found'

def test_deduct_wallet_success(client, session):
    # Register and charge the customer
    payload = {
        "full_name": "Deduct User",
        "username": "deductuser",
        "password": "deductpassword",
        "age": 32,
        "address": "333 Deduct St",
        "gender": "Female",
        "marital_status": "Married"
    }
    client.post('/api/customers/register', json=payload)
    charge_payload = {
        "amount": 300.0
    }
    client.post('/api/customers/deductuser/charge', json=charge_payload)

    # Deduct from the wallet
    deduct_payload = {
        "amount": 150.0
    }
    response = client.post('/api/customers/deductuser/deduct', json=deduct_payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == '150.0 deducted from wallet'
    assert data['new_balance'] == 150.0

def test_deduct_wallet_insufficient_balance(client, session):
    # Register and charge the customer
    payload = {
        "full_name": "Insufficient User",
        "username": "insufficientuser",
        "password": "insufficientpassword",
        "age": 29,
        "address": "444 Insufficient St",
        "gender": "Male",
        "marital_status": "Single"
    }
    client.post('/api/customers/register', json=payload)
    charge_payload = {
        "amount": 100.0
    }
    client.post('/api/customers/insufficientuser/charge', json=charge_payload)

    # Attempt to deduct more than the balance
    deduct_payload = {
        "amount": 150.0
    }
    response = client.post('/api/customers/insufficientuser/deduct', json=deduct_payload)
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'Insufficient balance'

def test_deduct_wallet_customer_not_found(client, session):
    deduct_payload = {
        "amount": 50.0
    }
    response = client.post('/api/customers/nonexistentuser/deduct', json=deduct_payload)
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == 'Customer not found'
