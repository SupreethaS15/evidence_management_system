from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['risk_prediction_db']
users_collection = db['users']

# Example users to insert
sample_users = [
    {
        "username": "admin",
        "password": "admin123"  # Hashed password
    },
    {
        "username": "user1",
        "password": "user1234" # Hashed password
    },
    {
        "username": "user2",
        "password": "password5678" # Hashed password
    }
]

# Insert users into MongoDB
users_collection.insert_many(sample_users)
print("Inserted")