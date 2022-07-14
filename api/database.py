import sqlite3

class DatabaseAPI:
    def create_db():
        conn = sqlite3.connect('opensocial.db')

        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Accounts (
            id int NOT NULL,
            account_email text NOT NULL,
            account_password text NOT NULL,
            first_name text NOT NULL,
            last_name text NOT NULL,
            account_status text NOT NULL,
            PRIMARY KEY(id)
        )
        ''')

        conn.close()