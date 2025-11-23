from sklearn.feature_extraction.text import TfidfVectorizer
from strip_markdown import strip_markdown
from sklearn.svm import SVC
import pandas as pd
import re
import joblib
import os

# Отримати директорію скрипту
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Шляхи до файлів
TRAIN_FILE = os.path.join(BASE_DIR, "data", "train.json")
TEST_FILE = os.path.join(BASE_DIR, "data", "test.json")
STOPWORDS_FILE = os.path.join(BASE_DIR, "stopwords_ua.txt")
MODEL_FILE = os.path.join(BASE_DIR, "svc_model.joblib")
VECTORIZER_FILE = os.path.join(BASE_DIR, "tfidf_vectorizer.joblib")

# Preprocess text
def preprocess_text(text: str) -> str:
    clean_text = strip_markdown(text)
    clean_text = clean_text.lower()

    clean_text = re.sub(r'http\S+|www\S+|https\S+', '', clean_text)
    clean_text = re.sub(r'\S+@\S+', '', clean_text)
    clean_text = re.sub(r'[^a-zA-Zа-яА-ЯїЇєЄіІґҐ\s]', '', clean_text)
    clean_text = ' '.join(clean_text.split())

    return clean_text


def train_classifier(X, y):
    # Load stopwords
    with open(STOPWORDS_FILE, 'r', encoding='utf-8') as f:
        stop_words = f.read().splitlines()

    # Create SINGLE vectorizer
    vectorizer = TfidfVectorizer(stop_words=stop_words)

    # Fit vectorizer on ALL training data
    X_vectors = vectorizer.fit_transform(X)

    # Train SVC
    classifier = SVC(kernel='linear')
    classifier.fit(X_vectors, y)

    return vectorizer, classifier


def predict_label(vectorizer, classifier, text: str):
    clean = preprocess_text(text)
    vec = vectorizer.transform([clean])
    return classifier.predict(vec)


if __name__ == "__main__":

    train_data = pd.read_json(TRAIN_FILE)
    test_data = pd.read_json(TEST_FILE)

    X = train_data['text'].apply(preprocess_text)
    y = train_data['label']

    X_test = test_data['text'].apply(preprocess_text)   

    # Train
    vectorizer, model = train_classifier(X, y)

    # Predict test samples
    result = pd.DataFrame(columns=['predicted_label', 'actual_label'])
    result['predicted_label'] = model.predict(vectorizer.transform(X_test))
    result['actual_label'] = test_data['label']
    print(result)
    
    joblib.dump(model, MODEL_FILE)
    joblib.dump(vectorizer, VECTORIZER_FILE)
