# Evidence Management System with Risk Prediction

This project is an **Evidence Management System** with real-time risk prediction using **machine learning** and **deep learning** models. The application is built using **Flask** for the backend, **MongoDB** for data storage, and **Socket.IO** for real-time communication. Additionally, an ensemble of machine learning models (Random Forest, XGBoost, and Gradient Boosting) is used to predict risk based on sensor data.

## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [How to Run](#how-to-run)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Model Training](#model-training)
- [Future Improvements](#future-improvements)
- [Contributing](#contributing)
- [License](#license)

## Features
- **Evidence Type Prediction**: Using a **Convolutional Neural Network (CNN)** to predict the type of evidence based on an uploaded image (fingerprint, gun, or stained cloth).
- **Risk Prediction**: Ensemble of machine learning models (Random Forest, XGBoost, and Gradient Boosting) to predict the risk level based on sensor data such as temperature, humidity, vibration, light intensity, and battery level.
- **Real-time Simulation**: Simulates real-time changes in the sensor data using IoT and updates the risk level based on these changes.
- **Login System**: User authentication with a session-based login system.
- **Dashboard**: Displays all submitted evidence logs and their current risk status in real time using **Socket.IO**.

## Technologies Used
- **Backend**: Flask, Socket.IO
- **Machine Learning**: RandomForest, XGBoost, Gradient Boosting, VotingClassifier (Ensemble Learning)
- **Deep Learning**: Convolutional Neural Network (CNN) for image classification
- **Database**: MongoDB
- **Frontend**: HTML, CSS, JavaScript, jQuery, Bootstrap
- **Other**: Scikit-learn, Pandas, Numpy, PIL, Pickle

## Setup Instructions

### Prerequisites
- Python 3.x
- MongoDB
- Git
- Python packages:
  - `Flask`
  - `pymongo`
  - `scikit-learn`
  - `xgboost`
  - `tensorflow`
  - `pillow`
  - `pandas`
  - `numpy`
  - `flask-socketio`
  - `pickle`
  - `threading`
  - `random`
  - `time`

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/evidence-management-system.git
   cd evidence-management-system
