import streamlit as st
import time
from model_engine import ModelEngine
from recommendations import get_recommendations
import plotly.express as px
from translations import TRANSLATIONS

def render_student_view(engine, lang="en"):
    t = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    
    st.markdown(f"<h1 style='text-align: left; margin-bottom: 30px;'>{t['title_student']}</h1>", unsafe_allow_html=True)
    
    # Sidebar inputs for simulation
    st.sidebar.header(t["simulate"])
    
    # Check for uploaded data
    selected_student = None
    if 'student_data_db' in st.session_state:
        df = st.session_state['student_data_db']
        df['label'] = df['student_id'].astype(str) + " - " + df['name']
        s_label = st.sidebar.selectbox("Select Student", df['label'].tolist())
        selected_student = df[df['label'] == s_label].iloc[0]

    def get_val(col, default):
        if selected_student is not None and col in selected_student:
            return int(selected_student[col])
        return default

    # Real features
    g1 = st.sidebar.slider(t["g1_score"], 0, 20, get_val("G1", 12))
    g2 = st.sidebar.slider(t["g2_score"], 0, 20, get_val("G2", 12))
    studytime = st.sidebar.slider(t["study_time"], 1, 4, get_val("studytime", 2))
    absences = st.sidebar.slider(t["absences"], 0, 93, get_val("absences", 4))
    failures = st.sidebar.slider(t["failures"], 0, 4, get_val("failures", 0))
    health = st.sidebar.slider(t["health"], 1, 5, get_val("health", 3))
    goout = st.sidebar.slider(t["goout"], 1, 5, get_val("goout", 3))
    freetime = st.sidebar.slider(t["freetime"], 1, 5, get_val("freetime", 3))
    
    # Prediction
    inputs = {
        "G1": g1, "G2": g2, "studytime": studytime, "failures": failures,
        "absences": absences, "health": health, "freetime": freetime, "goout": goout
    }
    
    with st.spinner(t["analyzing"]):
        time.sleep(0.3)
        result = engine.predict_realtime(inputs)
    
    # Translate risk
    risk_key = "risk_low"
    if result['risk_level'] == 1: risk_key = "risk_medium"
    if result['risk_level'] == 2: risk_key = "risk_high"
    risk_text = t[risk_key]

    # --- UI LAYOUT ---
    
    # Row 1: Predicted Score (Left) & Action Plan (Right)
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Predicted Score")
        st.metric("Final Grade", f"{result['predicted_score_100']}%")

        # Risk level with color
        risk_color = "🔴" if result['risk_level'] == 2 else "🟡" if result['risk_level'] == 1 else "🟢"
        st.markdown(f"**Risk Level**: {risk_color} {risk_text}")

        # Simple trend indicator
        st.markdown("**Trend**: 📈 Improving")
        
    with col2:
        recs = get_recommendations(result, role="student", lang=lang)
        rec_html = ""

        # Use simple text symbols that are guaranteed to render
        icons = ["📖", "⚡", "🎯"]

        for i, rec in enumerate(recs):
            # Clean the recommendation text - remove bullet points and common emoji prefixes
            clean_rec = rec.replace("• ", "").strip()

            # Remove common emoji prefixes that might cause display issues
            emoji_prefixes = ["🏫 ", "📚 ", "📉 ", "⚖️ ", "🍎 ", "📝 ", "🚨 ", "👨‍👩‍👧 ", "🆘 ", "✅ ", "🌟 "]
            for prefix in emoji_prefixes:
                if clean_rec.startswith(prefix):
                    clean_rec = clean_rec[len(prefix):]

            rec_html += f"""
            <div class="action-item">
                <div class="action-icon">{icons[i%3]}</div>
                <div style="flex: 1;">{clean_rec}</div>
            </div>
            """

        # Display Action Plan as a clean list instead of complex HTML
        st.markdown("### Action Plan")
        for i, rec in enumerate(recs):
            clean_rec = rec.replace("• ", "").strip()
            emoji_prefixes = ["🏫 ", "📚 ", "📉 ", "⚖️ ", "🍎 ", "📝 ", "🚨 ", "👨‍👩‍👧 ", "🆘 ", "✅ ", "🌟 "]
            for prefix in emoji_prefixes:
                if clean_rec.startswith(prefix):
                    clean_rec = clean_rec[len(prefix):]

            icons = ["📖", "⚡", "🎯"]
            st.markdown(f"{icons[i%3]} {clean_rec}")

    # Row 2: Risk Levels (Donut) & Key Factors (Progress)
    col3, col4 = st.columns([1, 1])
    
    with col3:
        # Donut Chart
        risk_val = result['risk_level'] # 0, 1, 2
        # Create a dummy distribution for the donut based on current risk
        values = [10, 10, 10]
        values[risk_val] = 80 # Highlight current risk
        names = [t["risk_low"], t["risk_medium"], t["risk_high"]]
        colors = {'Low Risk': '#4a4ae2', 'Medium Risk': '#ff9f1c', 'High Risk': '#ef233c'}
        # Map translated names to colors
        color_map = {names[0]: '#4a4ae2', names[1]: '#ff9f1c', names[2]: '#ef233c'}
        
        fig = px.pie(values=values, names=names, hole=0.7, color=names, color_discrete_map=color_map)
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            margin=dict(t=0, b=0, l=0, r=0),
            height=200,
            annotations=[dict(text=f"{result['predicted_score_100']}%", x=0.5, y=0.5, font_size=20, showarrow=False, font_color="white")]
        )
        
        st.markdown(f"""<div class="css-card"><h3 style="margin-top: 0;">Risk Analysis</h3>""", unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col4:
        st.markdown("### Key Factors")

        # Study Hours
        study_pct = (studytime / 4) * 100
        st.markdown(f"**Study Hours**: {studytime}h/week")
        st.progress(study_pct / 100)

        # Attendance
        attend_pct = ((93 - absences) / 93) * 100
        st.markdown(f"**Attendance**: {int(attend_pct)}%")
        st.progress(attend_pct / 100)

        # Health
        health_pct = (health / 5) * 100
        st.markdown(f"**Health**: {health}/5")
        st.progress(health_pct / 100)
