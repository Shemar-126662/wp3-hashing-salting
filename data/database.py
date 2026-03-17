import sqlite3

DATABASE = 'student.db'

def get_db_connection():
    conn  = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subjects (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS learning_goals (
            id TEXT PRIMARY KEY,
            subject_id TEXT,
            title TEXT,
            FOREIGN KEY (subject_id) REFERENCES subjects(id)
        )
    ''')
    
    cursor.execute('''
         CREATE TABLE IF NOT EXISTS keywords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS learning_goal_keywords (
            learning_goal_id TEXT,
            keyword_id INTEGER,
            FOREIGN KEY (keyword_id) REFERENCES keywords(id),
            FOREIGN KEY (learning_goal_id) REFERENCES learning_goals(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS student_subjects (
            student_id TEXT,
            subject_id TEXT,
            PRIMARY KEY (student_id, subject_id),
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (subject_id) REFERENCES subjects(id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS snapshots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT,
        learning_goal_id TEXT,
        date TEXT,
        source_type TEXT,
        source_id TEXT,
        FOREIGN KEY (student_id) REFERENCES students(id),
        FOREIGN KEY (learning_goal_id) REFERENCES learning_goals(id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS taxonomy_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            snapshot_id INTEGER,
            level TEXT,
            kennen REAL,
            kunnen REAL,
            confidence REAL,
            FOREIGN KEY (snapshot_id) REFERENCES snapshots(id)
        )
    ''')
    
    conn.commit()
    conn.close()
    
def database_is_empty():
        conn = get_db_connection() 
        count = conn.execute('SELECT COUNT(*) FROM students').fetchone()[0] 
        conn.close() 
        return count == 0
    