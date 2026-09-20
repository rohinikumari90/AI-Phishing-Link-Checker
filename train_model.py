import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
import joblib

# Load the feature dataset
df = pd.read_csv("Dataset/features_dataset.csv")

# Separate features (X) from label (y)
X = df.drop('status', axis=1)
y = df['status']

print("Feature columns:", X.columns.tolist())
print("Total samples:", len(df))

# ---- DIAGNOSTIC: Class balance check ----
print("\n--- Class Distribution ---")
print(df['status'].value_counts())
print("\n--- Class Distribution (%) ---")
print(df['status'].value_counts(normalize=True) * 100)

# ---- DIAGNOSTIC: Confirm which label (0 or 1) means phishing ----
# Whichever group has HIGHER average url_length / num_subdirs is usually "phishing"
print("\n--- Stats by class (helps confirm label mapping) ---")
print("status = 0:")
print(df[df['status'] == 0][['url_length', 'num_subdirs', 'domain_length']].describe())
print("\nstatus = 1:")
print(df[df['status'] == 1][['url_length', 'num_subdirs', 'domain_length']].describe())

# ---- DIAGNOSTIC: Direct check using known domain names ----
# This is the most reliable way to confirm label mapping —
# no assumptions, just look at real known URLs and their status
print("\n--- Known LEGITIMATE domains check (from raw URL file) ---")
try:
    df_raw = pd.read_csv("Dataset/sample_urls_augmented.csv")
    known_safe = df_raw[df_raw['url'].str.contains(
        'google.com|microsoft.com|wikipedia.org|amazon.com|apple.com',
        case=False, na=False, regex=True
    )][['url', 'status']]
    print(known_safe.head(15))

    print("\n--- Suspicious-looking URLs check (from raw URL file) ---")
    known_suspicious = df_raw[df_raw['url'].str.contains(
        'secure-login|verify-account|paypal-|banking-alert',
        case=False, na=False, regex=True
    )][['url', 'status']]
    print(known_suspicious.head(15))
except FileNotFoundError:
    print("Raw URL file not found at Dataset/sample_urls_augmented.csv — skipping this check.")

# Split into train (80%) and test (20%) sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))

# Train a Random Forest Classifier
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1,
    class_weight='balanced'
)
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate
print("\n--- Model Evaluation ---")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred))
print("Recall:", recall_score(y_test, y_pred))
print("F1 Score:", f1_score(y_test, y_pred))
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print("(Rows = Actual, Columns = Predicted | Order follows sorted class labels, e.g. 0 then 1)")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Check which features mattered most (great for your report!)
importances = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)
print("\nFeature Importances:")
print(importances)

# Save the trained model
joblib.dump(model, "Models/phishing_model.pkl")
print("\nModel saved to Models/phishing_model.pkl")
print("\nModel classes (order used in predict_proba):", model.classes_)