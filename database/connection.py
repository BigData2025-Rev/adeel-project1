from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
from os import getenv
from utils import logger

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
        db = client["shopping_app"]
        logger.info("Connected to database")
        return db
    except Exception as e:
        logger.error("Unable to connect to database")
        print(e)