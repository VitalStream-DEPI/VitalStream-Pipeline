import os
import streamlit as st
import pandas as pd
import duckdb
import joblib
import plotly.express as px

# ---------------------------------------------------------
# Base Paths (robust to any launch directory)
# ---------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "medstream_warehouse.duckdb")
MODEL_PATH = os.path.join(BASE_DIR, "models", "diabetes_model.pkl")
COLS_PATH = os.path.join(BASE_DIR, "models", "model_columns.pkl")
LOGO_PATH = os.path.join(BASE_DIR, "docs", "logo.png")

# ---------------------------------------------------------
# Page Setup
# ---------------------------------------------------------
st.set_page_config(
    page_title="MedStream | Clinical Analytics",
    page_icon="medical_symbol",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Clean, Human-Centric Medical Style (Light Blue & White)
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    /* Clean Card Container */
    div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"] {
        border-color: #E2E8F0;
        background-color: #FFFFFF;
        border-radius: 10px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
    }

    /* Primary button styling */
    .stButton > button {
        background-color: #2563EB;
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.65rem 1.4rem;
        font-size: 0.95rem;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        background-color: #1D4ED8;
        color: white;
    }

    /* Small badge */
    .badge-pill {
        background-color: #EFF6FF;
        color: #1D4ED8;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
        border: 1px solid #BFDBFE;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Data & Model Loaders
# ---------------------------------------------------------
@st.cache_data
def load_warehouse():
    con = duckdb.connect(DB_PATH, read_only=True)
    data = con.execute("SELECT * FROM patients_analytics").df()
    con.close()
    return data

@st.cache_resource
def load_pipeline():
    trained_model = joblib.load(MODEL_PATH)
    columns = joblib.load(COLS_PATH)
    return trained_model, columns

df = load_warehouse()
model, feature_cols = load_pipeline()

# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------
with st.sidebar:
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, use_container_width=True)
    else:
        st.title("MedStream")
    
    st.markdown("### Clinical Intelligence")
    st.caption("A decision-support pipeline combining DuckDB analytical storage with a calibrated Random Forest risk model.")
    
    st.divider()
    
    st.markdown("**System Overview**")
    st.markdown("- **Storage:** DuckDB Warehouse (`96,128` records)")
    st.markdown("- **Model:** Random Forest (`97.2%` test accuracy)")
    st.markdown("- **Target:** Type 2 Diabetes Mellitus")
    
    st.divider()
    
    st.markdown("**Project Team**")
    st.caption("Yousef Hosny & Basmala Taha")
    st.caption("DEPI Final Project - 2026")

# ---------------------------------------------------------
# Header Section
# ---------------------------------------------------------
st.markdown("""
<div style="margin-bottom: 1.5rem;">
    <span class="badge-pill">Clinical Decision Support</span>
    <h1 style="margin: 0.35rem 0 0.2rem 0; font-size: 2.1rem; color: #0F172A; font-weight: 700;">
        MedStream Health Platform
    </h1>
    <p style="color: #64748B; font-size: 0.98rem; margin: 0;">
        Interactive patient screening & clinical cohort analytics.
    </p>
</div>
""", unsafe_allow_html=True)

# Main Navigation Tabs
tab_prediction, tab_analytics = st.tabs(["Patient Risk Assessment", "Cohort Analytics"])

