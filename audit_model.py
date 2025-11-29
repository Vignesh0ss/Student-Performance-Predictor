import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, accuracy_score, r2_score
import pickle

def audit_model():
    print("--- Model Reality Audit ---")
    
    # 1. Check Data Source
    try:
        df = pd.read_csv("student-mat.csv", sep=';')
        print(f"[OK] Data Source: Real Kaggle Dataset found ({len(df)} rows)")
    except Exception as e:
        print(f"[ERROR] Data Source Error: {e}")
        return

    # 2. Train/Test Split & Evaluate
    feature_names = ["G1", "G2", "studytime", "failures", "absences", "health", "freetime", "goout"]
    X = df[feature_names]
    y_score = df['G3']
    y_risk = pd.cut(df['G3'], bins=[-1, 9, 14, 21], labels=[2, 1, 0]).astype(int)

    X_train, X_test, y_train, y_test = train_test_split(X, y_score, test_size=0.2, random_state=42)
    _, _, y_risk_train, y_risk_test = train_test_split(X, y_risk, test_size=0.2, random_state=42)

    # Load trained model
    try:
        with open("models.pkl", "rb") as f:
            models = pickle.load(f)
            regressor = models["regressor"]
            classifier = models["classifier"]
            print("[OK] Model Artifact: 'models.pkl' loaded successfully")
    except:
        print("[ERROR] Model Artifact: Not found (Training new one for audit...)")
        regressor = xgb.XGBRegressor(objective='reg:squarederror')
        regressor.fit(X_train, y_train)
        classifier = xgb.XGBClassifier(eval_metric='mlogloss')
        classifier.fit(X_train, y_risk_train)

    # 3. Metrics
    preds = regressor.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    r2 = r2_score(y_test, preds)
    
    risk_preds = classifier.predict(X_test)
    acc = accuracy_score(y_risk_test, risk_preds)

    print(f"\nPerformance Metrics (Real Test Set):")
    print(f"   - RMSE (Error Margin): {rmse:.2f} (Scale 0-20)")
    print(f"   - R2 Score (Accuracy): {r2:.2f} (Target > 0.8)")
    print(f"   - Risk Classification Accuracy: {acc*100:.1f}%")

    if r2 > 0.8:
        print("[GOOD] Verdict: HIGH ACCURACY. The model is effectively using G1/G2 to predict G3.")
    elif r2 > 0.5:
        print("[WARNING] Verdict: MODERATE ACCURACY. Useful but has error.")
    else:
        print("[BAD] Verdict: POOR ACCURACY. Model is guessing.")

    # 4. Feature Importance
    print("\nKey Drivers (Feature Importance):")
    importances = regressor.feature_importances_
    for name, imp in zip(feature_names, importances):
        print(f"   - {name}: {imp:.4f}")

    if importances[0] > 0.5 or importances[1] > 0.5:
        print("\n[INFO] Insight: The model relies HEAVILY on past grades (G1/G2). This is realistic but expected.")

if __name__ == "__main__":
    audit_model()
