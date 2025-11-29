import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

def generate_students(n=100):
    students = []
    for _ in range(n):
        student = {
            "student_id": fake.uuid4(),
            "name": fake.name(),
            "grade_level": random.choice([9, 10, 11, 12]),
            "baseline_ability": np.random.normal(0.5, 0.15) # 0 to 1 scale
        }
        students.append(student)
    return pd.DataFrame(students)

def generate_daily_logs(students_df, days=30):
    logs = []
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    for _, student in students_df.iterrows():
        current_date = start_date
        while current_date <= end_date:
            # Simulate study habits based on ability + noise
            base_study = student['baseline_ability'] * 4 # Max ~4-5 hours
            study_hours = max(0, np.random.normal(base_study, 1.0))
            
            # Simulate attendance (higher ability -> better attendance usually)
            attendance_prob = 0.7 + (student['baseline_ability'] * 0.3)
            attended = 1 if random.random() < attendance_prob else 0
            
            # Subject focus
            subjects = ['Math', 'Science', 'English', 'History']
            focus_subject = random.choice(subjects)
            
            logs.append({
                "student_id": student['student_id'],
                "date": current_date.date(),
                "study_hours": round(study_hours, 1),
                "attendance": attended,
                "focus_subject": focus_subject,
                "sleep_hours": round(np.random.normal(7, 1), 1),
                "screen_time": round(np.random.normal(3, 1.5), 1)
            })
            current_date += timedelta(days=1)
            
    return pd.DataFrame(logs)

def generate_scores(students_df, logs_df):
    scores = []
    # Generate a few tests
    test_dates = sorted(logs_df['date'].unique())[::7] # Weekly tests
    
    for date in test_dates:
        for _, student in students_df.iterrows():
            # Calculate recent study effort
            student_logs = logs_df[(logs_df['student_id'] == student['student_id']) & 
                                 (logs_df['date'] <= date) & 
                                 (logs_df['date'] > date - timedelta(days=7))]
            
            avg_study = student_logs['study_hours'].mean() if not student_logs.empty else 0
            avg_sleep = student_logs['sleep_hours'].mean() if not student_logs.empty else 7
            
            # Score formula: Ability + Effort + Sleep penalty + Random Noise
            base_score = student['baseline_ability'] * 60 # Base up to 60
            effort_bonus = avg_study * 8 # Up to ~32-40
            sleep_penalty = max(0, (7 - avg_sleep) * 2)
            
            final_score = base_score + effort_bonus - sleep_penalty + np.random.normal(0, 5)
            final_score = min(100, max(0, final_score))
            
            scores.append({
                "student_id": student['student_id'],
                "date": date,
                "subject": random.choice(['Math', 'Science', 'English']),
                "score": round(final_score, 1)
            })
            
    return pd.DataFrame(scores)

if __name__ == "__main__":
    print("Generating synthetic data...")
    students = generate_students(200)
    logs = generate_daily_logs(students)
    scores = generate_scores(students, logs)
    
    students.to_csv("students.csv", index=False)
    logs.to_csv("daily_logs.csv", index=False)
    scores.to_csv("scores.csv", index=False)
    print("Data generation complete.")
