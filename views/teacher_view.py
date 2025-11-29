import streamlit as st
import pandas as pd
import plotly.express as px
from translations import TRANSLATIONS

def render_teacher_view(engine, lang="en"):
    t = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    
    st.markdown(f"<h1 style='text-align: center; animation: fadeIn 1s;'>{t['title_teacher']}</h1>", unsafe_allow_html=True)
    
    # Mock Class Data using Real Model
    st.subheader(t["class_overview"])
    
    # Real Class Data from DB
    st.subheader(t["class_overview"])
    
    if 'student_data_db' in st.session_state:
        df = st.session_state['student_data_db']
        
        # Translate risk level for display
        def translate_risk(val):
            if val == 2: return t["risk_high"]
            if val == 1: return t["risk_medium"]
            return t["risk_low"]
            
        df['Risk Level Display'] = df['risk_level'].apply(translate_risk)
        
        # Prepare display dataframe
        cols_to_show = ['student_id', 'name', 'predicted_score', 'Risk Level Display', 'risk_level']
        # Add G1/G2 if exist
        if 'G1' in df.columns: cols_to_show.insert(2, 'G1')
        if 'G2' in df.columns: cols_to_show.insert(3, 'G2')
            
        df_final = df[cols_to_show].rename(columns={'Risk Level Display': 'Risk Level', 'predicted_score': 'Predicted Score'})
        
    else:
        st.info("Database is empty. Please add students or upload data.")
        df_final = pd.DataFrame()
    
    if not df_final.empty:
        # Heatmap of Risk
        risk_counts = df_final['Risk Level'].value_counts()
        fig = px.pie(risk_counts, values=risk_counts.values, names=risk_counts.index, 
                     title="Class Risk Distribution", hole=0.4,
                     color_discrete_map={t["risk_high"]: "red", t["risk_medium"]: "orange", t["risk_low"]: "green"})
        st.plotly_chart(fig, use_container_width=True)
        
        # At-Risk List
        st.markdown(f"### {t['at_risk_students']}")
        high_risk = df_final[df_final['risk_level'] == 2]
        if not high_risk.empty:
            st.dataframe(high_risk.style.applymap(lambda x: 'color: red' if x == t['risk_high'] else '', subset=['Risk Level']))
            
            if st.button(t["email_parents"]):
                st.success("Alerts sent to parents!")
        else:
            st.success(t["no_risk"])
    
    # Add New Student Form
    st.markdown("### ➕ Add New Student")
    with st.form("add_student_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Name", "New Student")
            g1 = st.number_input("G1 Score", 0, 20, 10)
            g2 = st.number_input("G2 Score", 0, 20, 10)
            absences = st.number_input("Absences", 0, 93, 0)
        with col2:
            studytime = st.number_input("Study Time (1-4)", 1, 4, 2)
            failures = st.number_input("Failures", 0, 4, 0)
            health = st.number_input("Health (1-5)", 1, 5, 5)
            goout = st.number_input("Go Out (1-5)", 1, 5, 3)
            freetime = st.number_input("Free Time (1-5)", 1, 5, 3)
            
        submitted = st.form_submit_button("Add Student")
        if submitted:
            import database as db
            # Predict first
            inputs = {
                "G1": g1, "G2": g2, "studytime": studytime, "failures": failures,
                "absences": absences, "health": health, "freetime": freetime, "goout": goout
            }
            res = engine.predict_realtime(inputs)
            
            # Save
            data = inputs.copy()
            data["name"] = name
            data["predicted_score"] = res["predicted_score"]
            data["risk_level"] = res["risk_level"]
            
            db.add_student(data)
            st.success(f"Added {name} to database! Refresh to see.")
            st.experimental_rerun()
            
    # Bulk Actions
    st.markdown(f"### {t['quick_actions']}")
    col1, col2 = st.columns(2)
    with col1:
        st.button(t["assign_practice"])
    with col2:
        st.button(t["schedule_review"])
