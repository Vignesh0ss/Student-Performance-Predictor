import sqlite3
import pandas as pd
import os
from sqlalchemy import create_engine

DB_NAME = "school_data.db"

def get_engine():
    return create_engine(f'sqlite:///{DB_NAME}')

def init_db():
    """Initialize the database with the students table."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT DEFAULT 'Student',
            G1 INTEGER,
            G2 INTEGER,
            G3 INTEGER,
            studytime INTEGER,
            failures INTEGER,
            absences INTEGER,
            health INTEGER,
            freetime INTEGER,
            goout INTEGER,
            risk_level INTEGER,
            predicted_score REAL
        )
    ''')
    conn.commit()
    conn.close()

def add_student(data):
    """
    Add a single student record.
    data: dict with keys matching columns
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Ensure all fields are present with defaults
    fields = ["name", "G1", "G2", "G3", "studytime", "failures", "absences", "health", "freetime", "goout", "risk_level", "predicted_score"]
    values = [data.get(f, 0) if f != "name" else data.get(f, "Student") for f in fields]
    
    c.execute(f'''
        INSERT INTO students ({", ".join(fields)})
        VALUES ({", ".join(["?"] * len(fields))})
    ''', values)
    
    conn.commit()
    conn.close()

def bulk_insert(df):
    """
    Insert a dataframe of students.
    df: pandas DataFrame
    """
    engine = get_engine()

    # Only keep columns that exist in the database schema
    db_columns = ["student_id", "name", "G1", "G2", "G3", "studytime", "failures", "absences", "health", "freetime", "goout", "risk_level", "predicted_score"]
    df_filtered = df[[col for col in db_columns if col in df.columns]]

    df_filtered.to_sql('students', engine, if_exists='append', index=False)

def get_all_students():
    """Return all students as a DataFrame."""
    engine = get_engine()
    try:
        df = pd.read_sql("SELECT * FROM students", engine)
    except:
        df = pd.DataFrame()
    return df

def clear_db():
    """Clear all data (for testing/reset)."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM students")
    conn.commit()
    conn.close()

# Initialize on import
init_db()
