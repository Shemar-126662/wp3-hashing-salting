from flask import Blueprint, render_template
from data.database import get_db_connection

student_bp = Blueprint('student', __name__)

@student_bp.route('/students/<student_id>')
def student_dashboard(student_id):
    conn = get_db_connection()
    
    student = conn.execute('SELECT * FROM students WHERE id = ?', (student_id,)).fetchone()
    if student is None:
        return "Student not found", 404
    
    subjects = conn.execute('''
        SELECT subjects.* FROM subjects subjects JOIN student_subjects ON subjects.id = student_subjects.subject_id
        WHERE student_subjects.student_id = ?
    ''', (student_id,)).fetchall()
    
    learning_goals = conn.execute('''
        SELECT learning_goals.* FROM learning_goals JOIN student_subjects ON learning_goals.subject_id = student_subjects.subject_id
        WHERE student_subjects.student_id = ?
    ''', (student_id,)).fetchall()
    
  
    progress_data = conn.execute('''
        SELECT 
            learning_goals.id as lg_id,
            AVG(taxonomy_scores.kennen) as avg_kennen,
            AVG(taxonomy_scores.kunnen) as avg_kunnen
        FROM learning_goals
        JOIN snapshots ON learning_goals.id = snapshots.learning_goal_id
        JOIN taxonomy_scores ON snapshots.id = taxonomy_scores.snapshot_id
        JOIN student_subjects ON learning_goals.subject_id = student_subjects.subject_id
        WHERE student_subjects.student_id = ?
        GROUP BY learning_goals.id
    ''', (student_id,)).fetchall()
    progress_data = [dict(row) for row in progress_data]

    
    
    conn.close()
    
    return render_template('student_dashboard.html', student=student, subjects=subjects, learning_goals=learning_goals, progress_data=progress_data)



