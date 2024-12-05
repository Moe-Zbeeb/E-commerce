from app.app import app
from app.extensions import db
from sqlalchemy import text  # Import the text function for raw SQL

# Use the Flask app context
with app.app_context():
    # Reset the alembic_version table
    with db.engine.connect() as connection:
        connection.execute(text("DROP TABLE IF EXISTS alembic_version;"))
    print("Alembic version table reset successfully.")