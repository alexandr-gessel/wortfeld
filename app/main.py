from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from bson import ObjectId
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime
import re 

load_dotenv()
app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

# MongoDB
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("MONGO_DB_NAME")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db.articles

@app.get("/projekt_wortfeld.html", response_class=HTMLResponse)
async def projekt_wortfeld(request: Request):
    return templates.TemplateResponse("projekt_wortfeld.html", {"request": request})
    
@app.get("/", response_class=HTMLResponse)
def index(request: Request, tag: str = None):
    docs = list(collection.find().sort("date", -1))  # без .limit()
    
    for doc in docs:
        doc["title"] = doc.get("title") or "Kein Titel"
        doc["date"] = datetime.strptime(doc.get("date", "1970-01-01T00:00:00"), "%Y-%m-%dT%H:%M:%S")
        
        text_blocks = doc.get("text", [])
        
        if isinstance(text_blocks, list):
            joined_text = " ".join(text_blocks)
        else:
            joined_text = str(text_blocks)

        joined_text = joined_text.strip()

        # zwei sätze
        sentences = re.split(r'(?<=[.!?]) +', joined_text)
        preview = " ".join(sentences[:2])

        doc["text_preview"] = preview

        # Tags
        preview_tags = []
        for t in doc.get("topics", [])[:3]:
            preview_tags.append({"text": t, "color": "green"})

        overlap = doc.get("keyword_overlap", {})
        tfidf_tag = (overlap.get("topics") or overlap.get("atlas") or [])
        if tfidf_tag:
            tfidf = tfidf_tag[0]
            if tfidf not in [t["text"] for t in preview_tags]:
                preview_tags.append({"text": tfidf, "color": "blue"})



        doc["preview_tags"] = preview_tags 

        

    if tag:
        docs = [doc for doc in docs if tag in [t["text"] for t in doc["preview_tags"]]]

        
        #print(doc["title"], "→", doc["text_preview"][:80])
    
    return templates.TemplateResponse("index.html", {"request": request, "articles": docs, "tag_filter": tag})

@app.get("/article/{id}", response_class=HTMLResponse)
def article_detail(request: Request, id: str):
    doc = collection.find_one({"_id": ObjectId(id)})
    if not doc:
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)

    doc["title"] = doc.get("title") or "Kein Titel"
    doc["date"] = datetime.strptime(doc.get("date", "1970-01-01T00:00:00"), "%Y-%m-%dT%H:%M:%S")
    
    # text
    text_blocks = doc.get("text", [])
    if isinstance(text_blocks, list):
        doc["text"] = "\n\n".join([t.strip() for t in text_blocks if t.strip()])
    else:
        doc["text"] = str(text_blocks).strip()

    # tags
    doc["keyword_overlap"] = doc.get("keyword_overlap", {"topics": [], "atlas": [], "unique": []})

    
    # Google NLP
    google_ents = doc.get("google_entities", [])
    categories = {
        "persons": "PERSON",
        "organizations": "ORGANIZATION",
        "locations": "LOCATION"
    }

    grouped = {}
    for key, gtype in categories.items():
        ents = [
            ent for ent in google_ents
            if ent.get("type") == gtype and "name" in ent
        ]
        ents_sorted = sorted(ents, key=lambda x: -x.get("salience", 0))[:4]
        grouped[key] = [ent["name"] for ent in ents_sorted]

    doc["google_nlp"] = grouped

    return templates.TemplateResponse("article.html", {
        "request": request,
        "article": doc,
        "google_nlp": doc.get("google_nlp", {})
    })


