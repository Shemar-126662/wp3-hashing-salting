from flask import Blueprint, jsonify, render_template
from data.database import get_db_connection

teacher_bp = Blueprint('teacher', __name__)


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

@teacher_bp.route('/teacher')
def teacher_dashboard():
    conn = get_db_connection()
    
    students = conn.execute('SELECT * FROM students').fetchall()
    
    avg_rows = conn.execute('''
        SELECT AVG(( kennen + kunnen ) / 2.0) as avg_score FROM taxonomy_scores
    ''').fetchone()
    
    average_score = 0
    if avg_rows["avg_score"]:
        average_score = round(avg_rows["avg_score"] * 100)
    
    weak_rows = conn.execute('''
        SELECT level, AVG((kennen + kunnen) / 2.0) as avg_score
        FROM taxonomy_scores
        GROUP BY level
        ORDER BY avg_score ASC
        LIMIT 2
    ''').fetchall()
    
    weak_areas = [row["level"] for row in weak_rows]
    
    conn.close()
    return render_template('teacher_dashboard.html',students=students, average_score=average_score, weak_areas=weak_areas)

@teacher_bp.route('/teacher/analysis')
def teacher_analysis():
    conn = get_db_connection()
    
    rows = conn.execute('''
        SELECT
            learning_goals.title,
            AVG(( kennen + kunnen ) / 2.0) as avg_score
        FROM learning_goals
        JOIN snapshots ON learning_goals.id = snapshots.learning_goal_id
        JOIN taxonomy_scores ON snapshots.id = taxonomy_scores.snapshot_id
        GROUP BY learning_goals.id
    ''').fetchall()
    
    conn.close()
    
    return render_template('teacher_analysis.html', learning_goals=rows)

@teacher_bp.route('/api/class-learning-goals')
def api_class_learning_goals():
    conn = get_db_connection()
    
    rows = conn.execute('''
        SELECT
            learning_goals.id,
            learning_goals.title,
            AVG(( kennen + kunnen ) / 2.0) as avg_score
        FROM learning_goals
        JOIN snapshots ON learning_goals.id = snapshots.learning_goal_id
        JOIN taxonomy_scores ON snapshots.id = taxonomy_scores.snapshot_id
        GROUP BY learning_goals.id
    ''').fetchall()
    
    conn.close()
    
    return jsonify([dict(row) for row in rows])
