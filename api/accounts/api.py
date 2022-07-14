import sqlite3
import re
import secrets

from werkzeug.security import generate_password_hash, check_password_hash
from api.utilities import UtilitiesAPI

class AccountAPI:
    def login(account_email, account_password):
        errors = [
            "incorrect_email_or_password"
        ]

        with sqlite3.connect('opensocial.db') as conn:
            cursor = conn.cursor()

            result = cursor.execute('SELECT access_token, account_password, user_id FROM Accounts WHERE account_email = (?)', [account_email]).fetchone()

            if result == None:
                return { "success": False, "why": errors[0] }, 403
            else:
                if check_password_hash(pwhash=result[1], password=account_password):
                    return { "success": True, "data": { "access_token": result[0], "user_id": result[2] } }
                else:
                    return { "success": False, "why": errors[0] }, 403
    def register(account_email, account_password, first_name, last_name):
        errors = [
            "incorrect_account_email",
            "incorrect_account_password",
            "incorrect_first_and_last_name",
            "this_mail_already_exists"
        ]

        email_regex = r"^((\w[^\W]+)[\.\-]?){1,}\@(([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$"

        with sqlite3.connect('opensocial.db') as conn:
            cursor = conn.cursor()

            check_is_email_exists = cursor.execute('SELECT id FROM Accounts WHERE account_email = (?)', [account_email]).fetchone()

            if check_is_email_exists == None:
                if bool(re.search(email_regex, account_email)):
                    if UtilitiesAPI.password_check(account_password):
                        if len(first_name) > 2 and len(last_name) > 2:
                            result = cursor.execute('INSERT INTO Accounts (account_email, account_password, first_name, last_name, access_token, user_id) VALUES (?,?,?,?,?,?) RETURNING access_token, user_id', (account_email, generate_password_hash(account_password), first_name, last_name, secrets.token_hex(20), secrets.token_hex(4)))

                            new_user_access_token = result.fetchone()

                            return { "success": True, "data": { "access_token": new_user_access_token[0], "user_id": new_user_access_token[1] } }
                        else:
                            return { "success": False, "why": errors[2] }, 400
                    else:
                        return { "success": False, "why": errors[1] }, 400
                else:
                    return { "success": False, "why": errors[0] }, 400
            else:
                return { "success": False, "why": errors[3] }, 403
    def getUser(access_token, user_id=""):
        errors = [
            "incorrect_token",
            "user_not_found",
            "user_banned"
        ]

        if UtilitiesAPI.checkToken(access_token):
            with sqlite3.connect('opensocial.db') as conn:
                cursor = conn.cursor()

                if user_id:
                    result = cursor.execute('SELECT * FROM Accounts WHERE user_id = (?)', [user_id]).fetchone()

                    if result != None:
                        return { "success": True, "data": { "first_name": result[3], "last_name": result[4], "status": result[5], "user_id": result[9] } }
                    else:
                        return { "success": False, "why": errors[1] }, 403
                else:
                    result = cursor.execute('SELECT * FROM Accounts WHERE access_token = (?)', [access_token]).fetchone()

                    return { "success": True, "data": { "first_name": result[3], "last_name": result[4], "status": result[5], "user_id": result[9] } }
        else:
            return { "success": False, "why": errors[0] }, 403
