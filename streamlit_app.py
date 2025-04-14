import streamlit as st
import pandas as pd
import requests
import plotly.express as px

API_BASE = "https://diabetes-prediction-ilzx.onrender.com"

st.set_page_config(page_title="Diabetes Prediction", layout="wide")
st.title("🩺 Diabetes Prediction Dashboard")

# --- RELOAD SECTION ---
with st.expander("📦 Reload Kaggle Diabetes Dataset"):
    if st.button("🔄 Reload Dataset"):
        with st.spinner("Reloading data and training model..."):
            response = requests.post(f"{API_BASE}/reload")
            if response.status_code == 200:
                st.success("✅ Dataset reloaded and model trained.")
                st.json(response.json())
            else:
                st.error("❌ Failed to reload data.")
                st.text(response.text)

st.markdown("---")

# --- PREDICTION FORM ---
st.header("📋 Patient Data Input")

with st.form("prediction_form"):
    col1, col2 = st.columns(2)

    with col1:
        Pregnancies = st.number_input("Pregnancies", 0, 20, 1)
        Glucose = st.number_input("Glucose", 0, 300, 120)
        BloodPressure = st.number_input("Blood Pressure", 0, 200, 70)
        SkinThickness = st.number_input("Skin Thickness", 0, 100, 20)

    with col2:
        Insulin = st.number_input("Insulin", 0, 900, 85)
        BMI = st.number_input("BMI", 0.0, 100.0, 28.0)
        DiabetesPedigreeFunction = st.number_input("Diabetes Pedigree Function", 0.0, 3.0, 0.5)
        Age = st.number_input("Age", 0, 120, 33)

    submit = st.form_submit_button("🧠 Predict")

    if submit:
        payload = {
            "Pregnancies": Pregnancies,
            "Glucose": Glucose,
            "BloodPressure": BloodPressure,
            "SkinThickness": SkinThickness,
            "Insulin": Insulin,
            "BMI": BMI,
            "DiabetesPedigreeFunction": DiabetesPedigreeFunction,
            "Age": Age
        }

        with st.spinner("Predicting..."):
            response = requests.post(f"{API_BASE}/predict", json=payload)
            if response.status_code == 200:
                result = response.json()
                prediction = result.get("diabetes")
                if prediction == 1:
                    st.error("⚠️ High risk of diabetes (Prediction: 1)")
                else:
                    st.success("✅ Low risk of diabetes (Prediction: 0)")
            else:
                st.error("Prediction failed.")
                st.text(response.text)

# --- DATA VISUALIZATION ---
st.markdown("---")
st.header("📊 Dataset Visualizations")

if st.button("📥 Load Data for Visualization"):
    with st.spinner("Loading..."):
        data_response = requests.get(f"{API_BASE}/data")
        if data_response.status_code == 200:
            df = pd.DataFrame(data_response.json())
            df["OutcomeLabel"] = df["Outcome"].map({0: "No Diabetes", 1: "Diabetes"})

            st.subheader("🧾 Raw Data Sample")
            st.dataframe(df.head())

            # Glucose vs Age Scatter Plot
            st.subheader("📈 Glucose vs Age by Outcome")
            fig = px.scatter(
                df,
                x="Age",
                y="Glucose",
                color="OutcomeLabel",
                title="Glucose vs Age by Diabetes Outcome",
                labels={"OutcomeLabel": "Outcome"},
                hover_data=["BMI", "Insulin", "BloodPressure"]
            )
            st.plotly_chart(fig, use_container_width=True)

            # BMI Distribution
            st.subheader("📉 BMI Distribution by Outcome")
            fig2 = px.histogram(
                df,
                x="BMI",
                color="OutcomeLabel",
                nbins=30,
                barmode="overlay",
                opacity=0.7,
                title="BMI Histogram"
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.error("❌ Could not fetch data.")
