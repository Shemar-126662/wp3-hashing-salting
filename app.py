from flask import Flask, render_template
import sqlite3

from data.database import init_db, get_db_connection, database_is_empty
import os
import zipfile


app = Flask(__name__)

def unzip_data():
    if not os.path.exists('data-sample.json'):
        with zipfile.ZipFile('data-sample.zip', 'r') as zip_ref:
            zip_ref.extractall('.')



def get_db_connection():
    conn  = sqlite3.connect('student.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    return render_template('index.html', students=students)

unzip_data()
init_db()

if database_is_empty():
    from import_data import import_data
    import_data()

if __name__ == '__main__':
    app.run(debug=True)

