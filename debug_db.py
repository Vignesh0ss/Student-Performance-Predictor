import pandas as pd
import sqlite3
import database as db

try:
    print("Init DB...")
    db.init_db()
    
    print("Creating DF...")
    df = pd.DataFrame({
        "name": ["Test"],
        "G1": [10], "G2": [10], "G3": [10],
        "studytime": [1], "failures": [0], "absences": [0],
        "health": [1], "freetime": [1], "goout": [1],
        "risk_level": [0], "predicted_score": [10.0]
    })
    
    print("Bulk Insert...")
    db.bulk_insert(df)
    print("Insert Done.")
    
    print("Read...")
    res = db.get_all_students()
    print(res)
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
