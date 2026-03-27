
from flask import Blueprint, render_template, request, redirect, session
from data.database import get_db_connection

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()

        user = conn.execute(
            'SELECT * FROM users WHERE email = ? AND password = ?',
            (email, password)
        ).fetchone()

        if user:
            session['user_id'] = user['id']
            session['role'] = user['role']
            session['email'] = user['email']
            session['name'] = user['name']

            if user['role'] == 'student':
                student = conn.execute(
                    'SELECT id FROM students WHERE user_id = ?',
                    (user['id'],)
                ).fetchone()
                if student:
                    session['student_id'] = student['id']

            if user['role'] == 'teacher':
                conn.close()
                return redirect('/teacher')
            else:
                student = conn.execute(
                    'SELECT id FROM students WHERE user_id = ?',
                    (user['id'],)
                ).fetchone()

                conn.close()

                if student:
                    return redirect(f"/students/{student['id']}")
                else:
                    return "Student niet gevonden", 404

        conn.close()
        return "Login mislukt"

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/login')