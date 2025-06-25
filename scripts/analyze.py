# analyze.py
# Простой анализ текста с использованием spaCy:
# извлекает именованные сущности, именные группы и ключевые слова по частям речи.

import spacy
from spacy.lang.de.stop_words import STOP_WORDS

# deutsch
nlp = spacy.load("de_core_news_md")

def analyze_text(text: str) -> dict:
    doc = nlp(text)

    # lemmas (существительные и имена)
    lemmas = [
        token.lemma_.lower()
        for token in doc
        if token.pos_ in {"NOUN", "PROPN"}
        and not token.is_stop
        and not token.is_punct
        and token.lemma_.lower() not in STOP_WORDS
    ]

    # entities
    entities = list({
        " ".join(token.lemma_.lower() for token in ent if not token.is_punct)
        for ent in doc.ents
        if ent.label_ in {"LOC", "ORG", "PERSON", "GPE", "EVENT"}
    })

    # Noun chunks
    noun_chunks = list({
        chunk.lemma_.lower().strip()
        for chunk in doc.noun_chunks
        if len(chunk) > 1
        and not any(token.is_stop or token.is_punct for token in chunk)
    })

    

    return {
        "lemmas" : lemmas,
        "entities": entities,
        "noun_chunks": noun_chunks,
        
    }

# nur fuer test
if __name__ == "__main__":
    sample = (
        "Noch unbekannte Täter haben in der Nacht von Mittwoch auf Donnerstag einen Zigarettenautomaten ins Visier genommen"

    "Nach derzeitigem Ermittlungsstand wurde Donnerstagnacht auf dem Haidach in der Leipziger Straße, vermutlich zwischen 03:50 Uhr bis 04:15 Uhr, ein Zigarettenautomat aufgebrochen und mehrere Zigarettenschachteln entwendet. "
        "Gegen 04:00 Uhr soll es zu einem Knall gekommen sein. Bislang unklar ist, ob dieser durch eine mögliche Sprengung des Automaten entstanden ist."
        " Die Polizei bittet Zeugen oder Hinweisgeber, sich unter der Rufnummer 07231 1863311 beim Polizeirevier Süd zu melden."
    )

    result = analyze_text(sample)
    
    for k, v in result.items():
        print(f"\n{k.upper()} ({len(v)}):")
        for item in sorted(v):
            print("  -", item)
