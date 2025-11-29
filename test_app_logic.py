import pandas as pd
import numpy as np
from model_engine import ModelEngine
import os

def test_backend_logic():
    print("--- 🧪 Testing Backend Logic ---")
    
    # 1. Initialize Engine
    try:
        engine = ModelEngine()
        print("✅ ModelEngine initialized")
    except Exception as e:
        print(f"❌ ModelEngine init failed: {e}")
        return

    # 2. Load Data
    try:
        df = pd.read_csv("student-mat.csv", sep=';')
        print(f"✅ Loaded student-mat.csv ({len(df)} rows)")
    except Exception as e:
        print(f"❌ Failed to load csv: {e}")
        return

    # 3. Test Batch Prediction
    try:
        print("Testing predict_batch...")
        results = engine.predict_batch(df)
        if 'Predicted Score' in results.columns and 'Risk Level' in results.columns:
            print("✅ predict_batch successful")
        else:
            print("❌ predict_batch missing columns")
    except Exception as e:
        print(f"❌ predict_batch failed: {e}")

    # 4. Test Training with DataFrame
    try:
        print("Testing train(df=df)...")
        engine.train(df=df)
        print("✅ Retraining successful")
    except Exception as e:
        print(f"❌ Retraining failed: {e}")

    # 5. Test Real-time Prediction
    try:
        print("Testing predict_realtime...")
        inputs = {
            "G1": 15, "G2": 14, "studytime": 3, "failures": 0,
            "absences": 2, "health": 5, "freetime": 3, "goout": 2
        }
        res = engine.predict_realtime(inputs)
        if res['predicted_score'] > 0:
            print(f"✅ predict_realtime successful (Score: {res['predicted_score']})")
        else:
            print("❌ predict_realtime returned invalid score")
    except Exception as e:
        print(f"❌ predict_realtime failed: {e}")

    print("\n--- ✨ Test Complete ---")

if __name__ == "__main__":
    test_backend_logic()
