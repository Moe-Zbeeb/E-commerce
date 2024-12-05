# File: /home/mohammad/E-commerce-1/app/seed_data.py
from app import create_app
from app.extensions import db
from app.models import Goods
import os

app = create_app()

with app.app_context():
    # Drop and recreate the database for a clean slate (optional)
    db.drop_all()
    db.create_all()

    # Sample data for the Goods table
    goods_list = [
        Goods(name="Laptop", price=1000.0, quantity=10),
        Goods(name="Phone", price=500.0, quantity=20),
        Goods(name="Headphones", price=100.0, quantity=30),
        Goods(name="Monitor", price=300.0, quantity=15),
        Goods(name="Keyboard", price=50.0, quantity=25),
    ]

    # Add goods to the database
    db.session.bulk_save_objects(goods_list)
    db.session.commit()

    print("Goods table seeded successfully!")
