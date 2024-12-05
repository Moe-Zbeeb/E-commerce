# tests/conftest.py
import pytest
from app import create_app
from app.extensions import db as _db
from app.models import Customer, Goods, Sales, InventoryItem, Review

@pytest.fixture(scope='session')
def app():
    """Create and configure a new app instance for each test session."""
    app = create_app(config_class='config.TestingConfig')
    
    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()
    
    yield app
    
    ctx.pop()

@pytest.fixture(scope='session')
def db(app):
    """Create a new database for the test session."""
    _db.create_all()
    
    yield _db
    
    _db.drop_all()

@pytest.fixture(scope='function')
def session(db):
    """Create a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()
    
    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)
    
    db.session = session
    
    yield session
    
    transaction.rollback()
    connection.close()
    session.remove()

@pytest.fixture(scope='function')
def client(app, session):
    """A test client for the app."""
    return app.test_client()
