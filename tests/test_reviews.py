import json
from app import create_app
from app.extensions import db
from app.models import Review

def setup_module(module):
    """Set up test app and database."""
    global app, client
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
    client = app.test_client()

def teardown_module(module):
    """Tear down database."""
    with app.app_context():
        db.drop_all()

def test_submit_review():
    """Test submitting a new review."""
    response = client.post('/api/reviews/', json={
        'product_id': 1,
        'user_id': 1,
        'rating': 5,
        'comment': 'Excellent product!'
    })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['rating'] == 5
    assert data['comment'] == 'Excellent product!'

def test_get_reviews():
    """Test retrieving reviews for a product."""
    response = client.get('/api/reviews/product/1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) >= 1
