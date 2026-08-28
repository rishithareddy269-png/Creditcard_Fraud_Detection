import pandas as pd
import joblib

# Load the trained model
model = joblib.load("fraud_detection_model.pkl")

# Load the scaler
scaler = joblib.load("scaler.pkl")

# Read the dataset
df = pd.read_csv("creditcard.csv")

# Take one transaction from the dataset
transaction = df.drop("Class", axis=1).iloc[[0]]

# Scale the transaction
transaction_scaled = scaler.transform(transaction)

# Make prediction
prediction = model.predict(transaction_scaled)

print("\nPrediction:")

if prediction[0] == 1:
    print("⚠️ FRAUDULENT TRANSACTION")
else:
    print("✅ NORMAL TRANSACTION")