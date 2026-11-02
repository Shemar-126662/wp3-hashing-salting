import contextlib
import io
import json
import os
from pathlib import Path
import sqlite3
import tempfile
import time
import unittest

from flask import Flask
from data import database
from import_data import import_data
from migrate_passwords import migrate_passwords
from routes.auth_routes import auth_bp
from security import hash_password, verify_password


class PasswordTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.old_database = database.DATABASE
        database.DATABASE = str(Path(self.temp.name) / 'test.db')
        self.app = Flask(__name__, template_folder=str(Path(__file__).resolve().parents[1] / 'templates'))
        self.app.secret_key = 'test-only'
        self.app.register_blueprint(auth_bp)
        self.client = self.app.test_client()

    def tearDown(self):
        database.DATABASE = self.old_database
        self.temp.cleanup()

    def test_salts_and_verification(self):
        first = hash_password('fictief-testwachtwoord')
        second = hash_password('fictief-testwachtwoord')
        self.assertNotEqual(first, second)
        self.assertNotEqual(first.split('$')[4], second.split('$')[4])
        self.assertTrue(first.startswith('$argon2id$'))
        self.assertTrue(verify_password(first, 'fictief-testwachtwoord'))
        self.assertFalse(verify_password(first, 'verkeerd'))
        self.assertFalse(verify_password('kapotte-hash', 'test'))

    def test_import_and_login(self):
        database.init_db()
        # Geen leerresultaten nodig om de fictieve docentaccounts te importeren.
        sample = Path(self.temp.name) / 'data-sample.json'
        sample.write_text(json.dumps({'entries': []}))
        previous = os.getcwd()
        output = io.StringIO()
        try:
            os.chdir(self.temp.name)
            with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
                import_data()
        finally:
            os.chdir(previous)
        with sqlite3.connect(database.DATABASE) as conn:
            columns = {row[1] for row in conn.execute('PRAGMA table_info(users)')}
            hashes = [r[0] for r in conn.execute('SELECT password_hash FROM users')]
        self.assertNotIn('password', columns)
        self.assertEqual(len(hashes), 4)
        self.assertTrue(all(h.startswith('$argon2id$') for h in hashes))
        for wrong_email, password in [('louella@admin.com', 'fout'), ('onbekend@test.com', 'louella123')]:
            response = self.client.post('/login', data={'email': wrong_email, 'password': password})
            self.assertEqual(response.status_code, 401)
            with self.client.session_transaction() as session:
                self.assertNotIn('user_id', session)
        start = time.perf_counter()
        response = self.client.post('/login', data={'email': 'louella@admin.com', 'password': 'louella123'})
        print(f'Juiste login: {(time.perf_counter() - start) * 1000:.0f} ms')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, '/teacher')
        with self.client.session_transaction() as session:
            self.assertIn('user_id', session)
        self.assertNotIn('louella123', output.getvalue())
        self.assertNotIn(b'louella123', Path(database.DATABASE).read_bytes())

    def test_register_and_student_login(self):
        database.init_db()
        self.assertEqual(self.client.get('/register').status_code, 200)
        with self.client.session_transaction() as session:
            token = session['register_token']
        data = {'name': 'Fictieve student', 'email': 'nieuw@test.com',
                'password': 'nieuw-testwachtwoord', 'token': token, 'role': 'teacher'}
        self.assertEqual(self.client.post('/register', data={**data, 'token': 'fout'}).status_code, 400)
        self.assertEqual(self.client.post('/register', data=data).status_code, 302)
        with sqlite3.connect(database.DATABASE) as conn:
            value, role = conn.execute('SELECT password_hash, role FROM users').fetchone()
        self.assertTrue(verify_password(value, data['password']))
        self.assertEqual(role, 'student')
        response = self.client.post('/login', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.location.startswith('/students/'))
        with self.client.session_transaction() as session:
            self.assertIn('student_id', session)
        self.assertNotIn(data['password'].encode(), Path(database.DATABASE).read_bytes())

    def test_migration_preserves_accounts_and_is_repeatable(self):
        with sqlite3.connect(database.DATABASE) as conn:
            conn.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT UNIQUE, password TEXT, role TEXT)')
            conn.execute("INSERT INTO users VALUES (7, 'Test', 'test@test.com', 'fictief-oud-wachtwoord', 'teacher')")
        self.assertEqual(migrate_passwords(), 1)
        self.assertEqual(migrate_passwords(), 0)
        database.init_db()
        with sqlite3.connect(database.DATABASE) as conn:
            self.assertNotIn('password', {r[1] for r in conn.execute('PRAGMA table_info(users)')})
            user_id, value = conn.execute('SELECT id, password_hash FROM users').fetchone()
        self.assertEqual(user_id, 7)
        self.assertTrue(verify_password(value, 'fictief-oud-wachtwoord'))
        self.assertNotIn(b'fictief-oud-wachtwoord', Path(database.DATABASE).read_bytes())
        response = self.client.post('/login', data={'email': 'test@test.com', 'password': 'fictief-oud-wachtwoord'})
        self.assertEqual(response.status_code, 302)


if __name__ == '__main__':
    unittest.main()
