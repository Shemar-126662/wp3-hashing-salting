from flask import Flask, redirect, render_template, request, url_for
from data.database import init_db, get_db_connection, database_is_empty
import os
import zipfile
from routes.student_routes import student_bp
from routes.teacher_routes import teacher_bp
from routes.auth_routes import auth_bp

app = Flask(__name__)

from routes.student_routes import student_bp
from routes.teacher_routes import teacher_bp

app.register_blueprint(student_bp)
app.register_blueprint(teacher_bp)
app.register_blueprint(auth_bp)

def unzip_data():
    if not os.path.exists('data-sample.json'):
        with zipfile.ZipFile('data-sample.zip', 'r') as zip_ref:
            zip_ref.extractall('.')

@app.route('/')
def index():
    return render_template('index.html')


app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(32)


unzip_data()
init_db()

if database_is_empty():
    from import_data import import_data
    import_data()

if __name__ == '__main__':
    app.run(debug=False)
