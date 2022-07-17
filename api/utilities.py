from peewee import *
from playhouse.db_url import connect
from api.config import ConfigAPI


class UtilitiesAPI:
    def create_db():
        with open('./api/sql/create_tables.sql', 'r') as file:
            conn = UtilitiesAPI.connectdb(ConfigAPI.new_database)

            cursor = conn.cursor()
            cursor.executescript(file.read())

            conn.close()

    def checkToken(access_token):
        with UtilitiesAPI.connectdb(ConfigAPI.new_database) as conn:
            cursor = conn.cursor()
            
            result = cursor.execute('SELECT id FROM Accounts WHERE access_token = (?)', [access_token]).fetchone()

            if result != None:
                return { "validToken": True, "id": result[0] }
            else:
                return { "validToken": False }

    def connectdb(config):
        return connect(config)

    def getUserJSON(user_id, additional=False):
        with UtilitiesAPI.connectdb(ConfigAPI.new_database) as conn:
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