#compare_keywords.py

from pymongo import MongoClient
from dotenv import load_dotenv
import os

# load .env 
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("MONGO_DB_NAME")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db.articles

# tfidf_keywords
articles = collection.find({"tfidf_keywords": {"$exists": True}})

updated_count = 0

for article in articles:
    tfidf_keywords = set(word.lower() for word in article.get("tfidf_keywords", []))
    topics = set(word.lower() for word in article.get("topics", []))
    atlas = set(word.lower() for word in article.get("atlas", []))

    overlap_topics = tfidf_keywords & topics
    overlap_atlas = tfidf_keywords & atlas
    unique = tfidf_keywords - overlap_topics - overlap_atlas

    keyword_overlap = {
        "topics": list(overlap_topics),
        "atlas": list(overlap_atlas),
        "unique": list(unique)
    }

    collection.update_one(
        {"_id": article["_id"]},
        {"$set": {"keyword_overlap": keyword_overlap}}
    )
    updated_count += 1

print(f"{updated_count} Dokumente aktualisiert mit keyword_overlap.")
