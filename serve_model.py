from flask import Flask, request, jsonify
import joblib
import pandas as pd
import numpy as np

app = Flask(__name__)

# Load models
fraud_model = joblib.load(r"notebooks/fraud_model.pkl")
credit_model = joblib.load(r"notebooks/credit_model.pkl")

# Load data
fraud_data = pd.read_csv(r"notebooks/Enhanced_Fraud_Data.csv")
credit_data = pd.read_csv(r"data/creditcard.csv")

# Helper function to calculate fraud summary
def calculate_summary(data, fraud_column):
    try:
        total_transactions = len(data)
        fraud_cases = data[data[fraud_column] == 1].shape[0]
        fraud_percentage = (fraud_cases / total_transactions) * 100 if total_transactions > 0 else 0
        return {"total_transactions": total_transactions, "fraud_cases": fraud_cases, "fraud_percentage": fraud_percentage}
    except Exception as e:
        print(f"Error calculating summary: {e}")
        return {"error": "Unable to calculate summary"}

# Total transactions, fraud cases, and fraud percentage for fraud data
@app.route('/fraud_summary', methods=['GET'])
def fraud_summary():
    summary = calculate_summary(fraud_data, 'class')
    return jsonify(summary)

# Total transactions, fraud cases, and fraud percentage for credit card data
@app.route('/credit_summary', methods=['GET'])
def credit_summary():
    summary = calculate_summary(credit_data, 'Class')
    return jsonify(summary)

# Endpoint for fraud trends over time (fraud data by day of week)
@app.route('/fraud_trends', methods=['GET'])
def fraud_trends():
    try:
        fraud_by_date = fraud_data[fraud_data['class'] == 1].groupby('day_of_week').size()
        return jsonify(fraud_by_date.to_dict())
    except Exception as e:
        print(f"Error fetching fraud trends: {e}")
        return jsonify({"error": "Unable to fetch fraud trends"}), 500

# Endpoint for credit card fraud trends over time
@app.route('/credit_trends', methods=['GET'])
def credit_trends():
    try:
        fraud_by_time = credit_data[credit_data['Class'] == 1].groupby('Time').size()
        return jsonify(fraud_by_time.to_dict())
    except Exception as e:
        print(f"Error fetching credit trends: {e}")
        return jsonify({"error": "Unable to fetch credit trends"}), 500

# Device and browser fraud analysis for fraud data
@app.route('/fraud_device_browser', methods=['GET'])
def fraud_device_browser():
    try:
        device_counts = fraud_data[fraud_data['class'] == 1].groupby('device_id').size()
        browser_counts = fraud_data[fraud_data['class'] == 1].groupby('browser').size()
        return jsonify({"device_counts": device_counts.to_dict(), "browser_counts": browser_counts.to_dict()})
    except Exception as e:
        print(f"Error fetching device/browser analysis: {e}")
        return jsonify({"error": "Unable to fetch device/browser analysis"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