# =========================================================
# TAB 1: Patient Risk Assessment
# =========================================================
with tab_prediction:
    st.markdown("##### Patient Intake Information")
    st.caption("Enter clinical parameters to predict patient diabetes risk profile.")
    
    with st.container(border=True):
        col_demo, col_labs = st.columns(2, gap="large")
        
        with col_demo:
            st.markdown("**1. Demographics & Medical History**")
            age = st.slider("Age (years)", min_value=1, max_value=100, value=45)
            gender = st.selectbox("Biological Sex", options=["Female", "Male"])
            smoking = st.selectbox(
                "Smoking History", 
                options=["never", "former", "current", "No Info"],
                format_func=lambda x: {
                    "never": "Never Smoked", 
                    "former": "Former Smoker", 
                    "current": "Current Smoker", 
                    "No Info": "Not Recorded"
                }.get(x, x)
            )
            
            c1, c2 = st.columns(2)
            with c1:
                hypertension = st.selectbox("Hypertension", [0, 1], format_func=lambda x: "Yes" if x else "No")
            with c2:
                heart_disease = st.selectbox("Heart Disease", [0, 1], format_func=lambda x: "Yes" if x else "No")
        
        with col_labs:
            st.markdown("**2. Clinical & Laboratory Measurements**")
            glucose = st.slider(
                "Fasting Blood Glucose (mg/dL)", 
                min_value=60, 
                max_value=300, 
                value=120, 
                help="Reference: <100 mg/dL Normal, 100-125 Prediabetes, ≥126 Diabetes"
            )
            hba1c = st.slider(
                "Glycated Hemoglobin (HbA1c %)", 
                min_value=3.5, 
                max_value=10.0, 
                value=5.6, 
                step=0.1, 
                help="Reference: <5.7% Normal, 5.7-6.4% Prediabetes, ≥6.5% Diabetes"
            )
            bmi = st.slider("Body Mass Index (BMI)", min_value=12.0, max_value=55.0, value=26.5, step=0.1)
            
            # Clinical reference guidance
            ref_notes = []
            if glucose >= 126:
                ref_notes.append("• Blood Glucose ≥ 126 mg/dL (Diabetes threshold)")
            elif glucose >= 100:
                ref_notes.append("• Blood Glucose 100-125 mg/dL (Prediabetes range)")
            
            if hba1c >= 6.5:
                ref_notes.append("• HbA1c ≥ 6.5% (Diagnostic threshold)")
            elif hba1c >= 5.7:
                ref_notes.append("• HbA1c 5.7-6.4% (Elevated range)")
                
            if ref_notes:
                st.info("\n".join(ref_notes))
            else:
                st.caption("Lab markers currently fall within standard healthy ranges.")

        st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
        btn_calculate = st.button("Calculate Risk Assessment", use_container_width=True)

    # Prediction Outcome Section
    if btn_calculate:
        patient_record = {
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
        
        pdf = pd.DataFrame([patient_record])
        for c in feature_cols:
            if c not in pdf.columns:
                pdf[c] = 0
        pdf = pdf[feature_cols]
        
        prob_percent = model.predict_proba(pdf)[0][1] * 100
        is_diabetic = model.predict(pdf)[0] == 1
        
        st.markdown("### Assessment Result")
        with st.container(border=True):
            r_col1, r_col2 = st.columns([1, 2], gap="large")
            
            with r_col1:
                st.caption("ESTIMATED RISK PROBABILITY")
                risk_color = "#DC2626" if is_diabetic else "#16A34A"
                st.markdown(f"<h2 style='font-size: 2.8rem; margin: 0; color: {risk_color}; font-weight: 700;'>{prob_percent:.1f}%</h2>", unsafe_allow_html=True)
                
                st.progress(prob_percent / 100.0)
                
                if is_diabetic:
                    st.error("High Risk Indicated")
                else:
                    st.success("Low Risk / Normal")
                    
            with r_col2:
                st.markdown("**Clinical Interpretation & Next Steps**")
                if is_diabetic:
                    st.markdown("""
                    - **Clinical Summary:** The patient exhibits markers highly correlated with Type 2 diabetes risk.
                    - **Primary Drivers:** Elevated blood glucose and HbA1c carry the greatest weight in model prediction.
                    - **Action Plan:** Recommend confirmatory laboratory fasting plasma glucose test, HbA1c re-test, and nutritional counseling.
                    """)
                else:
                    st.markdown("""
                    - **Clinical Summary:** The patient's metabolic profile is consistent with healthy non-diabetic ranges.
                    - **Action Plan:** Encourage routine physical activity, balanced diet, and periodic annual monitoring.
                    """)

# =========================================================
# TAB 2: Cohort Analytics (Warehouse Insights)
# =========================================================
with tab_analytics:
    st.markdown("##### Clinical Warehouse Overview")
    st.caption("Exploratory epidemiological statistics on 96,128 records from DuckDB.")
    
    # Clean 4 KPI Metrics
    total_cohort = len(df)
    diabetic_count = int((df['diabetes'] == 1).sum())
    diabetic_pct = (diabetic_count / total_cohort) * 100
    avg_glucose = df['blood_glucose_level'].mean()
    avg_hba1c = df['HbA1c_level'].mean()
    
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        with st.container(border=True):
            st.caption("TOTAL COHORT")
            st.subheader(f"{total_cohort:,}")
            st.caption("Validated patient records")
    with m2:
        with st.container(border=True):
            st.caption("DIABETES PREVALENCE")
            st.subheader(f"{diabetic_pct:.1f}%")
            st.caption(f"{diabetic_count:,} diagnosed patients")
    with m3:
        with st.container(border=True):
            st.caption("MEAN BLOOD GLUCOSE")
            st.subheader(f"{avg_glucose:.1f} mg/dL")
            st.caption("Cohort baseline avg")
    with m4:
        with st.container(border=True):
            st.caption("MEAN HBA1C")
            st.subheader(f"{avg_hba1c:.2f}%")
            st.caption("Glycemic control indicator")
            
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    
    # 2 High-Value, Clean Visualizations
    chart_col1, chart_col2 = st.columns(2, gap="large")
    
    chart_theme = {
        'paper_bgcolor': '#FFFFFF',
        'plot_bgcolor': '#FFFFFF',
        'font': {'family': 'Plus Jakarta Sans, sans-serif', 'color': '#334155'},
        'margin': {'l': 30, 'r': 20, 't': 40, 'b': 30}
    }
    
    with chart_col1:
        with st.container(border=True):
            st.markdown("**Biomarker Comparison by Diagnosis**")
            st.caption("Average Fasting Blood Glucose (mg/dL) for each cohort")
            
            comp_df = df.groupby('diabetes')[['blood_glucose_level', 'HbA1c_level']].mean().reset_index()
            comp_df['Status'] = comp_df['diabetes'].map({0: 'Non-Diabetic', 1: 'Diabetic'})
            
            fig_bar = px.bar(
                comp_df,
                x='Status',
                y='blood_glucose_level',
                color='Status',
                color_discrete_map={'Non-Diabetic': '#93C5FD', 'Diabetic': '#2563EB'},
                text_auto='.1f',
                labels={'blood_glucose_level': 'Mean Glucose (mg/dL)'}
            )
            fig_bar.update_layout(**chart_theme, showlegend=False, height=270)
            fig_bar.update_yaxes(gridcolor='#F1F5F9')
            st.plotly_chart(fig_bar, use_container_width=True)
            
    with chart_col2:
        with st.container(border=True):
            st.markdown("**Age Distribution Across Cohorts**")
            st.caption("Patient age distribution across diagnosis groups")
            
            fig_box = px.box(
                df,
                x='diabetes',
                y='age',
                color='diabetes',
                color_discrete_map={0: '#93C5FD', 1: '#2563EB'},
                labels={'diabetes': 'Diagnosis', 'age': 'Patient Age'},
                category_orders={'diabetes': [0, 1]}
            )
            fig_box.update_layout(**chart_theme, showlegend=False, height=270)
            fig_box.update_xaxes(tickvals=[0, 1], ticktext=['Non-Diabetic', 'Diabetic'])
            fig_box.update_yaxes(gridcolor='#F1F5F9')
            st.plotly_chart(fig_box, use_container_width=True)
            
    # Stratified Summary Table
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("**Stratified Cohort Summary**")
        st.caption("Aggregated demographics and clinical variables by cohort group.")
        
        cohort_table = df.groupby('diabetes').agg(
            Patients=('age', 'count'),
            Mean_Age=('age', 'mean'),
            Mean_BMI=('bmi', 'mean'),
            Mean_Glucose=('blood_glucose_level', 'mean'),
            Mean_HbA1c=('HbA1c_level', 'mean')
        ).reset_index()
        
        cohort_table['Cohort'] = cohort_table['diabetes'].map({0: 'Non-Diabetic Patients', 1: 'Diabetic Patients'})
        cohort_table = cohort_table[['Cohort', 'Patients', 'Mean_Age', 'Mean_BMI', 'Mean_Glucose', 'Mean_HbA1c']].round(2)
        
        st.dataframe(
            cohort_table,
            use_container_width=True,
            hide_index=True
        )
