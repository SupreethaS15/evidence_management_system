from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['risk_prediction_db']
evidence_collection = db['evidences']

# Example evidence records to insert
sample_evidences = [
    {
        "username": "admin",
        "image_filename": "evidence_image_1.png",
        "temperature": 25.3,
        "humidity": 60.5,
        "vibration": 1,  # 1 means "Yes"
        "light_intensity": 400.0,
        "battery_level": 85.0,
        "latitude": 37.7749,
        "longitude": -122.4194,
        "risk_prediction": "High Risk"
    },
    {
        "username": "user1",
        "image_filename": "evidence_image_2.png",
        "temperature": 22.1,
        "humidity": 55.3,
        "vibration": 0,  # 0 means "No"
        "light_intensity": 500.0,
        "battery_level": 90.0,
        "latitude": 40.7128,
        "longitude": -74.0060,
        "risk_prediction": "Low Risk"
    },
    {
        "username": "user2",
        "image_filename": "evidence_image_3.png",
        "temperature": 35.7,
        "humidity": 75.1,
        "vibration": 1,  # 1 means "Yes"
        "light_intensity": 300.0,
        "battery_level": 65.0,
        "latitude": 51.5074,
        "longitude": -0.1278,
        "risk_prediction": "High Risk"
    }
]

# Insert evidence records into MongoDB
evidence_collection.insert_many(sample_evidences)
print("inserted")