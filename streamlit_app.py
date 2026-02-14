import streamlit as st
import requests
import json
from datetime import datetime

API_URL = "http://18.205.34.219:8000/predict"

# ======================================
# API CALL FUNCTION (MOVE THIS TO TOP)
# ======================================
def send_request(payload):

    with st.spinner("Analyzing transaction..."):

        try:
            response = requests.post(API_URL, json=payload, timeout=10)

            if response.status_code == 200:
                result = response.json()

                prediction = result.get("prediction")
                probability = result.get("probability", 0.0)

                try:
                    probability = float(probability)
                except:
                    probability = 0.0

                if prediction == 1:
                    st.markdown(
                        f'<div class="result-box" style="background-color:#ef4444;">🚨 FRAUD DETECTED<br>Confidence: {probability:.2f}</div>',
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f'<div class="result-box" style="background-color:#22c55e;">✅ Legitimate Transaction<br>Confidence: {probability:.2f}</div>',
                        unsafe_allow_html=True
                    )
            else:
                st.error(f"API Error ({response.status_code}): {response.text}")

        except requests.exceptions.Timeout:
            st.error("⏳ Request timed out. Backend may be slow or unreachable.")

        except Exception as e:
            st.error(f"Connection Error: {e}")


# ======================================
# Page Config
# ======================================
st.set_page_config(
    page_title="Fraud Detection System",
    page_icon="💳",
    layout="wide"
)

# ======================================
# Custom Styling
# ======================================
st.markdown("""
<style>
body {
    background-color: #0f172a;
}
.main {
    background-color: #0f172a;
}
.block-container {
    padding-top: 2rem;
}
.stButton>button {
    background: linear-gradient(90deg, #00C6FF, #0072FF);
    color: white;
    border-radius: 12px;
    height: 3em;
    width: 100%;
    font-size: 16px;
}
.result-box {
    padding: 25px;
    border-radius: 15px;
    font-size: 22px;
    text-align: center;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ======================================
# Header
# ======================================
st.title("💳 AI Fraud Detection Dashboard")
st.markdown("#### Real-time Transaction Risk Analysis System")

st.divider()

# ======================================
# Tabs
# ======================================
tab1, tab2 = st.tabs(["📝 Manual Form Input", "📦 Direct JSON Input"])

# ======================================
# TAB 1 - FORM INPUT
# ======================================
with tab1:

    st.subheader("Enter Transaction Details")

    col1, col2 = st.columns(2)

    with col1:
        transaction_id = st.number_input("Transaction ID", value=1)
        amount = st.number_input("Amount", value=55.530334)
        customer_id = st.number_input("Customer ID", value=1952)
        merchant_id = st.number_input("Merchant ID", value=2701)
        transaction_amount = st.number_input("Transaction Amount", value=79.413607)
        anomaly_score = st.number_input("Anomaly Score", value=0.686699)

    with col2:
        category = st.selectbox("Category", ["Food", "Shopping", "Travel", "Other"])
        merchant_name = st.text_input("Merchant Name", "Merchant 2701")
        location = st.text_input("Location", "Location 2701")
        name = st.text_input("Customer Name", "Customer 1952")
        age = st.number_input("Age", value=50)
        address = st.text_input("Address", "Address 1952")
        account_balance = st.number_input("Account Balance", value=2869.689912)

    timestamp = st.text_input("Timestamp (YYYY-MM-DD HH:MM:SS)", "2022-01-01 00:00:00")
    last_login = st.date_input("Last Login", datetime(2024, 8, 9))
    suspicious_flag = st.selectbox("Suspicious Flag (Not used in prediction)", [0, 1])

    if st.button("🔍 Predict from Form"):

        payload = {
            "TransactionID": transaction_id,
            "Amount": amount,
            "CustomerID": customer_id,
            "Timestamp": timestamp,
            "MerchantID": merchant_id,
            "TransactionAmount": transaction_amount,
            "AnomalyScore": anomaly_score,
            "Category": category,
            "MerchantName": merchant_name,
            "Location": location,
            "Name": name,
            "Age": age,
            "Address": address,
            "AccountBalance": account_balance,
            "LastLogin": str(last_login),
            "SuspiciousFlag": suspicious_flag
        }

        send_request(payload)


# ======================================
# TAB 2 - DIRECT JSON INPUT
# ======================================
with tab2:

    st.subheader("Send Raw JSON Payload Directly")

    default_json = {
        "TransactionID": 1,
        "Amount": 55.530334,
        "CustomerID": 1952,
        "Timestamp": "2022-01-01 00:00:00",
        "MerchantID": 2701,
        "TransactionAmount": 79.413607,
        "AnomalyScore": 0.686699,
        "Category": "Other",
        "MerchantName": "Merchant 2701",
        "Location": "Location 2701",
        "Name": "Customer 1952",
        "Age": 50,
        "Address": "Address 1952",
        "AccountBalance": 2869.689912,
        "LastLogin": "2024-08-09",
        "SuspiciousFlag": 0
    }

    json_input = st.text_area(
        "Edit JSON Below:",
        value=json.dumps(default_json, indent=4),
        height=400
    )

    if st.button("🚀 Send JSON Directly"):
        try:
            payload = json.loads(json_input)
            send_request(payload)
        except Exception as e:
            st.error(f"Invalid JSON Format: {e}")
