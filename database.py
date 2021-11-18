import os
from pymongo import MongoClient

host = os.environ.get("MONGODB_URI", "mongodb://localhost:27017/Charity-tracker")
client = MongoClient(host=host)
db = client.get_default_database()

users = db.users
donations = db.donations
charities = db.charities
