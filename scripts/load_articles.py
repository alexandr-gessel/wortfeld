#load_articles.py


import json
import os
from pymongo import MongoClient
from dotenv import load_dotenv
from pathlib import Path

from analyze import analyze_text  # из scripts/analyze.py

# Загрузка переменных окружения
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("MONGO_DB_NAME")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db.articles

# Загрузка JSON
with open(Path("data") / "sampled_output.json", encoding="utf-8") as f:
    articles = json.load(f)

for raw in articles:
    # Пропускаем статьи без текста
    if not raw.get("text"):
        continue

    # Подготовка полей
    clean_text = " ".join(raw["text"]).strip()
    analysis = analyze_text(clean_text)

    document = {
        "date": raw.get("date"),
        "title": raw.get("titel"),
        "atlas": raw.get("atlas", []),
        "topics": raw.get("themen", []),
        "text": clean_text,
        "entities": analysis["entities"],
        "noun_chunks": analysis["noun_chunks"],
        "lemmas": analysis["lemmas"]
    }

    # Вставка в MongoDB
    collection.insert_one(document)

print(f"{len(articles)} Artikel verarbeitet.")
