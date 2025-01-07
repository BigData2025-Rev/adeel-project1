from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
from os import getenv


# Load environment variables from .env
load_dotenv()

# Access variables
uri = getenv("MONGO_URI")
if not uri:
    raise ValueError("MONGO_URI environment variable not set")

# Get database connection
def get_database():
    try:
        client = MongoClient(uri)
        db = client["shopping"]
        return db
    except Exception as e:
        print(e)