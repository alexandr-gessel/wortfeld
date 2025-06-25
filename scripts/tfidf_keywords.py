# tfidf_keywords.py

import os
from dotenv import load_dotenv
from pymongo import MongoClient
from sklearn.feature_extraction.text import TfidfVectorizer
from spacy.lang.de.stop_words import STOP_WORDS
from pathlib import Path

# 
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("MONGO_DB_NAME")
COLLECTION_NAME = os.getenv("MONGO_COLLECTION", "articles")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# alle docs
documents = list(collection.find({}, {"_id": 1, "lemmas": 1, "noun_chunks": 1, "entities": 1}))

# vorberitung von corpus
corpus = []
doc_ids = []

for doc in documents:
    # eine Zeile (lemmas + ent + chunks)
    tokens = doc.get("lemmas", []) + doc.get("entities", []) + doc.get("noun_chunks", [])
    text = " ".join(tokens).lower()
    corpus.append(text)
    doc_ids.append(doc["_id"])

#  TF-IDF mit STOP_WORDS
vectorizer = TfidfVectorizer(max_df=0.8, min_df=2, stop_words=list(STOP_WORDS), ngram_range=(1, 3), max_features=1000)
X = vectorizer.fit_transform(corpus)
feature_names = vectorizer.get_feature_names_out()

# топ-N in MongoDB
TOP_N = 10

for i, row in enumerate(X):
    scores = row.toarray().flatten()
    top_indices = scores.argsort()[-TOP_N:][::-1]
    keywords = [feature_names[j] for j in top_indices]

    collection.update_one({"_id": doc_ids[i]}, {"$set": {"tfidf_keywords": keywords}})

print(f"TF-IDF Analyse abgeschlossen. Schlüsselwörter für {len(documents)} Artikel gespeichert.")
