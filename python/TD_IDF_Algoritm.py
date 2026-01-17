from sklearn.feature_extraction.text import  TfidfVectorizer
import numpy as np
documents = [
    "The sky is blue",
    "The sun is bright",
    "The sky is blue and the sun is bright",
    "We can see the shining sun, the bright blue sky"
    "The sun is born west"
]


vectorizer = TfidfVectorizer()

# Metinleri fit ve transform etme (TF-IDF hesaplama)
tfidf_matrix = vectorizer.fit_transform(documents)

print("TF-IDF Matriksi:")
print(tfidf_matrix.toarray())

# Kelime (özellik) isimlerini gösterme
print("\nKelime Dağarcığı:")
print(vectorizer.get_feature_names_out())
