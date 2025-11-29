import streamlit as st
from model_engine import ModelEngine
from views.student_view import render_student_view
from views.teacher_view import render_teacher_view
from views.parent_view import render_parent_view

# Page Config
st.set_page_config(page_title="Student Performance Predictor", page_icon="🎓", layout="wide")

# Load CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize Engine
@st.cache_resource
def load_engine():
    engine = ModelEngine()
    engine.load_models()
    return engine

try:
    engine = load_engine()
except:
    st.error("Models not found! Please run training first.")
    st.stop()

# Sidebar Navigation
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/4762/4762311.png", width=100)
st.sidebar.title("Navigation")

# Language Selector
lang_options = {
    "English": "en",
    "Hindi (हिंदी)": "hi",
    "Tamil (தமிழ்)": "ta",
    "Telugu (తెలుగు)": "te",
    "Kannada (ಕನ್ನಡ)": "kn",
    "Malayalam (മലയാളം)": "ml"
}
selected_lang_name = st.sidebar.selectbox("Language / भाषा / மொழி", list(lang_options.keys()))
lang_code = lang_options[selected_lang_name]

# File Uploader
st.sidebar.markdown("---")
uploaded_file = st.sidebar.file_uploader("📂 Upload Student Data (CSV)", type=["csv"])

import pandas as pd
import database as db

# Initialize DB
db.init_db()

if uploaded_file is not None:
    try:
        # Try reading with comma first, then semicolon
        try:
            df = pd.read_csv(uploaded_file)
            if len(df.columns) < 5: # Likely wrong delimiter
                uploaded_file.seek(0)
                df = pd.read_csv(uploaded_file, sep=';')
        except:
            uploaded_file.seek(0)
            df = pd.read_csv(uploaded_file, sep=';')
            
        st.sidebar.success(f"Loaded {len(df)} students from file!")
        
        # Check if we can retrain (needs G3)
        if 'G3' in df.columns:
            if st.sidebar.button("🔄 Retrain Model"):
                with st.spinner("Retraining..."):
                    engine.train(df=df)
                    st.success("Model Retrained on your data!")
        
        # Process and Save to DB
        if st.sidebar.button("💾 Save to Database"):
            with st.spinner("Processing & Saving..."):
                # Run predictions first to populate risk/score
                results = engine.predict_batch(df)
                
                # Rename columns to match DB schema if needed
                # DB expects: predicted_score, risk_level (int)
                results['predicted_score'] = results['Predicted Score']
                results['risk_level'] = results['Risk Val']
                
                # Drop UI columns not in DB
                cols_to_keep = ["G1", "G2", "G3", "studytime", "failures", "absences", "health", "freetime", "goout", "risk_level", "predicted_score"]
                # Add name if missing
                if "name" not in results.columns:
                    results["name"] = [f"Student {i}" for i in range(len(results))]
                    cols_to_keep.append("name")
                
                # Filter columns
                db_df = results[[c for c in cols_to_keep if c in results.columns]]
                
                db.bulk_insert(db_df)
                st.sidebar.success("Data saved to Database!")
                
    except Exception as e:
        st.sidebar.error(f"Error: {e}")

# Load data from DB for global use
student_data = db.get_all_students()
if not student_data.empty:
    st.session_state['student_data_db'] = student_data
    st.sidebar.info(f"📚 Database: {len(student_data)} students")
else:
    st.sidebar.warning("Database is empty. Upload CSV or Add Student.")

role = st.sidebar.radio("Select Role", ["Student", "Teacher", "Parent"])

if role == "Student":
    render_student_view(engine, lang=lang_code)
elif role == "Teacher":
    render_teacher_view(engine, lang=lang_code)
elif role == "Parent":
    render_parent_view(engine, lang=lang_code)

st.sidebar.markdown("---")
st.sidebar.caption("v1.1 | Student Performance Predictor")

# Add helpful links in sidebar
with st.sidebar.expander("ℹ️ About"):
    st.markdown("""
    **Student Performance Predictor** uses machine learning to help educators and parents identify at-risk students and provide personalized recommendations.

    **Features:**
    - Real-time performance prediction
    - Risk assessment and alerts
    - Multi-language support
    - CSV data import/export
    - Personalized recommendations

    **Powered by:** XGBoost ML models trained on educational data.
    """)
