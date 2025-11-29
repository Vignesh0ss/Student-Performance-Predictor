#!/usr/bin/env python3
"""
System Verification Script - Tests all major components
"""

def test_imports():
    """Test all required imports"""
    print("Testing imports...")
    try:
        import pandas as pd
        import numpy as np
        import xgboost as xgb
        import streamlit as st
        import plotly
        import sklearn
        import shap
        import sqlalchemy
        print("[OK] All imports successful")
        return True
    except Exception as e:
        print(f"[ERROR] Import error: {e}")
        return False

def test_model_engine():
    """Test model engine functionality"""
    print("Testing model engine...")
    try:
        from model_engine import ModelEngine
        engine = ModelEngine()
        engine.load_models()

        # Test prediction
        inputs = {
            "G1": 15, "G2": 15, "studytime": 3, "failures": 0,
            "absences": 2, "health": 5, "freetime": 3, "goout": 2
        }
        result = engine.predict_realtime(inputs)
        assert 'predicted_score' in result
        assert 'risk_level' in result
        print("[OK] Model engine working")
        return True
    except Exception as e:
        print(f"[ERROR] Model engine error: {e}")
        return False

def test_database():
    """Test database functionality"""
    print("Testing database...")
    try:
        import database as db
        import pandas as pd

        # Test init
        db.init_db()

        # Test add student
        student = {
            "name": "Test Student",
            "G1": 10, "G2": 10, "G3": 10,
            "studytime": 2, "failures": 0, "absences": 5,
            "health": 5, "freetime": 3, "goout": 3,
            "risk_level": 1, "predicted_score": 10.5
        }
        db.add_student(student)

        # Test retrieve
        df = db.get_all_students()
        assert len(df) >= 1
        assert df.iloc[-1]['name'] == "Test Student"

        print("[OK] Database working")
        return True
    except Exception as e:
        print(f"[ERROR] Database error: {e}")
        return False

def test_data_loading():
    """Test data loading from CSV"""
    print("Testing data loading...")
    try:
        import pandas as pd
        df = pd.read_csv("student-mat.csv", sep=';')
        assert len(df) > 0
        assert 'G1' in df.columns
        assert 'G3' in df.columns
        print(f"[OK] Data loaded: {len(df)} rows")
        return True
    except Exception as e:
        print(f"[ERROR] Data loading error: {e}")
        return False

def test_recommendations():
    """Test recommendations system"""
    print("Testing recommendations...")
    try:
        from recommendations import get_recommendations
        from model_engine import ModelEngine

        engine = ModelEngine()
        engine.load_models()

        inputs = {
            "G1": 12, "G2": 12, "studytime": 2, "failures": 0,
            "absences": 5, "health": 4, "freetime": 3, "goout": 3
        }
        result = engine.predict_realtime(inputs)
        recs = get_recommendations(result, role="student", lang="en")
        assert len(recs) > 0
        print(f"[OK] Recommendations generated: {len(recs)} items")
        return True
    except Exception as e:
        print(f"[ERROR] Recommendations error: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("STUDENT PERFORMANCE PREDICTOR - SYSTEM VERIFICATION")
    print("=" * 50)

    tests = [
        test_imports,
        test_data_loading,
        test_model_engine,
        test_database,
        test_recommendations
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1
        print()

    print("=" * 50)
    print(f"RESULTS: {passed}/{total} tests passed")

    if passed == total:
        print("SUCCESS: ALL SYSTEMS OPERATIONAL!")
        print("The Student Performance Predictor is ready to use.")
        print("Run: streamlit run app.py")
    else:
        print("ERROR: Some systems need attention.")

    print("=" * 50)

if __name__ == "__main__":
    main()
