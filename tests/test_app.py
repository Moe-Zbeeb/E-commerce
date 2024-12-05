import json
from app import create_app

def test_health_check():
    """Test the global health check endpoint."""
    app = create_app()
    client = app.test_client()
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == "ok"
