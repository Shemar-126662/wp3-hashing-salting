from flask import Blueprint, jsonify, render_template
from data.database import get_db_connection

student_bp = Blueprint('student', __name__)

@student_bp.route('/students/')
def students_list():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students ORDER BY name').fetchall()
    conn.close()
    return render_template('students_list.html', students=students)

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

    keyword_rows = conn.execute('''
        SELECT lgk.learning_goal_id, k.name AS keyword
        FROM learning_goal_keywords lgk
        JOIN keywords k ON k.id = lgk.keyword_id
        JOIN student_subjects ss ON ss.subject_id = (
            SELECT subject_id FROM learning_goals WHERE id = lgk.learning_goal_id
        )
        WHERE ss.student_id = ?
    ''', (student_id,)).fetchall()
    keywords_map = {}
    for row in keyword_rows:
        keywords_map.setdefault(row['learning_goal_id'], []).append(row['keyword'])
    
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
    
    return render_template('student_dashboard.html', student=student, subjects=subjects, learning_goals=learning_goals, progress_data=progress_data, keywords_map=keywords_map)

@student_bp.route('/api/students/<student_id>')
def api_student_dashboard(student_id):
    conn = get_db_connection()
    
    subjects = conn.execute('SELECT * FROM subjects').fetchall()
    
    learning_goals = conn.execute('SELECT * FROM learning_goals').fetchall()
    
    progress_data = conn.execute('''
        SELECT lg_id, AVG(avg_kennen) as avg_kennen, AVG(avg_kunnen) as avg_kunnen
        FROM (
            SELECT learning_goals.id as lg_id,
                   taxonomy_scores.kennen as avg_kennen,
                   taxonomy_scores.kunnen as avg_kunnen
            FROM learning_goals
            JOIN snapshots ON learning_goals.id = snapshots.learning_goal_id
            JOIN taxonomy_scores ON snapshots.id = taxonomy_scores.snapshot_id
        )
        GROUP BY lg_id
    ''').fetchall()
    
    conn.close()
    
    return jsonify({
        "subjects": [dict(s) for s in subjects],
        "learning_goals": [dict(g) for g in learning_goals],
        "progress_data": [dict(p) for p in progress_data]
    })
    
@student_bp.route('/students/<student_id>/learning-goal/<lg_id>')
def learning_goal_detail(student_id, lg_id):
        
    conn = get_db_connection()
        
    student = conn.execute('SELECT * FROM students WHERE id = ?', (student_id,)).fetchone()
    if student is None:
        return jsonify({"error": "Student not found"}), 404

    learning_goal = conn.execute('SELECT * FROM learning_goals WHERE id = ?', (lg_id,)).fetchone()
    if learning_goal is None:
        return jsonify({"error": "Learning goal not found"}), 404

    conn.close()

    return render_template('learning_goal_detail.html', student=student, learning_goal=learning_goal, lg_id=lg_id, student_id=student_id)

@student_bp.route('/api/students/<student_id>/learning-goal/<lg_id>')
def api_learning_goal_detail(student_id, lg_id):
    
    conn = get_db_connection()
    
    rows = conn.execute('''
        SELECT 
        snapshots.id,
        snapshots.date,
        taxonomy_scores.level,
        taxonomy_scores.kennen,
        taxonomy_scores.kunnen,
        taxonomy_scores.confidence
        FROM snapshots
        JOIN taxonomy_scores 
        ON snapshots.id = taxonomy_scores.snapshot_id
        WHERE snapshots.student_id = ?
        AND snapshots.learning_goal_id = ?
        AND snapshots.id = (
        SELECT id FROM snapshots
        WHERE student_id = ?
        AND learning_goal_id = ?
        ORDER BY date DESC
        LIMIT 1
        )
    ''', (student_id, lg_id, student_id, lg_id)).fetchall()
    
    conn.close()
    
    return jsonify([dict(row) for row in rows])

@student_bp.route('/students/<student_id>/snapshots')
def student_snapshots(student_id):
    return render_template('student_snapshots.html', student_id=student_id)

@student_bp.route('/api/students/<student_id>/snapshots')
def api_student_snapshots(student_id):
    conn = get_db_connection()
    
    rows = conn.execute('''
        SELECT 
            learning_goals.title,
            snapshots.source_type,
            snapshots.date,
            GROUP_CONCAT(DISTINCT keywords.name) as keywords,
            taxonomy_scores.level,
            AVG((taxonomy_scores.kennen + taxonomy_scores.kunnen + taxonomy_scores.confidence) / 3.0) as avg_score
        FROM snapshots
        JOIN learning_goals ON snapshots.learning_goal_id = learning_goals.id
        JOIN taxonomy_scores ON snapshots.id = taxonomy_scores.snapshot_id
        LEFT JOIN learning_goal_keywords lgk ON learning_goals.id = lgk.learning_goal_id
        LEFT JOIN keywords ON keywords.id = lgk.keyword_id
        WHERE snapshots.student_id = ?
        AND snapshots.id IN (
        SELECT id FROM snapshots
        WHERE student_id = ?
        ORDER BY date DESC
        LIMIT 100
        )
        GROUP BY snapshots.id, taxonomy_scores.level
    ''', (student_id, student_id)).fetchall()
    
    conn.close()
    
    return jsonify([dict(row) for row in rows])
        
        

