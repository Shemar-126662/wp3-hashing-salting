import json
from data.database import get_db_connection

    
def import_data():
    with open('data-sample.json', encoding='utf-8') as f:
        data = json.load(f)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    for entry in data["entries"]:
        student = entry["student"]
        subject = entry["subject"]
        
        cursor.execute('INSERT OR IGNORE INTO students (id, name) VALUES (?, ?)', (student['id'], student['name']))
        cursor.execute('INSERT OR IGNORE INTO subjects (id, name) VALUES (?, ?)', (subject['id'], subject['name']))
        cursor.execute('INSERT OR IGNORE INTO student_subjects (student_id, subject_id) VALUES (?, ?)', (student['id'], subject['id']))
        
        for lg in entry.get("learningGoals", []):
            cursor.execute('INSERT OR IGNORE INTO learning_goals (id, subject_id, title) VALUES (?, ?, ?)', (lg['id'], subject['id'], lg['title']))
            
            for keywords in lg.get("keywords", []):
                cursor.execute('INSERT OR IGNORE INTO keywords (name) VALUES (?)', (keywords,))
                
                # get keyword id
                cursor.execute('SELECT id FROM keywords WHERE name = ?', (keywords,))
                keyword_id = cursor.fetchone()[0]
                
                cursor.execute('INSERT OR IGNORE INTO learning_goal_keywords (learning_goal_id, keyword_id) VALUES (?, ?)', (lg['id'], keyword_id))
                
            for snapshot in lg.get("snapshots", []):
                cursor.execute('''INSERT INTO snapshots (student_id, learning_goal_id, date, source_type, source_id) VALUES (?,?, ?, ?, ?)'''
                           ,
                           (
                                 student['id'], lg['id'], snapshot['at'], snapshot['source']['type'], snapshot['source']['id']
                           )
                        )
                snapshot_id = cursor.lastrowid
            
                for tax in snapshot.get("taxonomy", []):
                        cursor.execute('''INSERT INTO taxonomy_scores (snapshot_id, level, kennen, kunnen, confidence) VALUES (?, ?, ?, ?, ?)'''
                           ,
                           (
                                 snapshot_id, tax['level'], tax['kennen'], tax['kunnen'], tax['confidence']
                           )
                        )
                
        
        
    conn.commit()
    conn.close()
