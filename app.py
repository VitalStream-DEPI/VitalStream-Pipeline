import streamlit as st
import pandas as pd
import duckdb
import joblib

# page configuration
st.set_page_config(page_title="MedStream Dashboard", page_icon="🩺", layout="wide")

st.title("🩺 MedStream - Clinical Diabetes Dashboard & AI Predictor")
st.markdown("An interactive clinical tool connecting our **Data Warehouse (DuckDB)** with a **Random Forest ML Model (97.2% Accuracy)**.")

# load warehouse metrics
@st.cache_data
def get_warehouse_metrics():
    con = duckdb.connect("medstream_warehouse.duckdb", read_only=True)
    df = con.execute("SELECT * FROM patients_analytics").df()
    con.close()
    return df

df = get_warehouse_metrics()
model = joblib.load("models/diabetes_model.pkl")
feature_cols = joblib.load("models/model_columns.pkl")

# tabs: 1. Predictor, 2. Warehouse Analytics
tab_pred, tab_analytics = st.tabs(["🔮 Patient Risk Predictor", "📊 Warehouse Analytics"])

with tab_pred:
    st.subheader("Patient Clinical Assessment")
    st.write("Enter patient measurements below to calculate diabetes risk in real time:")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.slider("Age (years)", 1, 100, 45)
        gender = st.selectbox("Gender", ["Female", "Male"])
        smoking = st.selectbox("Smoking History", ["never", "former", "current", "No Info"])
    with col2:
        glucose = st.slider("Blood Glucose Level (mg/dL)", 60, 300, 130)
        hba1c = st.slider("HbA1c Level", 3.5, 10.0, 5.8, step=0.1)
        bmi = st.slider("BMI", 12.0, 60.0, 27.5, step=0.1)
    with col3:
        hypertension = st.selectbox("Hypertension (High BP)", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
        heart_disease = st.selectbox("Heart Disease History", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
        st.write("")
        st.write("")
        predict_btn = st.button("🔍 Assess Diabetes Risk", type="primary", use_container_width=True)

    if predict_btn:
        # build input record
        patient = {
            'age': age,
            'hypertension': hypertension,
            'heart_disease': heart_disease,
            'bmi': bmi,
            'HbA1c_level': hba1c,
            'blood_glucose_level': glucose,
            'gender_code': 1 if gender == "Male" else 0,
            'gender_Male': 1 if gender == "Male" else 0,
            'smoking_history_former': 1 if smoking == "former" else 0,
            'smoking_history_never': 1 if smoking == "never" else 0,
            'smoking_history_No Info': 1 if smoking == "No Info" else 0
        }
        
        patient_df = pd.DataFrame([patient])
        for c in feature_cols:
            if c not in patient_df.columns:
                patient_df[c] = 0
        patient_df = patient_df[feature_cols]
        
        prob = model.predict_proba(patient_df)[0][1] * 100
        pred = model.predict(patient_df)[0]
        
        st.divider()
        if pred == 1:
            st.error(f"### ⚠️ High Risk Detected: **{prob:.1f}% Probability**")
            st.write("Clinical indicators suggest elevated diabetes likelihood. Diagnostic confirmation and lifestyle intervention recommended.")
        else:
            st.success(f"### ✅ Low Risk / Normal: **{prob:.1f}% Probability**")
            st.write("Patient parameters fall within expected non-diabetic reference ranges.")

with tab_analytics:
    st.subheader("Data Warehouse Summary (96,128 Patient Records)")
    
    # KPIs
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    total_records = len(df)
    diabetic_count = int((df['diabetes'] == 1).sum())
    kpi1.metric("Total Cohort", f"{total_records:,}")
    kpi2.metric("Diagnosed Patients", f"{diabetic_count:,}", f"{(diabetic_count/total_records)*100:.1f}%")
    kpi3.metric("Avg Blood Glucose", f"{df['blood_glucose_level'].mean():.1f} mg/dL")
    kpi4.metric("Avg HbA1c", f"{df['HbA1c_level'].mean():.2f}")
    
    st.divider()
    col_a, col_b = st.columns(2)
    with col_a:
        st.write("#### Age vs. Diabetes Status")
        st.bar_chart(df.groupby('diabetes')['age'].mean())
    with col_b:
        st.write("#### Blood Glucose by Diagnosis")
        st.bar_chart(df.groupby('diabetes')['blood_glucose_level'].mean())
