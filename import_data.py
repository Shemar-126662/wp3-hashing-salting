import json
import sqlite3

def get_db_connection():
    conn  = sqlite3.connect('student.db')
    conn.row_factory = sqlite3.Row
    return conn
    
def import_data():
    with open('data-sample.json') as f:
        data = json.load(f)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    for entry in data["entries"]:
        student = entry["student"]
        subject = entry["subject"]
        
        cursor.execute('INSERT OR IGNORE INTO students (id, name) VALUES (?, ?)', (student['id'], student['name']))
        cursor.execute('INSERT OR IGNORE INTO subjects (id, name) VALUES (?, ?)', (subject['id'], subject['name']))
    conn.commit()
    conn.close()
