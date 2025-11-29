import streamlit as st
from recommendations import get_recommendations
from translations import TRANSLATIONS

def render_parent_view(engine, lang="en"):
    t = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    
    st.markdown(f"<h1 style='text-align: center; animation: fadeIn 1s;'>{t['title_parent']}</h1>", unsafe_allow_html=True)
    
    # Check for uploaded data
    if 'student_data_db' not in st.session_state or st.session_state['student_data_db'].empty:
        st.warning(t["no_data_parent"]) # Ensure this key exists or use generic text
        st.info("Please ask a teacher to add student records or upload data.")
        return

    df = st.session_state['student_data_db']
    # Create label with ID and Name
    df['label'] = df['student_id'].astype(str) + " - " + df['name']
    
    s_label = st.sidebar.selectbox("Select Child", df['label'].tolist())
    selected_student = df[df['label'] == s_label].iloc[0]
    student_name = selected_student['name']
    
    # Inputs from DB
    inputs = {
        "G1": int(selected_student.get("G1", 0)),
        "G2": int(selected_student.get("G2", 0)),
        "studytime": int(selected_student.get("studytime", 0)),
        "failures": int(selected_student.get("failures", 0)),
        "absences": int(selected_student.get("absences", 0)),
        "health": int(selected_student.get("health", 0)),
        "freetime": int(selected_student.get("freetime", 0)),
        "goout": int(selected_student.get("goout", 0))
    }
    
    st.info(f"{t['viewing_data']} **{student_name}**")
    
    # Predict
    result = engine.predict_realtime(inputs)
    
    # Translate risk
    risk_key = "risk_low"
    if result['risk_level'] == 1: risk_key = "risk_medium"
    if result['risk_level'] == 2: risk_key = "risk_high"
    risk_text = t[risk_key]
    
    # Simple Cards
    col1, col2 = st.columns(2)
    with col1:
        st.metric(t["predicted_score"], f"{result['predicted_score']}/20", "Stable")
    with col2:
        st.metric(t["absences"], "12", "+2 this week")
        
    # Risk Badge
    st.markdown(f"### {t['current_status']} **{risk_text}**")
    
    # Recommendations
    st.markdown(f"### {t['how_to_help']}")
    recs = get_recommendations(result, role="parent", lang=lang)
    for rec in recs:
        st.warning(rec)
        
    # Trend Graph (Mock) - ensure no negative values on axis
    st.markdown(f"### {t['perf_trend']}")
    predicted_score = max(0, result['predicted_score'])  # Ensure non-negative
    trend_data = [8, 9, 11, 10, 9, predicted_score]  # All positive values

    # Use plotly for better control over axis
    import plotly.graph_objects as go
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Current'],
        y=trend_data,
        mode='lines+markers',
        name='Performance',
        line=dict(color='#4a4ae2', width=3),
        marker=dict(size=8, color='#4a4ae2')
    ))

    # Set y-axis to start from 0 (no negative values)
    fig.update_layout(
        yaxis=dict(range=[0, max(trend_data) + 2]),  # Start from 0, add padding
        xaxis_title="Time Period",
        yaxis_title="Performance Score",
        showlegend=False,
        height=300
    )

    st.plotly_chart(fig, use_container_width=True)
