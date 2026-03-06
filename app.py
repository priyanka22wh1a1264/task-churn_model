# Streamlit UI for Customer Churn Prediction

import streamlit as st
import pickle
import pandas as pd

# Load model and files
model = pickle.load(open("model.pkl", "rb"))
model_columns = pickle.load(open("model_columns.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))

# Page configuration
st.set_page_config(
    page_title="Customer Churn Prediction",
    page_icon="churn.png",
    layout="wide"
)

# Sidebar
with st.sidebar:
    st.title("Customer Churn App")
    st.image("churn.png", width=200)
    st.markdown("### Predict if a customer will churn")
    st.info("Enter the customer details and click Predict.")

# Main Title
st.title("📊 Customer Churn Prediction System")

# Layout
col1, col2 = st.columns(2)

# -------------------------
# Customer Information
# -------------------------
with col1:
    st.subheader("Customer Information")

    gender = st.selectbox("Gender", ["Female", "Male"])
    senior = st.selectbox("Senior Citizen", ["No", "Yes"])
    partner = st.selectbox("Partner", ["No", "Yes"])
    dependents = st.selectbox("Dependents", ["No", "Yes"])

    tenure = st.number_input("Tenure (months)", 0, 72)
    monthly_charges = st.number_input("Monthly Charges")
    total_charges = st.number_input("Total Charges")

# -------------------------
# Service Details
# -------------------------
with col2:
    st.subheader("Service Details")

    phone_service = st.selectbox("Phone Service", ["No", "Yes"])
    multiple_lines = st.selectbox("Multiple Lines", ["No phone service", "No", "Yes"])
    internet_service = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])

    contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
    paperless = st.selectbox("Paperless Billing", ["No", "Yes"])

    payment_method = st.selectbox(
        "Payment Method",
        [
            "Electronic check",
            "Mailed check",
            "Bank transfer (automatic)",
            "Credit card (automatic)"
        ]
    )

# Convert Senior Citizen
senior = 1 if senior == "Yes" else 0

# -------------------------
# Create dataframe for prediction
# -------------------------
input_data = pd.DataFrame(columns=model_columns)
input_data.loc[0] = 0

# Numeric values
input_data["SeniorCitizen"] = senior
input_data["tenure"] = tenure
input_data["MonthlyCharges"] = monthly_charges
input_data["TotalCharges"] = total_charges

# Gender
if gender == "Male" and "gender_Male" in input_data.columns:
    input_data["gender_Male"] = 1

# Partner
if partner == "Yes" and "Partner_Yes" in input_data.columns:
    input_data["Partner_Yes"] = 1

# Dependents
if dependents == "Yes" and "Dependents_Yes" in input_data.columns:
    input_data["Dependents_Yes"] = 1

# Phone Service
if phone_service == "Yes" and "PhoneService_Yes" in input_data.columns:
    input_data["PhoneService_Yes"] = 1

# Multiple Lines
if multiple_lines == "Yes" and "MultipleLines_Yes" in input_data.columns:
    input_data["MultipleLines_Yes"] = 1
elif multiple_lines == "No phone service" and "MultipleLines_No phone service" in input_data.columns:
    input_data["MultipleLines_No phone service"] = 1

# Internet Service
if internet_service == "Fiber optic" and "InternetService_Fiber optic" in input_data.columns:
    input_data["InternetService_Fiber optic"] = 1
elif internet_service == "No" and "InternetService_No" in input_data.columns:
    input_data["InternetService_No"] = 1

# Contract
if contract == "One year" and "Contract_One year" in input_data.columns:
    input_data["Contract_One year"] = 1
elif contract == "Two year" and "Contract_Two year" in input_data.columns:
    input_data["Contract_Two year"] = 1

# Paperless Billing
if paperless == "Yes" and "PaperlessBilling_Yes" in input_data.columns:
    input_data["PaperlessBilling_Yes"] = 1

# Payment Method
if payment_method == "Credit card (automatic)" and "PaymentMethod_Credit card (automatic)" in input_data.columns:
    input_data["PaymentMethod_Credit card (automatic)"] = 1
elif payment_method == "Electronic check" and "PaymentMethod_Electronic check" in input_data.columns:
    input_data["PaymentMethod_Electronic check"] = 1
elif payment_method == "Mailed check" and "PaymentMethod_Mailed check" in input_data.columns:
    input_data["PaymentMethod_Mailed check"] = 1

# -------------------------
# Predict Button
# -------------------------
st.markdown("---")

c1, c2, c3, c4, c5 = st.columns(5)

with c3:
    predict_button = st.button("🔍 Predict Churn")

# Prediction
if predict_button:
    scaled_input = scaler.transform(input_data)
    prediction = model.predict(scaled_input)

    if prediction[0] == 1:
        st.error("⚠ Customer is likely to Churn")
    else:
        st.success("✅ Customer is likely to Stay")