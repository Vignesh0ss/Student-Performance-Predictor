import unittest
import pandas as pd
import os
import sqlite3
from model_engine import ModelEngine
import database as db
import shutil

class TestStudentPerformanceSystem(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print("\nStarting System Verification...")
        # Use a test database
        cls.test_db = "test_school_data.db"
        # Backup original if exists (though we shouldn't touch prod db in tests ideally, 
        # but for this script we will mock the db module's DB_NAME)
        
        # Monkey patch database module to use test db
        db.DB_NAME = cls.test_db
        if os.path.exists(cls.test_db):
            os.remove(cls.test_db)
        db.init_db()
        
        cls.engine = ModelEngine()

    @classmethod
    def tearDownClass(cls):
        # On Windows, sometimes the database file is locked, so we use a try-except
        try:
            if os.path.exists(cls.test_db):
                os.remove(cls.test_db)
        except PermissionError:
            pass  # Ignore permission errors on Windows
        print("\nSystem Verification Complete.")

    def test_01_model_training(self):
        """Test if model can train on the CSV data"""
        print("\n[Test] Model Training...")
        try:
            df = pd.read_csv("student-mat.csv", sep=';')
            self.engine.train(df=df)
            self.assertTrue(os.path.exists("models.pkl"), "Model file not created")
            print("   -> Model trained successfully.")
        except Exception as e:
            self.fail(f"Model training failed: {e}")

    def test_02_realtime_prediction(self):
        """Test real-time prediction logic"""
        print("\n[Test] Real-time Prediction...")
        inputs = {
            "G1": 15, "G2": 15, "studytime": 3, "failures": 0,
            "absences": 2, "health": 5, "freetime": 3, "goout": 2
        }
        res = self.engine.predict_realtime(inputs)
        self.assertIn('predicted_score', res)
        self.assertIn('risk_level', res)
        self.assertTrue(0 <= res['predicted_score'] <= 20)
        print(f"   -> Prediction: Score {res['predicted_score']}, Risk {res['risk_level']}")

    def test_03_database_operations(self):
        """Test CRUD operations on SQLite"""
        print("\n[Test] Database Operations...")
        
        # Add Student
        student = {
            "name": "Test Student",
            "G1": 10, "G2": 10, "G3": 10,
            "studytime": 2, "failures": 0, "absences": 5,
            "health": 5, "freetime": 3, "goout": 3,
            "risk_level": 1, "predicted_score": 10.5
        }
        db.add_student(student)
        
        # Retrieve
        df = db.get_all_students()
        self.assertEqual(len(df), 1)
        self.assertEqual(df.iloc[0]['name'], "Test Student")
        print("   -> Student added and retrieved successfully.")

    def test_04_batch_processing(self):
        """Test processing a full CSV and saving to DB"""
        print("\n[Test] Batch Processing & DB Import...")
        df = pd.read_csv("student-mat.csv", sep=';').head(5) # Test with 5 rows
        
        # Predict
        results = self.engine.predict_batch(df)
        self.assertIn('Predicted Score', results.columns)
        
        # Prepare for DB
        results['predicted_score'] = results['Predicted Score']
        results['risk_level'] = results['Risk Val']
        results['name'] = [f"Batch Student {i}" for i in range(len(results))]
        
        # Save
        db.bulk_insert(results)
        
        # Verify
        final_df = db.get_all_students()
        # 1 existing + 5 new = 6
        self.assertEqual(len(final_df), 6)
        print(f"   -> Batch processed and saved. Total students: {len(final_df)}")

if __name__ == '__main__':
    unittest.main()
