import pandas as pd
import numpy as np
import xgboost as xgb
import shap
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, accuracy_score

class ModelEngine:
    def __init__(self):
        self.regressor = None
        self.classifier = None
        self.explainer = None
        # Features selected from student-mat.csv
        self.feature_names = [
            "G1", "G2", "studytime", "failures", "absences", 
            "health", "freetime", "goout"
        ]
        
    def train(self, data_path="student-mat.csv", df=None):
        print("Loading data...")
        if df is None:
            # Load semicolon separated file
            df = pd.read_csv(data_path, sep=';')
        
        # Select features and target
        X = df[self.feature_names]
        y_score = df['G3']
        
        # Risk class: 0=Low (>15), 1=Medium (10-15), 2=High (<10)
        # G3 is 0-20 scale
        y_risk = pd.cut(df['G3'], bins=[-1, 9, 14, 21], labels=[2, 1, 0]).astype(int)
        
        # Train Regressor
        print("Training Regressor...")
        self.regressor = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100)
        self.regressor.fit(X, y_score)
        
        # Train Classifier
        print("Training Classifier...")
        self.classifier = xgb.XGBClassifier(eval_metric='mlogloss')
        self.classifier.fit(X, y_risk)
        
        # Setup SHAP
        print("Setting up SHAP...")
        self.explainer = shap.TreeExplainer(self.regressor)
        
        self.save_models()
        print("Training complete.")
        
    def save_models(self):
        with open("models.pkl", "wb") as f:
            pickle.dump({
                "regressor": self.regressor,
                "classifier": self.classifier,
                "explainer": self.explainer
            }, f)
            
    def load_models(self):
        if os.path.exists("models.pkl"):
            with open("models.pkl", "rb") as f:
                models = pickle.load(f)
                self.regressor = models["regressor"]
                self.classifier = models["classifier"]
                self.explainer = models["explainer"]
            return True
        return False

    def predict_batch(self, df):
        """
        Predicts for a whole dataframe.
        Returns dataframe with 'Predicted Score', 'Risk Level', 'Risk Val'
        """
        if not self.regressor:
            if not self.load_models():
                raise Exception("Models not trained or loaded")
        
        # Ensure columns exist
        X = df[self.feature_names]
        
        pred_scores = self.regressor.predict(X)
        pred_risks = self.classifier.predict(X)
        risk_labels = {0: "Low Risk", 1: "Medium Risk", 2: "High Risk"}
        
        results = df.copy()
        results['Predicted Score'] = np.round(pred_scores, 1)
        results['Risk Val'] = pred_risks
        results['Risk Level'] = [risk_labels[r] for r in pred_risks]
        
        return results
        
    def predict_realtime(self, inputs):
        """
        inputs: dict with keys matching self.feature_names
        """
        if not self.regressor:
            if not self.load_models():
                raise Exception("Models not trained or loaded")
                
        # Prepare input
        input_df = pd.DataFrame([inputs], columns=self.feature_names)
        
        # Predict
        pred_score = self.regressor.predict(input_df)[0]
        pred_risk = self.classifier.predict(input_df)[0]
        risk_labels = {0: "Low Risk", 1: "Medium Risk", 2: "High Risk"}
        
        # Explain
        shap_values = self.explainer.shap_values(input_df)
        
        # Format SHAP for frontend
        explanation = []
        for i, feature in enumerate(self.feature_names):
            explanation.append({
                "feature": feature,
                "value": inputs[feature],
                "impact": shap_values[0][i]
            })
            
        return {
            "predicted_score": round(float(pred_score), 1), # Scale 0-20
            "predicted_score_100": round(float(pred_score) * 5, 1), # Scale 0-100 for UI
            "risk_category": risk_labels[pred_risk],
            "risk_level": int(pred_risk), # 0, 1, 2
            "explanation": explanation
        }

if __name__ == "__main__":
    engine = ModelEngine()
    engine.train()
