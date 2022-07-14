import sqlite3

class UtilitiesAPI:
    def create_db():
        conn = sqlite3.connect('opensocial.db')

        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            account_email TEXT NOT NULL,
            account_password TEXT NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            account_status TEXT,
            access_token TEXT NOT NULL,
            phone_number INTEGER,
            account_level TEXT DEFAULT 'user',
            user_id TEXT NOT NULL
        )
        ''')

        conn.close()

    def checkToken(access_token):
        with sqlite3.connect('opensocial.db') as conn:
            cursor = conn.cursor()
            
            result = cursor.execute('SELECT id FROM Accounts WHERE access_token = (?)', [access_token]).fetchone()

            if result != None:
                return True
            else:
                return False
    
    def password_check(password):     
        if len(password) < 6 or len(password) > 20 or not any(char.isdigit() for char in password):
            return False
        else:
            return True