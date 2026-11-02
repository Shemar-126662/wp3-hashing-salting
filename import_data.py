import json
from data.database import get_db_connection
from security import hash_password

    
def import_data():
    with open('data-sample.json', encoding='utf-8') as f:
        data = json.load(f)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Voeg docenten toe
    teachers = [
        ("Louella", "louella@admin.com", "louella123", "teacher"),
        ("Lars", "lars@admin.com", "lars123", "teacher"),
        ("Sietze", "sietze@admin.com", "sietze123", "teacher"),
        ("Diederik", "diederik@admin.com", "diederik123", "teacher"),
    ]
    for name, email, password, role in teachers:
        cursor.execute('''
            INSERT OR IGNORE INTO users (name, email, password_hash, role)
            VALUES (?, ?, ?, ?)
        ''', (name, email, hash_password(password), role))

    for entry in data["entries"]:
        student = entry["student"]
        subject = entry["subject"]

        name = student['name']

        users_map = {
            "Milan": ("milan@test.com", "milan123", "student"),
            "Emma": ("emma@test.com", "emma123", "student"),
            "Jamie": ("jamie@test.com", "jamie123", "student"),
            "Lotte": ("lotte@test.com", "lotte123", "student"),
            "Sam": ("sam@test.com", "sam123", "student"),
            "Daan": ("daan@test.com", "daan123", "student"),
            "Robin": ("robin@test.com", "robin123", "student"),
            "Noah": ("noah@test.com", "noah123", "student"),
            "Taylor": ("taylor@test.com", "taylor123", "student"),
            "Alex": ("alex@test.com", "alex123", "student"),
        }

        if name in users_map:
            email, password, role = users_map[name]
        else:
            email = f"{name.lower()}@test.com"
            password = "1234"
            role = "student"

        if not cursor.execute('SELECT 1 FROM users WHERE email = ?', (email,)).fetchone():
            cursor.execute('''
                INSERT OR IGNORE INTO users (name, email, password_hash, role)
                VALUES (?, ?, ?, ?)
            ''', (name, email, hash_password(password), role))
        cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
        user_row = cursor.fetchone()
        user_id = user_row[0] if user_row else None

        cursor.execute('''
            INSERT OR IGNORE INTO students (id, user_id, name)
            VALUES (?, ?, ?)
        ''', (student['id'], user_id, name))

        cursor.execute('INSERT OR IGNORE INTO subjects (id, name) VALUES (?, ?)', (subject['id'], subject['name']))
        cursor.execute('INSERT OR IGNORE INTO student_subjects (student_id, subject_id) VALUES (?, ?)', (student['id'], subject['id']))
        
        for lg in entry.get("learningGoals", []):
            cursor.execute('INSERT OR IGNORE INTO learning_goals (id, subject_id, title) VALUES (?, ?, ?)', (lg['id'], subject['id'], lg['title']))
            
            for keywords in lg.get("keywords", []):
                cursor.execute('INSERT OR IGNORE INTO keywords (name) VALUES (?)', (keywords,))
                
                cursor.execute('SELECT id FROM keywords WHERE name = ?', (keywords,))
                keyword_id = cursor.fetchone()[0]
                
                cursor.execute('INSERT OR IGNORE INTO learning_goal_keywords (learning_goal_id, keyword_id) VALUES (?, ?)', (lg['id'], keyword_id))
                
            for snapshot in lg.get("snapshots", []):
                cursor.execute('''INSERT OR IGNORE INTO snapshots (student_id, learning_goal_id, date, source_type, source_id) VALUES (?,?, ?, ?, ?)'''
                           ,
                           (
                                 student['id'], lg['id'], snapshot['at'], snapshot['source']['type'], snapshot['source']['id']
                           )
                        )
                cursor.execute('''
                            SELECT id FROM snapshots 
                            WHERE student_id = ? 
                            AND learning_goal_id = ? 
                            AND date = ? 
                            AND source_id = ?
                        ''', (student['id'], lg['id'], snapshot['at'], snapshot['source']['id']))

                row = cursor.fetchone()
                if row:
                    snapshot_id = row[0]
                else:
                    continue            
                for tax in snapshot.get("taxonomy", []):
                        cursor.execute('''INSERT OR IGNORE INTO taxonomy_scores (snapshot_id, level, kennen, kunnen, confidence) VALUES (?, ?, ?, ?, ?)'''
                           ,
                           (
                                 snapshot_id, tax['level'], tax['kennen'], tax['kunnen'], tax['confidence']
                           )
                        )
                
        
        
    conn.commit()
    conn.close()
