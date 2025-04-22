import os
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
from utils import prepare_dataset
import pandas as pd

def train_model(data_path="C:/Users/saman/Downloads/combined_emails_with_natural_pii.csv"):
    df = pd.read_csv(data_path)
    X, y = prepare_dataset(df)
    encoder = LabelEncoder()
    y_encoded = encoder.fit_transform(y)

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer()),
        ("clf", RandomForestClassifier())
    ])

    pipeline.fit(X, y_encoded)

    os.makedirs("saved_model", exist_ok=True)
    joblib.dump(pipeline, "email_classifier.pkl")
    joblib.dump(encoder, "label_encoder.pkl")
    print("Model and encoder saved.")

def load_model():
    model = joblib.load("email_classifier.pkl")
    encoder = joblib.load("label_encoder.pkl")
    return model, encoder

def predict_category(text, model, encoder):
    pred = model.predict([text])[0]
    return encoder.inverse_transform([pred])[0]

#  Add this block so training runs when you call python models.py
if __name__ == "__main__":
    train_model()
