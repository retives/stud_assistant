import joblib
from strip_markdown import strip_markdown
import re
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_FILE = os.path.join(BASE_DIR, "svc_model.joblib")
VECTORIZER_FILE = os.path.join(BASE_DIR, "tfidf_vectorizer.joblib")

# Load saved model + vectorizer
vectorizer = joblib.load(VECTORIZER_FILE)
classifier = joblib.load(MODEL_FILE)

def preprocess_text(text: str) -> str:
    clean_text = strip_markdown(text)
    clean_text = clean_text.lower()

    clean_text = re.sub(r'http\S+|www\S+|https\S+', '', clean_text)
    clean_text = re.sub(r'\S+@\S+', '', clean_text)
    clean_text = re.sub(r'[^a-zA-Zа-яА-ЯїЇєЄіІґҐ\s]', '', clean_text)
    clean_text = ' '.join(clean_text.split())
    return clean_text


def predict_label(text: str) -> str:
    clean = preprocess_text(text)
    vec = vectorizer.transform([clean])
    prediction = classifier.predict(vec)
    return prediction[0]
