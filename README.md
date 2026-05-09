# Listicle Generator

Built by Valentina for the Elevate Group / WideStep AI Automation Engineer assessment.

---

## What it does

You paste a product URL and upload a research JSON file. The app scrapes the product images, sends the research to an LLM, and generates a full static advertorial page — zero manual editing.

Two pages:
- **/create** — submit a new listicle
- **/dashboard** — see all generated listicles and preview them

---

## Stack

- Python + Flask
- Groq API (llama-3.3-70b-versatile)
- BeautifulSoup for scraping
- Jinja2 for templating
- SQLite for persistence

---

## How to run it

**1. Clone the repo**
```bash
git clone 
cd listicle-generator
```

**2. Create a virtual environment**
```bash
python -m venv venv

# Mac/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Add your Groq API key**

Create a `.env` file in the root folder:
GROQ_API_KEY=your_key_here
Get a free key at https://console.groq.com

**5. Run**
```bash
python app.py
```

Open http://localhost:5000

---

## Project structure
├── app.py              # routes and pipeline orchestration
├── database.py         # SQLite setup
├── core/
│   ├── scraper.py      # pulls images from product URL
│   ├── generator.py    # calls Groq, returns structured copy
│   └── assembler.py    # renders the final HTML
├── templates/
│   ├── create.html
│   ├── dashboard.html
│   └── listicle.html
└── outputs/            # generated pages land here

---

## Known limitations

- The scraper works on most Shopify stores. If a store blocks it, the job won't crash — it just continues with whatever images it found.
- SQLite is fine for local use. For production I'd swap it for Postgres and move file storage to S3.
- Groq's free tier has rate limits. For high volume I'd add a job queue.

---

## Dependencies

| Package | Why |
|---|---|
| Flask | web server |
| Groq | LLM API |
| BeautifulSoup4 | scraping |
| Jinja2 | templating |
| python-dotenv | loads the API key from .env |
| requests | HTTP calls |
