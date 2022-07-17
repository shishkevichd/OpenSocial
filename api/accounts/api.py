import re
import secrets

from werkzeug.security import generate_password_hash, check_password_hash
from api.utilities import UtilitiesAPI
from api.config import ConfigAPI
from datetime import datetime

class AccountAPI:
    def login(account_email, account_password):
        errors = [
            "incorrect_email_or_password"
        ]

        with UtilitiesAPI.connectdb(ConfigAPI.new_database) as conn:
            cursor = conn.cursor()

            result = cursor.execute('SELECT access_token, account_password, user_id FROM Accounts WHERE account_email = (?)', [account_email]).fetchone()

            if result == None:
                return UtilitiesAPI.errorJson(errors[0])
            else:
                if check_password_hash(pwhash=result[1], password=account_password):
                    return { "success": True, "data": { "access_token": result[0], "user_id": result[2] } }
                else:
                    return UtilitiesAPI.errorJson(errors[0])
    def register(account_email, account_password, first_name, last_name, gender):
        errors = [
            "incorrect_account_email",
            "incorrect_account_password",
            "incorrect_first_and_last_name",
            "incorrect_gender",
            "this_mail_already_exists"
        ]

        email_regex = r"^((\w[^\W]+)[\.\-]?){1,}\@(([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$"

        with UtilitiesAPI.connectdb(ConfigAPI.new_database) as conn:
            cursor = conn.cursor()

            check_is_email_exists = cursor.execute('SELECT id FROM Accounts WHERE account_email = (?)', [account_email]).fetchone()

            if check_is_email_exists == None:
                if bool(re.search(email_regex, account_email)):
                    if UtilitiesAPI.password_check(account_password):
                        if len(first_name) > 2 and len(last_name) > 2:
                            if int(gender) == 1 or int(gender) == 2:
                                result = cursor.execute(
                                    'INSERT INTO Accounts (account_email, account_password, first_name, last_name, access_token, user_id, gender, create_time) VALUES (?,?,?,?,?,?,?,?) RETURNING access_token, user_id', 
                                    (account_email, generate_password_hash(account_password), first_name, last_name, secrets.token_hex(20), secrets.token_hex(4), int(gender), str(datetime.utcnow()))
                                )

                                new_user_access_token = result.fetchone()

                                return { "success": True, "data": { "access_token": new_user_access_token[0], "user_id": new_user_access_token[1] } }
                            else:
                                return UtilitiesAPI.errorJson(errors[3])
                        else:
                            return UtilitiesAPI.errorJson(errors[2])
                    else:
                        return UtilitiesAPI.errorJson(errors[1])
                else:
                    return UtilitiesAPI.errorJson(errors[0])
            else:
                return UtilitiesAPI.errorJson(errors[4])
    def getUser(access_token, user_id=""):
        errors = [
            "incorrect_token",
            "user_not_found",
            "user_banned"
        ]

        if UtilitiesAPI.checkToken(access_token)['validToken']:
            with UtilitiesAPI.connectdb(ConfigAPI.new_database) as conn:
                cursor = conn.cursor()

                if user_id:
                    result = cursor.execute('SELECT user_id FROM Accounts WHERE user_id = (?)', [user_id]).fetchone()

                    if result != None:
                        return { "success": True, "data": UtilitiesAPI.getUserJSON(result[0]) }
                    else:
                        return UtilitiesAPI.errorJson(errors[1])
                else:
                    result = cursor.execute('SELECT user_id FROM Accounts WHERE access_token = (?)', [access_token]).fetchone()

                    return { "success": True, "data": UtilitiesAPI.getUserJSON(result[0], additional=True) }
        else:
            return UtilitiesAPI.errorJson(errors[0])
    def sendFriendRequest(access_token, target_friend_id):
        errors = [
            "incorrect_token",
            "user_not_found",
            "request_already_sent",
            "its_the_same_request",
            "cant_send_request_to_yourself"
        ]
        
        check_token = UtilitiesAPI.checkToken(access_token)

        if check_token['validToken']:
            with UtilitiesAPI.connectdb(ConfigAPI.new_database) as conn:
                cursor = conn.cursor()

                is_sent_request_to_yourself = cursor.execute('SELECT user_id FROM Accounts WHERE access_token = (?)', [access_token]).fetchone()

                if target_friend_id != is_sent_request_to_yourself[0]:
                    is_target_friend_avaliable = cursor.execute('SELECT id FROM Accounts WHERE user_id = (?)', [target_friend_id]).fetchone()

                    if is_target_friend_avaliable != None:
                        is_request_already_sent = cursor.execute('SELECT * FROM Friends WHERE first_friend = (?) AND second_friend = (?)', (check_token['id'], target_friend_id)).fetchone()

                        if is_request_already_sent != None:
                            return UtilitiesAPI.errorJson(errors[2])
                        else:
                            is_not_the_same_request = cursor.execute('SELECT * FROM Friends WHERE first_friend = (?) AND second_friend = (?)', (is_target_friend_avaliable[0], check_token['id'])).fetchone()

                            if is_not_the_same_request == None:
                                cursor.execute('INSERT INTO Friends(first_friend,second_friend,status) VALUES (?,?,?)', (check_token['id'], is_target_friend_avaliable[0], 'incoming'))

                                conn.commit()
                                cursor.close()

                                return { "status": True }
                            else:
                                return UtilitiesAPI.errorJson(errors[3])
                    else:
                        return UtilitiesAPI.errorJson(errors[1])
                else:
                    return UtilitiesAPI.errorJson(errors[4])
        else:
            return UtilitiesAPI.errorJson(errors[0])
    def acceptFriendRequest(access_token, user_id):
        errors = [
            "incorrect_token",
            "user_not_found",
            "cant_accept_request_to_yourself",
            "there_was_no_request"
        ]

        check_token = UtilitiesAPI.checkToken(access_token)

        if check_token['validToken']:
            with UtilitiesAPI.connectdb(ConfigAPI.new_database) as conn:
                cursor = conn.cursor()

                is_yourself = cursor.execute('SELECT user_id FROM Accounts WHERE access_token = (?)', [access_token]).fetchone()

                if is_yourself[0] != user_id:
                    is_user_avaliable = cursor.execute('SELECT id,user_id FROM Accounts WHERE user_id = (?)', [user_id]).fetchone()

                    if is_user_avaliable != None:
                        is_has_request = cursor.execute('SELECT status FROM Friends WHERE first_friend = (?) AND second_friend = (?)', (is_user_avaliable[0], check_token['id'])).fetchone()

                        if (is_has_request != None and is_has_request[0] == 'incoming') or (is_has_request != None and is_has_request[0] == 'declined'):
                            cursor.execute('UPDATE Friends SET status = (?) WHERE first_friend = (?) AND second_friend = (?)', ('accepted', is_user_avaliable[0], check_token['id']))

                            conn.commit()
                            cursor.close()

                            return { "status": True }
                        else:
                            return UtilitiesAPI.errorJson(errors[3])
                    else:
                        return UtilitiesAPI.errorJson(errors[1])
                else:
                    return UtilitiesAPI.errorJson(errors[2])
        else:
            return UtilitiesAPI.errorJson(errors[0])
    def declineFriendRequest(access_token, user_id):
        errors = [
            "incorrect_token",
            "user_not_found",
            "cant_decline_request_to_yourself",
            "there_was_no_request"
        ]

        check_token = UtilitiesAPI.checkToken(access_token)

        if check_token['validToken']:
            with UtilitiesAPI.connectdb(ConfigAPI.new_database) as conn:
                cursor = conn.cursor()

                is_yourself = cursor.execute('SELECT user_id FROM Accounts WHERE access_token = (?)', [access_token]).fetchone()

                if is_yourself[0] != user_id:
                    is_user_avaliable = cursor.execute('SELECT id,user_id FROM Accounts WHERE user_id = (?)', [user_id]).fetchone()

                    if is_user_avaliable != None:
                        is_has_request = cursor.execute('SELECT status FROM Friends WHERE first_friend = (?) AND second_friend = (?)', (is_user_avaliable[0], check_token['id'])).fetchone()

                        if is_has_request != None and is_has_request[0] == 'incoming':
                            cursor.execute('UPDATE Friends SET status = (?) WHERE first_friend = (?) AND second_friend = (?)', ('declined', is_user_avaliable[0], check_token['id']))

                            conn.commit()
                            cursor.close()

                            return { "status": True }
                        else:
                            return UtilitiesAPI.errorJson(errors[3])
                    else:
                        return UtilitiesAPI.errorJson(errors[1])
                else:
                    return UtilitiesAPI.errorJson(errors[2])
        else:
            return UtilitiesAPI.errorJson(errors[0])
    def deleteFriend(access_token, user_id):
        errors = [
            "incorrect_token",
            "user_not_found",
            "cant_decline_request_to_yourself",
            "friend_is_not_on_the_list"
        ]

        check_token = UtilitiesAPI.checkToken(access_token)

        if check_token['validToken']:
            with UtilitiesAPI.connectdb(ConfigAPI.new_database) as conn:
                cursor = conn.cursor()

                is_yourself = cursor.execute('SELECT user_id FROM Accounts WHERE access_token = (?)', [access_token]).fetchone()

                if is_yourself[0] != user_id:
                    is_user_avaliable = cursor.execute('SELECT id,user_id FROM Accounts WHERE user_id = (?)', [user_id]).fetchone()

                    if is_user_avaliable != None:
                        is_friend_in_friend_list = cursor.execute('SELECT id FROM Friends WHERE first_friend = (?) AND second_friend = (?)', (is_user_avaliable[0], check_token['id'])).fetchone()

                        if is_friend_in_friend_list != None:
                            cursor.execute("DELETE FROM Friends WHERE first_friend = (?) AND second_friend = (?)", (is_user_avaliable[0], check_token['id']))

                            conn.commit()
                            cursor.close()

                            return { "status": True }
                        else:
                            is_friend_in_friend_list_second = cursor.execute('SELECT id FROM Friends WHERE first_friend = (?) AND second_friend = (?)', (check_token['id'], is_user_avaliable[0])).fetchone()

                            if is_friend_in_friend_list_second != None:
                                cursor.execute("DELETE FROM Friends WHERE first_friend = (?) AND second_friend = (?)", (check_token['id'], is_user_avaliable[0]))

                                conn.commit()
                                cursor.close()

                                return { "status": True }
                            else:
                                return UtilitiesAPI.errorJson(errors[3])
                    else:
                        return UtilitiesAPI.errorJson(errors[1])
                else:
                    return UtilitiesAPI.errorJson(errors[2])
        else:
            return UtilitiesAPI.errorJson(errors[0])