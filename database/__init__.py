from .connection import get_database

# Get the database connection
db = get_database()

# Define collections
accounts = db["accounts"]
items = db["items"]
orders = db["orders"]

__all__ = ["accounts", "items", "orders"]