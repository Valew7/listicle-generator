import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'listicles.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    # Ensure data directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_url TEXT NOT NULL,
            product_name TEXT,
            status TEXT DEFAULT 'pending',
            error_message TEXT,
            file_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def create_job(product_url):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO jobs (product_url) VALUES (?)', (product_url,))
    job_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return job_id

def update_job_status(job_id, status, product_name=None, file_path=None, error_message=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if product_name and file_path:
        cursor.execute('''
            UPDATE jobs SET status = ?, product_name = ?, file_path = ?, error_message = ? 
            WHERE id = ?
        ''', (status, product_name, file_path, error_message, job_id))
    else:
        cursor.execute('''
            UPDATE jobs SET status = ?, error_message = ? 
            WHERE id = ?
        ''', (status, error_message, job_id))
    conn.commit()
    conn.close()

def get_all_jobs():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM jobs ORDER BY created_at DESC')
    jobs = cursor.fetchall()
    conn.close()
    return jobs

def get_job(job_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM jobs WHERE id = ?', (job_id,))
    job = cursor.fetchone()
    conn.close()
    return job
