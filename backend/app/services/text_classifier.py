from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import text
from strip_markdown import strip_markdown
from sklearn.svm import SVC
import re
# Preprocess text - it is in markdown notation so either convert to plain text or handle markdown appropriately

def preprocess_text(text: str) -> str:
    clean_text = strip_markdown(text)
    clean_text = clean_text.lower()
    
    # Remove URLs, email addresses, and special characters
    clean_text = re.sub(r'http\S+|www\S+|https\S+', '', clean_text)
    clean_text = re.sub(r'\S+@\S+', '', clean_text)
    clean_text = re.sub(r'[^a-zA-Zа-яА-ЯїЇєЄіІґҐ\s]', '', clean_text)
    clean_text = ' '.join(clean_text.split())

    return clean_text

# Vectorization
def vectorize_text(text: str) -> any:
    clean_text = preprocess_text(text)
    with open('backend/app/services/stopwords_ua.txt', 'r', encoding='utf-8') as f:
        stop_words = f.read().splitlines()
        vectorizer = TfidfVectorizer(stop_words=stop_words)
        vectorized = vectorizer.fit_transform([clean_text])
        return vectorized


if __name__ == "__main__":
    markdown = """
## Основні пункти

- **Python** — універсальна мова програмування.
- **Pandas** допомагає аналізувати та обробляти дані.
- **NumPy** забезпечує швидкі числові операції.

> Ефективні інструменти роблять роботу з даними швидшою та зручнішою, а а а.

    """

    print(preprocess_text(markdown))
    print(vectorize_text(markdown))