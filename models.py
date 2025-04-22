import os
import joblib
import re
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
from utils import prepare_dataset, mask_pii


# Rule-based detection for Incident
def classify_incident(email):
    incident_keywords = [
        "unauthorized access", "exposed", "leak", "data dump", "log file", "security alert", 
        "breach", "attack", "hacked", "leaked", "public forum", "git repo", "credentials"
    ]
    if any(kw in email.lower() for kw in incident_keywords):
        return "Incident"
    return None


# Rule-based detection for Transaction
def classify_transaction(email):
    transaction_keywords = [
        "card", "cvv", "expiry", "transaction", "bank", "payment", "account", 
        "credit", "debit", "pin", "upi", "ifsc"
    ]
    if any(keyword in email.lower() for keyword in transaction_keywords):
        return "Transaction"
    return None


# Rule-based detection for Change
def classify_change(email):
    change_keywords = [
        "change", "update", "modify", "new", "revision", "alter", "amend", "adjust"
    ]
    if any(keyword in email.lower() for keyword in change_keywords):
        return "Change"
    return None


# Rule-based detection for Problem
def classify_problem(email):
    problem_keywords = [
        "issue", "problem", "error", "complaint", "failure", "bug", "technical issue", 
        "outage", "broken", "defect", "problematic"
    ]
    if any(keyword in email.lower() for keyword in problem_keywords):
        return "Problem"
    return None


# Train the model
def train_model(data_path="combined_emails_with_natural_pii.csv"):
    df = pd.read_csv(data_path)
    X, y = prepare_dataset(df)

    # Update categories using rule-based logic
    y_updated = []
    for email, label in zip(X, y):
        category = classify_incident(email) or classify_transaction(email) or classify_change(email) or classify_problem(email) or label
        y_updated.append(category)

    # Encode labels
    encoder = LabelEncoder()
    y_encoded = encoder.fit_transform(y_updated)

    # Train pipeline
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer()),
        ("clf", RandomForestClassifier())
    ])
    pipeline.fit(X, y_encoded)

    # Save model and encoder
    os.makedirs("saved_model", exist_ok=True)
    joblib.dump(pipeline, "email_classifier.pkl")
    joblib.dump(encoder, "label_encoder.pkl")
    print(" Model and encoder saved.")


# Load saved model and encoder
def load_model():
    model = joblib.load("email_classifier.pkl")
    encoder = joblib.load("label_encoder.pkl")
    return model, encoder


# Predict the category of the email
def predict_category(text, model, encoder):
    # Priority: Incident > Transaction > Change > Problem > ML model
    if classify_incident(text):
        return "Incident"
    elif classify_transaction(text):
        return "Transaction"
    elif classify_change(text):
        return "Change"
    elif classify_problem(text):
        return "Problem"
    else:
        pred = model.predict([text])[0]
        return encoder.inverse_transform([pred])[0]


# Run training directly
if __name__ == "__main__":
    train_model()
