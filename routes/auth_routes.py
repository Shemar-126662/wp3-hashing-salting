
import secrets
import sqlite3
from hmac import compare_digest

from flask import Blueprint, render_template, request, redirect, session
from data.database import get_db_connection
from security import hash_password, password_hasher, verify_password

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        conn = get_db_connection()

        user = conn.execute(
            'SELECT * FROM users WHERE email = ?',
            (email,)
        ).fetchone()

        if user and verify_password(user['password_hash'], password):
            if password_hasher.check_needs_rehash(user['password_hash']):
                conn.execute('UPDATE users SET password_hash = ? WHERE id = ?',
                             (password_hasher.hash(password), user['id']))
                conn.commit()
            session.clear()
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
        return "Login mislukt", 401

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if 'register_token' not in session:
        session['register_token'] = secrets.token_urlsafe(32)
    if request.method == 'GET':
        return render_template('register.html', token=session['register_token'])
    token = request.form.get('token', '')
    if not compare_digest(token, session['register_token']):
        return 'Ongeldig formulier', 400
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip().lower()
    password = request.form.get('password', '')
    if not name or len(name) > 100 or '@' not in email or len(email) > 254 or not 12 <= len(password) <= 1024:
        return 'Vul een naam, e-mailadres en wachtwoord van 12 tot 1024 tekens in', 400
    conn = get_db_connection()
    try:
        with conn:
            cursor = conn.execute(
                'INSERT INTO users (name, email, password_hash, role) VALUES (?, ?, ?, ?)',
                (name, email, hash_password(password), 'student'))
            conn.execute('INSERT INTO students (user_id, name) VALUES (?, ?)',
                         (cursor.lastrowid, name))
    except sqlite3.IntegrityError:
        return 'Account kan niet worden aangemaakt', 400
    finally:
        conn.close()
    session.pop('register_token', None)
    return redirect('/login')
