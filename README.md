# Wortfeld

**Wortfeld** ist ein FastAPI-Projekt zur Analyse und Visualisierung deutschsprachiger Nachrichtenartikel. Es kombiniert spaCy für linguistische Analyse, TF-IDF zur Extraktion von Schlüsselwörtern, MongoDB als Datenbank und Jinja2 für die Darstellung im Webinterface. Das Projekt bildet eine vollständige Verarbeitungskette ab – von der Datenerhebung und -strukturierung bis zur Anzeige der Analyseergebnisse.

## 📌 Projektbeschreibung

Dieses Projekt basiert auf praktischer Erfahrung mit der Entwicklung eines Systems zur Medienbeobachtung deutschsprachiger Nachrichtenquellen in einem Analysezentrum (2020–2021). Die damals eingesetzten Methoden (Parser, MongoDB, spaCy, Benachrichtigungen) wurden in *Wortfeld* übernommen und in einer offenen Variante weiterentwickelt.

Als Datenbasis dient eine Auswahl von Artikeln der Website [Tagesschau.de](https://tagesschau.de). Aus über 11 000 Artikeln wurde mithilfe eines Skripts eine Stichprobe von 96 Artikeln erstellt – etwa 7 bis 8 pro Monat, wobei auf thematische Vielfalt geachtet wurde.

**Umgesetzte Funktionen:**

- Speicherung strukturierter Artikel in **MongoDB**
- Lemmatisierung, POS-Filterung, Extraktion benannter Entitäten und Nominalgruppen via **spaCy**
- Extraktion von Schlüsselwörtern mit **TF-IDF**
- Anreicherung der Daten mit **Google NLP API** (Entitäten, Salienz, Wikipedia-Links)
- Darstellung im Webinterface mit **FastAPI** und **Jinja2**

## 🛠️ Installation und Ausführung

### 1. Projekt klonen

```bash
git clone https://github.com/geromiko/wortfeld.git
cd wortfeld
```

### 2. Virtuelle Umgebung erstellen

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Abhängigkeiten installieren

```bash
pip install -U pip
pip install -r requirements.txt
python -m spacy download de_core_news_md
```

### 4. Umgebungsvariablen definieren

Erstelle eine Datei `.env` im Projektverzeichnis mit folgendem Inhalt:

```env
MONGO_URI=mongodb+srv://benutzer:passwort@cluster.mongodb.net/wortfeld
```

### 5. Daten laden

```bash
python scripts/load_articles.py
python scripts/tfidf_keywords.py
```

### 6. Server starten

```bash
uvicorn app.main:app --reload
```

Die Anwendung ist erreichbar unter: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## 💡 Hinweise

- Getestet mit Python 3.9 und spaCy 3.6
- Verwendete Modell: `de_core_news_md`
- Für Google NLP wird ein eigener API-Key benötigt (nicht im MVP enthalten)
- Die Datengrundlage besteht aus 96 Artikeln (~2.5 MB). Der vollständige Tagesschau-Korpus umfasst >11 000 Artikel.

## 📂 Projektstruktur

```
.
├── README.md
├── about.txt
├── app
│   ├── main.py
│   ├── routes
│   ├── static
│   └── templates
│       ├── article.html
│       ├── index.html
│       └── projekt_wortfeld.html
├── data
│   ├── article_google_nlp.json
│   └── sampled_output.json
├── requirements.txt
└── scripts
    ├── analyze.py
    ├── analyze_google_nlp.py
    ├── compare_keywords.py
    ├── entity_type_counter.py
    ├── load_articles.py
    ├── mongo_google_nlp.py
    └── tfidf_keywords.py
```

## 📄 Weitere Informationen

Eine ausführliche Projektbeschreibung ist auf der Website verfügbar:  
👉 [pythia.one/wortfeld](https://pythia.one/wortfeld)
