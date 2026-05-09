import os
import json
from tempfile import template
import threading
from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory
from dotenv import load_dotenv
from database import init_db, create_job, update_job_status, get_all_jobs, get_job
from scraper import scrape_product_media
from generator import extract_research_fields, generate_listicle_content

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-key-123")

# Initialize database
init_db()

# Directories
LISTICLES_DIR = os.path.join(os.path.dirname(__file__), 'data', 'listicles')
os.makedirs(LISTICLES_DIR, exist_ok=True)

@app.route('/')
def dashboard():
    jobs = get_all_jobs()
    return render_template('dashboard.html', jobs=jobs)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        product_url = request.form.get('product_url')
        research_file = request.files.get('research_json')
        
        if not product_url or not research_file:
            return "Missing required fields", 400
        
        try:
            research_data = json.load(research_file)
        except Exception as e:
            return f"Invalid JSON file: {e}", 400
        
        # Create pending job
        job_id = create_job(product_url)
        
        # Start background processing
        thread = threading.Thread(target=process_listicle, args=(job_id, product_url, research_data))
        thread.start()
        
        return redirect(url_for('dashboard'))
        
    return render_template('create.html')
def process_listicle(job_id, product_url, raw_research):
    with app.app_context():
        try:
            # 1. Scrape media
            media_urls = scrape_product_media(product_url)
            
            # 2. Extract key research fields
            extracted_research = extract_research_fields(raw_research)
            product_name = extracted_research.get('product_name', 'Product')
            
            # 3. Generate content with Groq
            content = generate_listicle_content(extracted_research, media_urls)
            
            # 4. Render HTML
            from jinja2 import Environment, FileSystemLoader
            env = Environment(loader=FileSystemLoader('templates'))
            template = env.get_template('listicle.html')
            rendered_html = template.render(content=content)
            
            # 5. Save HTML file
            filename = f"listicle_{job_id}.html"
            file_path = os.path.join(LISTICLES_DIR, filename)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(rendered_html)
                
            # 6. Update database
            update_job_status(job_id, 'completed', product_name=product_name, file_path=filename)
            
        except Exception as e:
            print(f"Error processing job {job_id}: {e}")
            import traceback
            traceback.print_exc()
            update_job_status(job_id, 'failed', error_message=str(e))

@app.route('/preview/<filename>')
def preview(filename):
    return send_from_directory(LISTICLES_DIR, filename)

@app.route('/api/jobs')
def api_jobs():
    jobs = [dict(job) for job in get_all_jobs()]
    return jsonify(jobs)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
