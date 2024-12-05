import logging
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy
from redis import Redis

# Initialize Redis connection
redis_connection = Redis(host='localhost', port=6379)

# Initialize shared extensions
db = SQLAlchemy()
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="redis://localhost:6379"  # Use Redis as the storage backend
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # Log to a file
        logging.StreamHandler()         # Log to the console
    ]
)
logger = logging.getLogger(__name__)