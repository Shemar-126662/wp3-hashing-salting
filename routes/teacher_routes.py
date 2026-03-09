from flask import Blueprint, jsonify, render_template
from data.database import get_db_connection

teacher_bp = Blueprint('teacher', __name__)

@teacher_bp.route('/teacher')
def teacher_dashboard():
    conn = get_db_connection()
    
    students = conn.execute('SELECT * FROM students').fetchall()
    
    conn.close()
    
    return render_template('teacher_dashboard.html', students=students)
