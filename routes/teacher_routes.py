from flask import Blueprint, jsonify, render_template
from data.database import get_db_connection

teacher_bp = Blueprint('teacher', __name__)

@teacher_bp.route('/teacher')
def teacher_dashboard():
    conn = get_db_connection()
    
    students = conn.execute('SELECT * FROM students').fetchall()
    
    conn.close()
    
    return render_template('teacher_dashboard.html', students=students)

@teacher_bp.route('/api/class-overview')
def api_class_overview():
    conn = get_db_connection()
    
    rows = conn.execute('''
        SELECT 
            students.id,
            students.name,
            AVG((taxonomy_scores.kennen + taxonomy_scores.kunnen) / 2.0) as avg_score
            from students
            JOIN student_subjects ON students.id = student_subjects.student_id
            JOIN learning_goals ON student_subjects.subject_id = learning_goals.subject_id
            JOIN snapshots ON learning_goals.id = snapshots.learning_goal_id
            JOIN taxonomy_scores ON snapshots.id = taxonomy_scores.snapshot_id
        GROUP BY students.id
    ''').fetchall()
    
    conn .close()
    
    return jsonify([dict(row) for row in rows])
