from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Loads environment variables
load_dotenv()

# Connects to MongoDB
MONGODB_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGODB_URI)
db = client["petshop"]

# Retrieves database
def get_database():
    return db