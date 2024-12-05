# File: /home/mohammad/E-commerce-1/app/extensions.py
import logging
from flask_sqlalchemy import SQLAlchemy
from redis import Redis
from sqlalchemy import event
import time
import os  # Import os module
from flask_session import Session  # For session management

# Initialize Redis connection
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
redis_connection = Redis(host=REDIS_HOST, port=6379)

# Initialize shared extensions
db = SQLAlchemy()

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Log Formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Console Handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# File Handler
file_handler = logging.FileHandler("app.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# SQLAlchemy Query Profiling
@event.listens_for(db.engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    conn.info.setdefault("query_start_time", []).append(time.time())
    logger.info(f"Executing Query: {statement}")

@event.listens_for(db.engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total = time.time() - conn.info["query_start_time"].pop(-1)
    logger.info(f"Query Executed in {total:.4f}s")
