"""Eenmalige migratie van de oude SQLite-database met fictieve accounts.

Stop de app voor gebruik. Bewaar oude kopieën met plaintext niet bij de inlevering.
"""
from data.database import get_db_connection
from security import hash_password


def migrate_passwords():
    conn = get_db_connection()
    try:
        columns = {row['name'] for row in conn.execute('PRAGMA table_info(users)')}
        if 'password' not in columns:
            return 0
        # secure_delete overschrijft verwijderde inhoud in dit databasebestand.
        conn.execute('PRAGMA secure_delete = ON')
        with conn:
            conn.execute('BEGIN')
            conn.execute('ALTER TABLE users ADD COLUMN password_hash TEXT')
            rows = conn.execute('SELECT id, password FROM users').fetchall()
            for row in rows:
                if not isinstance(row['password'], str):
                    raise ValueError('Account zonder geldig wachtwoord; reset vereist')
                conn.execute('UPDATE users SET password_hash = ? WHERE id = ?',
                             (hash_password(row['password']), row['id']))
            conn.execute('ALTER TABLE users DROP COLUMN password')
        conn.execute('VACUUM')
        return len(rows)
    finally:
        conn.close()


if __name__ == '__main__':
    print(f"Migratie klaar: {migrate_passwords()} accounts omgezet.")
