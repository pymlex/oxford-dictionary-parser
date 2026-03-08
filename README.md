# Oxford Dictionary Parser

<img width="1328" height="200" alt="image" src="https://github.com/user-attachments/assets/70699f48-3aac-4164-8daf-9da04b9b06d8" />

A FastAPI service that provides information from Oxford Learner's Dictionaries as structured entries. Can be used as a no-login OALD API only in educational purposes.

---

## Key features

* Fetches pages with rotating user-agent.
* Extracts: headword, parts of speech, phonetics (UK/US), examples, verb forms, related entries, and origin when present.
* Optional multi-page crawling for related entries (configurable via `MAX_PAGES`).

## Repo layout

````
.
├── app/
│   ├── api.py          
│   ├── fetcher.py      
│   ├── parser.py       
│   ├── config.py       
│   └── main.py
├── requirements.txt
└── .env                
````

---

## Installation

For Windows users:

```bash
git clone https://github.com/youruser/oxford-dictionary-parser.git
cd oxford-dictionary-parser
.\setip.bat
````

Set variables or put `.env` with:

```
MAX_PAGES=4
USER_AGENT_POOL=auto
```

---

## Running

```
.venv\Scripts\activate
python -m uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload
```

---

## API

`GET /api/parse?word=<word>` — returns JSON:

```json
{
  "status": "ok",
  "word": "<headword>",
  "pages_found": 2,
  "results": [
    {
      "entry_id": "...",
      "headword": "steer",
      "part_of_speech": "verb",
      "phonetics": {
         "uk": {"text": "/stɪə(r)/","audio":"https://..."},
         "us": {...}
      },
      "verb_forms":[...],
      "senses":[
         {
           "group": null,
           "definition":"to control",
           "examples":["..."]
         }
      ],
      "origin": "from Old French ...",
      "related_entries":[...]
    }
  ]
}
```
