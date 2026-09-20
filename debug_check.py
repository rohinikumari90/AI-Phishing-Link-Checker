import pandas as pd
import joblib
from feature_extraction import extract_features

model = joblib.load("Models/phishing_model.pkl")

test_url = "https://google.com"
features = extract_features(test_url)

print("Extracted features for:", test_url)
for k, v in features.items():
    print(f"  {k}: {v}")

features_df = pd.DataFrame([features])
proba = model.predict_proba(features_df)[0]
print("\nPrediction probabilities:")
print("  Phishing (0):", proba[0])
print("  Legitimate (1):", proba[1])