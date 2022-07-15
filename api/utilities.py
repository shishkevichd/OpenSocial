import sqlite3

from api.config import ConfigAPI


class UtilitiesAPI:
    def create_db():
        conn = sqlite3.connect(ConfigAPI.database)

        cursor = conn.cursor()
        
        cursor.executescript('''
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
            user_id TEXT NOT NULL,
            gender INTEGER,
            birthday TEXT
        );

        CREATE TABLE IF NOT EXISTS Notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            content TEXT NOT NULL,
            creator INTEGER NOT NULL,
            date INTEGER NOT NULL,
            note_id TEXT NOT NULL,
            is_edited INT DEFAULT 0,
            FOREIGN KEY(creator) REFERENCES Accounts(id)
        );

        CREATE TABLE IF NOT EXISTS Friends (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            first_friend INTEGER NOT NULL,
            second_friend INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'incoming',
            FOREIGN KEY(first_friend) REFERENCES Accounts(id)
            FOREIGN KEY(second_friend) REFERENCES Accounts(id)
        )
        ''')

        conn.close()

    def checkToken(access_token):
        with sqlite3.connect(ConfigAPI.database) as conn:
            cursor = conn.cursor()
            
            result = cursor.execute('SELECT id FROM Accounts WHERE access_token = (?)', [access_token]).fetchone()

            if result != None:
                return { "validToken": True, "id": result[0] }
            else:
                return { "validToken": False }

    def getUserJSON(user_id, additional=False):
        with sqlite3.connect(ConfigAPI.database) as conn:
            cursor = conn.cursor()
            
            result = cursor.execute('SELECT * FROM Accounts WHERE user_id = (?)', [user_id]).fetchone()

            if result != None:
                if additional:
                    return { "first_name": result[3], "last_name": result[4], "status": result[5], "user_id": result[9], "phone_number": result[7], "gender": result[10] }
                else:
                    return { "first_name": result[3], "last_name": result[4], "status": result[5], "user_id": result[9], "gender": result[10] }
            else:
                return None

    def errorJson(reason):
        return { "status": False, "why": reason }, 400
    
    def password_check(password):     
        if len(password) < 6 or len(password) > 20 or not any(char.isdigit() for char in password):
            return False
        else:
            return True