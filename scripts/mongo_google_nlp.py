# mongo_google_nlp.py
# füer 96 Artikel aus Mongo

from pymongo import MongoClient
from google.cloud import language_v1
from dotenv import load_dotenv
from tqdm import tqdm
import os

# 
load_dotenv()

# MongoDB
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("MONGO_DB_NAME")
COLLECTION_NAME = os.getenv("MONGO_COLLECTION", "articles")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# init  Google NLP 
gclient = language_v1.LanguageServiceClient()

# alle texte
documents = list(collection.find({}))

for doc in tqdm(documents, desc="Google NLP для статей"):
    doc_id = doc["_id"]
    text = " ".join(doc["text"]) if isinstance(doc["text"], list) else str(doc["text"])

    document = language_v1.Document(
        content=text,
        type_=language_v1.Document.Type.PLAIN_TEXT,
        language="de"
    )

    # entities
    try:
        response_entities = gclient.analyze_entities(document=document)
        google_entities = [
            {
                "name": e.name,
                "type": language_v1.Entity.Type(e.type_).name,
                "salience": round(e.salience, 4)
            }
            for e in response_entities.entities
        ]
    except Exception as e:
        google_entities = []
        print(f"[{doc_id}] ERROR в analyze_entities: {e}")

    # categories
    try:
        if len(text) > 1000 :
            response_categories = gclient.classify_text(document=document)
            google_categories = [
                {
                    "name": c.name,
                    "confidence": round(c.confidence, 4)
                }
                for c in response_categories.categories
            ]
        else:
            google_categories = []
    except Exception as e:
        google_categories = []
        print(f"[{doc_id}] ERROR в classify_text: {e}")

    # update MongoDB-doc
    collection.update_one(
        {"_id": doc_id},
        {"$set": {
            "google_entities": google_entities,
            "google_categories": google_categories
        }}
    )