from translations import TRANSLATIONS

def get_recommendations(prediction_result, role="student", lang="en"):
    """
    Generates concise recommendations based on SHAP explanation and risk level.
    Features: G1, G2, studytime, failures, absences, health, freetime, goout
    """
    recs = []
    explanation = prediction_result['explanation']
    risk_level = prediction_result['risk_level']
    t = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    
    # Sort features by negative impact
    negative_impacts = sorted([x for x in explanation if x['impact'] < 0], key=lambda x: x['impact'])
    
    # 1. Address top negative factors
    for item in negative_impacts[:2]: # Top 2 issues
        feature = item['feature']
        val = item['value']
        
        if feature == "absences":
            recs.append(t["rec_attendance"])
        elif feature == "studytime" and val < 3:
            recs.append(t["rec_study"])
        elif feature == "failures" and val > 0:
            recs.append(t["rec_failures"])
        elif feature == "goout" and val > 4:
            recs.append(t["rec_social"])
        elif feature == "health" and val < 3:
            recs.append(t["rec_health"])
        elif feature == "G1" or feature == "G2":
            recs.append(t["rec_scores"])
            
    # 2. Risk-based generic advice
    if risk_level == 2: # High
        if role == "teacher":
            recs.append(t["rec_intervention"])
        elif role == "parent":
            recs.append(t["rec_monitor"])
        else: # Student
            recs.append(t["rec_help"])
    elif risk_level == 0: # Low
        recs.append(t["rec_excellent"])
        
    # Ensure at least one rec
    if not recs:
        recs.append(t["rec_maintain"])
        
    return recs[:3] # Max 3 concise bullets
