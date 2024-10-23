from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from pymongo import MongoClient
import pickle
import random
import threading
import time
import pandas as pd
from bson import ObjectId
from flask_socketio import SocketIO, emit
from tensorflow.keras.models import load_model  # type: ignore
from PIL import Image
import numpy as np

app = Flask(__name__)
app.secret_key = b'\xddhO\xc8\x05\xb8<\xa5m1\xa5\x9c\x11O5\xaf\x9e\t\xe8\xcd\x1bWv`'
socketio = SocketIO(app)

# MongoDB connection setup
client = MongoClient('mongodb://localhost:27017/')
db = client['risk_prediction_db']
users_collection = db['users']
evidence_collection = db['evidences']

# Load the pre-trained CNN model for evidence type classification (3 classes)
evidence_type_model = load_model('models/evidence_type_cnn.h5')

# Load the risk prediction model
with open('models/risk_prediction_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Load the scaler used during training for the risk prediction model
with open('models/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

# Default variables based on evidence type (updated with correct classes)
evidence_defaults = {
    'fingerprint': {'Temperature': '28', 'Humidity': '55', 'Vibration': '0', 'Light_Intensity': '250', 'Battery_Level': '85'},
    'gun': {'Temperature': '22', 'Humidity': '40', 'Vibration': '1', 'Light_Intensity': '300', 'Battery_Level': '90'},
    'stained_cloth': {'Temperature': '25', 'Humidity': '50', 'Vibration': '0', 'Light_Intensity': '200', 'Battery_Level': '80'}
}

# Global flag to track simulation state
simulation_running = False

# Login route
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = users_collection.find_one({'username': username, 'password': password})
        if user:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return 'Invalid login credentials'

    return render_template('login.html')

# Route for predicting the evidence type when the image is uploaded
@app.route('/predict_evidence', methods=['POST'])
def predict_evidence():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    if 'evidence_image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    # Handle image upload for CNN prediction
    evidence_image = request.files['evidence_image']
    img = Image.open(evidence_image).resize((64, 64))
    img_array = np.array(img) / 255.0  # Normalize the image
    img_array = img_array.reshape(1, 64, 64, 3)  # Add batch dimension

    # Use the CNN model to predict the evidence type
    prediction = evidence_type_model.predict(img_array)
    predicted_class = np.argmax(prediction[0])  # Get class index

    # Update the classes based on the correct evidence types
    evidence_types = ['fingerprint', 'gun', 'stained_cloth']
    predicted_evidence = evidence_types[predicted_class]

    # Autofill variables based on the predicted evidence type
    variables = evidence_defaults[predicted_evidence]

    # Return predicted evidence type and variables as JSON
    return jsonify({
        'predicted_evidence': predicted_evidence,
        'variables': variables
    })

# Home route for submitting the final evidence and running risk prediction
@app.route('/home', methods=['GET', 'POST'])
def home():
    global simulation_running

    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Get variables from the form
        variables = {
            'Temperature': request.form['temperature'],
            'Humidity': request.form['humidity'],
            'Vibration': request.form['vibration'],
            'Light_Intensity': request.form['light_intensity'],
            'Battery_Level': request.form['battery_level']
        }

        # Run risk prediction using the ensemble model
        features = pd.DataFrame([variables], columns=[
            'Temperature', 'Humidity', 'Vibration', 'Light_Intensity', 'Battery_Level'
        ])
        scaled_features = scaler.transform(features)
        risk_prediction = model.predict(scaled_features)[0]
        risk = 'High Risk' if risk_prediction == 1 else 'Low Risk'

        # Store the evidence and prediction in MongoDB
        evidence_id = str(ObjectId())
        evidence_collection.insert_one({
            '_id': evidence_id,
            'username': session['username'],
            'variables': variables,
            'risk_prediction': risk
        })

        # Start the IoT simulation after the first prediction, if not already running
        if not simulation_running:
            simulation_running = True
            threading.Thread(target=simulate_iot_data, daemon=True).start()

        return redirect(url_for('dashboard'))

    return render_template('home.html')

# Dashboard route to display evidence logs and risk status
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    evidences = list(evidence_collection.find({'username': session['username']}))
    return render_template('dashboard.html', evidences=evidences)

# Simulate IoT Monitoring (Random data changes)
def simulate_iot_data():
    global simulation_running

    while simulation_running:
        time.sleep(10)  # Simulate IoT update every 10 seconds (for testing purposes)

        # Retrieve all evidences from MongoDB
        all_evidences = evidence_collection.find()

        for evidence in all_evidences:
            # Randomly update numerical variables to simulate IoT changes
            updated_values = {
                'Temperature': random.uniform(10, 50),       # Simulate temperature (°C)
                'Humidity': random.uniform(30, 90),          # Simulate humidity (%)
                'Vibration': random.randint(0, 1),           # Simulate vibration (0 or 1)
                'Light_Intensity': random.uniform(100, 1000),# Simulate light intensity (lx)
                'Battery_Level': random.uniform(0, 100),     # Simulate battery level (%)
            }

            # Update evidence with new simulated values in MongoDB
            evidence_collection.update_one(
                {'_id': evidence['_id']},
                {'$set': {'variables': updated_values}}
            )

            # Create features DataFrame with correct column names
            features = pd.DataFrame([updated_values], columns=[
                'Temperature', 'Humidity', 'Vibration', 'Light_Intensity',
                'Battery_Level'
            ])
            scaled_features = scaler.transform(features)

            # Run the risk prediction with updated data
            risk_prediction = model.predict(scaled_features)[0]  # Use DataFrame
            new_risk = 'High Risk' if risk_prediction == 1 else 'Low Risk'

            # If risk status changes, update it
            if new_risk != evidence['risk_prediction']:
                evidence_collection.update_one(
                    {'_id': evidence['_id']},
                    {'$set': {'risk_prediction': new_risk}}
                )

                # Emit real-time risk updates to all connected clients
                socketio.emit('risk_update', {
                    'evidence_id': str(evidence['_id']),
                    'risk': new_risk,
                    'variables': updated_values
                })

# Start the Flask app with SocketIO
if __name__ == '__main__':
    socketio.run(app, debug=True)
