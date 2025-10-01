import pandas as pd
import os
from flask_cors import CORS
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier   
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
from flask import Flask, Blueprint, request, jsonify

bp_plant = Blueprint("crop", __name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # AI folder
file_path = os.path.join(BASE_DIR, 'plant', 'Crop_recommendation.csv')
target_file = "Crop_recommendation.csv"

print("Reading CSV file from:", file_path)

# Read CSV
df = pd.read_csv(file_path)

# Print summary
print(f"\n📁 File: {target_file}")
print(" Columns:")
for col in df.columns:
    print(f"   - {col} ({df[col].dtype})")
print(f" Rows: {len(df)}")

print("🔍 Raw value samples:")
print(df.head(len(df)))
print(df.dtypes)

# Clean numeric features only
numeric_cols = ['nitrogen', 'phosphorus', 'potassium', 'temperature', 'humidity', 'ph', 'rainfall']
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col].astype(str).str.strip(), errors='coerce')

# Check nulls
print("\n❓ Missing values per column:")
print(df[numeric_cols].isnull().sum())

# Drop rows with missing values only in important columns
df = df.dropna(subset=numeric_cols + ['crop_name'])

print(f"✅ Remaining rows after clean-up: {len(df)}")

# Encode target variable
le = LabelEncoder()
df['crop_name'] = le.fit_transform(df['crop_name'])

# ✅ Features (X) and label (y)
X = df[['nitrogen', 'phosphorus', 'potassium', 'temperature', 'humidity', 'ph', 'rainfall']]
y = df['crop_name']

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ✅ Train model with Random Forest
model = RandomForestClassifier(
    n_estimators=200,       
    max_depth=None,         
    random_state=42,
    n_jobs=-1             
)
model.fit(X_train, y_train)

# Test prediction
y_pred = model.predict(X_test)
y_train_pred = model.predict(X_train)

accuracy = accuracy_score(y_test, y_pred)
train_accuracy = accuracy_score(y_train, y_train_pred)

print(f"\n✅ Random Forest trained. Train Accuracy: {train_accuracy:.2%}, Test Accuracy: {accuracy:.2%}")
print(classification_report(y_test, y_pred, target_names=le.classes_))

# Function to predict from new input
@bp_plant.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "GET":
        return "✅ This endpoint accepts POST requests with sensor data only."
    try:
        data = request.json
        input_df = pd.DataFrame([{
            'nitrogen': data['n'],
            'phosphorus': data['p'],
            'potassium': data['k'],
            'temperature': data['temp'],
            'humidity': data['hum'],
            'ph': data['ph_val'],
            'rainfall': data['rain']
        }])
        prediction = model.predict(input_df)
        crop_name = le.inverse_transform(prediction)[0]
        return jsonify({"crop": crop_name})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

