# Import all necessary libraries
import pandas as pd
import numpy as np
import joblib
import streamlit as st

# Load the model and structure
model = joblib.load("pollution_model.pkl")
model_cols = joblib.load("model_columns.pkl")

# Set page config
st.set_page_config(page_title="💧 Water Pollutants Predictor", layout="centered")

# Header
st.markdown("<h1 style='text-align: center; color: #2e8b57;'>💧 Water Pollutants Predictor</h1>", unsafe_allow_html=True)
st.markdown("### 🌍 Predict key water pollutants based on Year and Station ID")

# Add a separator line
st.markdown("---")

# Tabs for prediction details and safety classification
tab1, tab2 = st.tabs(["📊 Detailed Prediction", "✅ Safety Check"])

with tab1:
    with st.form(key="predict_form_tab1"):
        col1, col2 = st.columns(2)
        with col1:
            year_input = st.number_input("📅 Select Year", min_value=2000, max_value=2100, value=2022, step=1)
        with col2:
            station_id = st.text_input("🏷️ Enter Station ID", value='1')

        submitted = st.form_submit_button("🔍 Predict")

    if submitted:
        if not station_id:
            st.warning("⚠️ Please enter a valid Station ID.")
        else:
            # Prepare input
            input_df = pd.DataFrame({'year': [year_input], 'id': [station_id]})
            input_encoded = pd.get_dummies(input_df, columns=['id'])

            # Align columns
            for col in model_cols:
                if col not in input_encoded.columns:
                    input_encoded[col] = 0
            input_encoded = input_encoded[model_cols]

            # Make prediction
            predicted_pollutants = model.predict(input_encoded)[0]
            pollutants = ['NH4', 'BSK5', 'Suspended', 'O2', 'NO3', 'NO2', 'SO4', 'PO4', 'CL']

            st.success(f"✅ Prediction complete for Station ID **'{station_id}'** in year **{year_input}**.")

            # Display results in a table
            with st.expander("📊 View Predicted Pollutant Levels"):
                result_df = pd.DataFrame({
                    "Pollutant": pollutants,
                    "Level": [f"{val:.2f}" for val in predicted_pollutants]
                })
                st.table(result_df)

with tab2:
    with st.form(key="predict_form_tab2"):
        col1, col2 = st.columns(2)
        with col1:
            year_input2 = st.number_input("📅 Select Year (Safety Check)", min_value=2000, max_value=2100, value=2022, step=1)
        with col2:
            station_id2 = st.text_input("🏷️ Enter Station ID (Safety Check)", value='1')

        submitted2 = st.form_submit_button("🔍 Check Safety")

    if submitted2:
        if not station_id2:
            st.warning("⚠️ Please enter a valid Station ID.")
        else:
            # Prepare input
            input_df2 = pd.DataFrame({'year': [year_input2], 'id': [station_id2]})
            input_encoded2 = pd.get_dummies(input_df2, columns=['id'])

            # Align columns
            for col in model_cols:
                if col not in input_encoded2.columns:
                    input_encoded2[col] = 0
            input_encoded2 = input_encoded2[model_cols]

            # Make prediction
            predicted_pollutants2 = model.predict(input_encoded2)[0]
            pollutants = ['NH4', 'BSK5', 'Suspended', 'O2', 'NO3', 'NO2', 'SO4', 'PO4', 'CL']

            # Example threshold values (replace with actual standards)
            safe_thresholds = {
                'NH4': 1.5,
                'BSK5': 5.0,
                'Suspended': 10.0,
                'O2': 5.0,  # minimum
                'NO3': 50.0,
                'NO2': 3.0,
                'SO4': 250.0,
                'PO4': 0.5,
                'CL': 250.0
            }

            # Check safety
            safe = True
            drinkable = True
            for p, value in zip(pollutants, predicted_pollutants2):
                if p == 'O2':
                    if value < safe_thresholds[p]:
                        safe = False
                        drinkable = False
                else:
                    if value > safe_thresholds[p]:
                        safe = False
                        drinkable = False

            # Display results
            if safe:
                st.success("💧 Water is SAFE for general use.")
            else:
                st.error("⚠️ Water is NOT safe for general use.")

            if drinkable:
                st.info("🥤 Water is DRINKABLE.")
            else:
                st.warning("🚫 Water is NOT drinkable.")

# Footer note
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 0.9em;'>Built with ❤️ using Streamlit</p>", unsafe_allow_html=True)
