# Import all necessary libraries
import pandas as pd
import numpy as np
import joblib
import pickle
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

# Input section
with st.form(key="predict_form"):
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

# Footer note
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 0.9em;'>Built with ❤️ using Streamlit</p>", unsafe_allow_html=True)
# Import all necessary libraries
import pandas as pd
import numpy as np
import joblib
import pickle
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

# Input section
with st.form(key="predict_form"):
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

# Footer note
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 0.9em;'>Built with ❤️ using Streamlit</p>", unsafe_allow_html=True)
