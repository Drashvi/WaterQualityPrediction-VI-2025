# Import all necessary libraries
import pandas as pd
import numpy as np
import joblib
import streamlit as st
from sklearn.ensemble import RandomForestClassifier

# Load pollutant prediction model and structure
model = joblib.load("pollution_model.pkl")
model_cols = joblib.load("model_columns.pkl")

# Set page config
st.set_page_config(page_title="💧 Water Quality App", layout="centered")

# ---------------------- CSS for Dark Theme ----------------------
st.markdown("""
    <style>
    /* Global dark background */
    body, .stApp {
        background-color: #0d1117;
        color: #f0f6fc;
    }

    /* Headings */
    h1, h2, h3 {
        color: #58a6ff !important;
        font-family: 'Segoe UI', sans-serif;
        text-align: center;
    }

    /* Success message box */
    .stSuccess {
        background-color: #122f1e !important;
        color: #7ee787 !important;
        border-left: 5px solid #238636 !important;
    }

    /* Error message box */
    .stError {
        background-color: #2d0f12 !important;
        color: #ff7b72 !important;
        border-left: 5px solid #da3633 !important;
    }

    /* Warning message */
    .stWarning {
        background-color: #3a2f00 !important;
        color: #f2cc60 !important;
        border-left: 5px solid #9e6a03 !important;
    }

    /* Table styling */
    table {
        background-color: #161b22 !important;
        color: #c9d1d9 !important;
        border-radius: 8px;
        border: 1px solid #30363d !important;
    }
    th {
        background-color: #21262d !important;
        color: #f0f6fc !important;
    }
    td {
        background-color: #0d1117 !important;
    }

    /* Tabs styling */
    .stTabs [role="tablist"] {
        background-color: #161b22;
        border-radius: 10px;
        padding: 5px;
    }
    .stTabs [role="tab"] {
        color: #c9d1d9;
        border-radius: 8px;
        padding: 8px 12px;
    }
    .stTabs [role="tab"][aria-selected="true"] {
        background-color: #238636;
        color: white;
        font-weight: bold;
    }

    /* Input fields */
    .stNumberInput, .stTextInput {
        background-color: #161b22 !important;
        color: #f0f6fc !important;
        border-radius: 5px;
    }

    /* Footer */
    footer, .stMarkdown p {
        color: #8b949e !important;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)


# ---------------------- Functions for Safety Checks ----------------------
def check_drinkable_issues(p):
    issues = []
    if p[3] < 6: issues.append("O₂ below 6 mg/L")
    if p[0] >= 0.5: issues.append("NH₄ too high")
    if p[1] >= 3: issues.append("BSK5 too high")
    if p[4] >= 50: issues.append("NO₃ too high")
    if p[5] >= 1: issues.append("NO₂ too high")
    return issues

def check_usable_issues(p):
    issues = []
    if p[3] < 4: issues.append("O₂ below 4 mg/L")
    if p[0] >= 1: issues.append("NH₄ too high")
    if p[4] >= 100: issues.append("NO₃ too high")
    if p[5] >= 2: issues.append("NO₂ too high")
    return issues

# ---------------------- UI ----------------------
st.markdown("<h1 style='text-align: center; color: #2e8b57;'>💧 Water Quality Predictor</h1>", unsafe_allow_html=True)

# Tabs for both functionalities
tab1, tab2 = st.tabs(["🔍 Predict Pollutants", "🧪 Manual Usability Check"])

# ---------------------- TAB 1: Pollutants Predictor ----------------------
with tab1:
    st.markdown("### 🌍 Predict key water pollutants based on Year and Station ID")
    st.markdown("---")

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
            input_df = pd.DataFrame({'year': [year_input], 'id': [station_id]})
            input_encoded = pd.get_dummies(input_df, columns=['id'])

            for col in model_cols:
                if col not in input_encoded.columns:
                    input_encoded[col] = 0
            input_encoded = input_encoded[model_cols]

            predicted_pollutants = model.predict(input_encoded)[0]
            pollutants = ['NH4', 'BSK5', 'Suspended', 'O2', 'NO3', 'NO2', 'SO4', 'PO4', 'CL']

            st.success(f"✅ Prediction complete for Station ID **'{station_id}'** in year **{year_input}**.")

            with st.expander("📊 View Predicted Pollutant Levels"):
                result_df = pd.DataFrame({
                    "Pollutant": pollutants,
                    "Level": [f"{val:.2f}" for val in predicted_pollutants]
                })
                st.table(result_df)

            # Safety assessment
            st.markdown("### 🧪 Water Safety Assessment")

            drinkable_issues = check_drinkable_issues(predicted_pollutants)
            if not drinkable_issues:
                st.success("💧 Safe to DRINK")
            else:
                st.error("⚠️ NOT safe to drink")
                st.write("🚫 Problem with:", ", ".join(drinkable_issues))

            usable_issues = check_usable_issues(predicted_pollutants)
            if not usable_issues:
                st.success("🚿 Safe to USE for washing/irrigation")
            else:
                st.error("⚠️ NOT safe to use")
                st.write("🚫 Problem with:", ", ".join(usable_issues))

# ---------------------- TAB 2: Manual Usability Checker ----------------------
with tab2:
    st.markdown("### 🧪 Check if water is usable/drinkable based on pollutant levels")
    st.markdown("---")

    with st.form("usability_form"):
        nh4 = st.number_input("Ammonium (NH₄) level (mg/L)", min_value=0.0, value=0.4)
        bsk5 = st.number_input("BSK5 (mg/L)", min_value=0.0, value=2.5)
        suspended = st.number_input("Suspended Solids (mg/L)", min_value=0.0, value=10.0)
        o2 = st.number_input("Oxygen (O₂) level (mg/L)", min_value=0.0, value=5.0)
        no3 = st.number_input("Nitrate (NO₃) level (mg/L)", min_value=0.0, value=10.0)
        no2 = st.number_input("Nitrite (NO₂) level (mg/L)", min_value=0.0, value=0.5)
        so4 = st.number_input("Sulfate (SO₄) level (mg/L)", min_value=0.0, value=100.0)
        po4 = st.number_input("Phosphate (PO₄) level (mg/L)", min_value=0.0, value=1.0)
        cl = st.number_input("Chloride (Cl⁻) level (mg/L)", min_value=0.0, value=120.0)

        usability_submit = st.form_submit_button("Check Usability")

    if usability_submit:
        manual_pollutants = [nh4, bsk5, suspended, o2, no3, no2, so4, po4, cl]

        st.markdown("### 🧪 Water Safety Assessment")

        drinkable_issues = check_drinkable_issues(manual_pollutants)
        if not drinkable_issues:
            st.success("💧 Safe to DRINK")
        else:
            st.error("⚠️ NOT safe to drink")
            st.write("🚫 Problem with:", ", ".join(drinkable_issues))

        usable_issues = check_usable_issues(manual_pollutants)
        if not usable_issues:
            st.success("🚿 Safe to USE for washing/irrigation")
        else:
            st.error("⚠️ NOT safe to use")
            st.write("🚫 Problem with:", ", ".join(usable_issues))

# ---------------------- Footer ----------------------
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 0.9em;'>Built with ❤️ using Streamlit</p>", unsafe_allow_html=True)
