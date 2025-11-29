import pandas as pd
import numpy as np

def load_data():
    students = pd.read_csv("students.csv")
    logs = pd.read_csv("daily_logs.csv")
    scores = pd.read_csv("scores.csv")
    return students, logs, scores

def compute_features(students, logs, scores):
    # Convert dates
    logs['date'] = pd.to_datetime(logs['date'])
    scores['date'] = pd.to_datetime(scores['date'])
    
    feature_rows = []
    
    # We want to create a training dataset. 
    # For each score (target), we compute features based on data available BEFORE that score.
    
    for _, score_row in scores.iterrows():
        student_id = score_row['student_id']
        exam_date = score_row['date']
        
        # Filter logs prior to exam
        prior_logs = logs[(logs['student_id'] == student_id) & (logs['date'] < exam_date)]
        
        if prior_logs.empty:
            continue
            
        # 1. Rolling Averages (7, 14, 30 days)
        last_7d = prior_logs[prior_logs['date'] >= exam_date - pd.Timedelta(days=7)]
        last_30d = prior_logs[prior_logs['date'] >= exam_date - pd.Timedelta(days=30)]
        
        avg_study_7d = last_7d['study_hours'].mean() if not last_7d.empty else 0
        avg_study_30d = last_30d['study_hours'].mean() if not last_30d.empty else 0
        
        attendance_rate_30d = last_30d['attendance'].mean() if not last_30d.empty else 0
        
        # 2. Trends
        # Slope of study hours in last 14 days
        last_14d = prior_logs[prior_logs['date'] >= exam_date - pd.Timedelta(days=14)]
        if len(last_14d) > 1:
            # Simple linear regression for slope
            y = last_14d['study_hours'].values
            x = np.arange(len(y))
            slope = np.polyfit(x, y, 1)[0]
        else:
            slope = 0
            
        # 3. Interactions
        study_attendance_interaction = avg_study_30d * attendance_rate_30d
        
        # 4. Static features
        student_info = students[students['student_id'] == student_id].iloc[0]
        
        feature_rows.append({
            "student_id": student_id,
            "exam_date": exam_date,
            "subject": score_row['subject'],
            "grade_level": student_info['grade_level'],
            "avg_study_7d": avg_study_7d,
            "avg_study_30d": avg_study_30d,
            "attendance_rate_30d": attendance_rate_30d,
            "study_trend_14d": slope,
            "study_attendance_interaction": study_attendance_interaction,
            "prev_score": 0, # Placeholder, could be improved with lag features
            "target_score": score_row['score']
        })
        
    return pd.DataFrame(feature_rows)

if __name__ == "__main__":
    print("Computing features...")
    students, logs, scores = load_data()
    features_df = compute_features(students, logs, scores)
    features_df.to_csv("features.csv", index=False)
    print(f"Features computed: {len(features_df)} rows.")
