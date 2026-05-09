# List-Test: AI Listicle Generator

A complete web application for generating high-converting listicle pre-landing pages (advertorials) for ecommerce products using AI.

## Features
- **Dashboard**: View and manage all generated listicles.
- **AI-Powered**: Uses Groq API (llama-3.3-70b-versatile) for content generation.
- **Automated Scraping**: Extracts images and videos from product URLs.
- **Editorial Design**: Professional listicle templates inspired by top-performing advertorials.

## Setup Instructions

1. **Environment Variables**:
   Copy `.env.example` to `.env` and add your Groq API key:
   ```bash
   cp .env.example .env
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```bash
   python app.py
   ```

4. **Access the App**:
   Open [http://localhost:5000](http://localhost:5000) in your browser.

## Project Structure
- `app.py`: Flask routes and server logic.
- `scraper.py`: Logic for scraping product media.
- `generator.py`: Groq API integration for content generation.
- `database.py`: SQLite database operations.
- `templates/`: Jinja2 HTML templates.
- `static/`: CSS and JavaScript files.
- `data/listicles/`: Generated HTML files.
