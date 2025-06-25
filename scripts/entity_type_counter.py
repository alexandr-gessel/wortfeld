# entity_type_counter.py
# suche nach verschidene google entities

from pymongo import MongoClient
from collections import Counter

client = MongoClient("mongodb://localhost:27017/")
db = client["wortfeld"]
collection = db["articles"]

entity_type_counter = Counter()

for doc in collection.find():
    for ent in doc.get("google_entities", []):
        entity_type_counter[ent.get("type", "UNKNOWN")] += 1

for item, count in entity_type_counter.most_common(6):
    print(f"{item}: {count}")


# Ergebnis:
#OTHER: 5875
#PERSON: 2412
#NUMBER: 2044
#ORGANIZATION: 1438
#LOCATION: 1247
#EVENT: 605