import pandas as pd
import os
import joblib
from flask import Flask, Blueprint, request, jsonify
from flask_cors import CORS
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, classification_report
from sklearn.ensemble import RandomForestClassifier     # ✅ เปลี่ยนเป็น Random Forest
from imblearn.over_sampling import SMOTE

# ==== Flask App ====
bp_soil = Blueprint("soil", __name__)

# ==== Paths ====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # AI folder
file_path = os.path.join(BASE_DIR, 'plant', 'SoilType_dataset.csv')

print("Reading CSV file from:", file_path)

# ==== Read CSV ====
df = pd.read_csv(file_path)

# ==== Clean & Rename Columns ====
df.columns = df.columns.str.strip()  # Remove extra spaces

# Fix missing or wrong column names for Phosphorus
if 'Unnamed: 6' in df.columns:
    df = df.rename(columns={'Unnamed: 6': 'P'})

# If long names are used, rename them
df = df.rename(columns={
    'Nitrogen': 'N',
    'Phosphorus': 'P',
    'Potassium': 'K'
})

print("Detected Columns:", df.columns.tolist())

# ==== Save first row for testing ====
first_row = df.loc[0]
df = df.drop(index=0).reset_index(drop=True)

# ==== Check Required Columns ====
required_cols = ['pH', 'EC', 'N', 'P', 'K']
for col in required_cols:
    if col not in df.columns:
        raise ValueError(f"Missing required column in CSV: {col}")

# ==== Features & Labels ====
X = df[required_cols]
y_label = df['SoilType']

# ==== Encode Labels ====
le = LabelEncoder()
y = le.fit_transform(y_label)

# ==== SMOTE Oversampling ====
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y)

# ==== Train/Test Split ====
X_train, X_test, y_train, y_test = train_test_split(
    X_resampled, y_resampled, test_size=0.2, random_state=42, stratify=y_resampled
)

# ==== Scale Features ====
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ==== Train Random Forest Classifier ====
model = RandomForestClassifier(
    n_estimators=300,        # จำนวนต้นไม้ (default=100) สามารถเพิ่มหรือลดได้
    max_depth=None,          # ปล่อยให้ต้นไม้ลึกตามต้องการ
    random_state=42,
    n_jobs=-1                # ใช้ CPU ทุกคอร์ให้เร็วขึ้น
)
model.fit(X_train_scaled, y_train)

# ==== Evaluate ====
train_acc = accuracy_score(y_train, model.predict(X_train_scaled))
test_acc = accuracy_score(y_test, model.predict(X_test_scaled))

print(f"\n Train Accuracy: {train_acc:.2%}")
print(f" Test Accuracy:  {test_acc:.2%}")
print("\n=== Classification Report ===")
print(classification_report(y_test, model.predict(X_test_scaled), target_names=le.classes_))

# ==== Save Model, Scaler, Encoder ====
joblib.dump(model, 'soiltype_rf_model.pkl')
joblib.dump(scaler, 'soiltype_scaler.pkl')
joblib.dump(le, 'soiltype_label_encoder.pkl')
print("\n ✅ Model, Scaler, and Label Encoder saved as Random Forest version.")

# ==== API Endpoint ====
@bp_soil.route("/wish", methods=["GET", "POST"])
def predict():
    if request.method == "GET":
        return "✅ This endpoint accepts POST requests with sensor data only."
    try:
        data = request.json
        input_df = pd.DataFrame([{
            'pH': data['pH'],
            'EC': data['EC'],
            'N': data['N'],
            'P': data['P'],
            'K': data['K'],
        }])

        # Scale input before prediction
        input_scaled = scaler.transform(input_df)
        prediction = model.predict(input_scaled)
        soil_type = le.inverse_transform(prediction)[0]

        return jsonify({"soil_type": soil_type})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
