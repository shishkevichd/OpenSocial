from datetime import datetime
from opensocial.model import BaseModel
from peewee import *
from werkzeug.security import generate_password_hash, check_password_hash
from opensocial.utilities import UtilitiesAPI

import re
import secrets


class Accounts(BaseModel):
    id = IntegerField(primary_key=True)
    email = CharField(max_length=50, null=False)
    password = TextField(null=False)
    first_name = CharField(max_length=50, null=False)
    last_name = CharField(max_length=50, null=False)
    join_date = DateTimeField(default=datetime.now)
    birthday = DateField(null=True)
    user_id = CharField(max_length=12)
    gender = IntegerField(null=False)
    access_token = TextField(null=False)

    def isValidAccessToken(target_access_token):
        requested_user = Accounts.get_or_none(Accounts.access_token == target_access_token)

        if requested_user == None:
            return False
        else:
            return True

    def getJSON(self, advanced=False):
        json_object = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'gender': 'man' if self.gender == 2 else "women",
            'user_id': self.user_id
        }
        if advanced:
            json_object['join_date'] = self.join_date
            json_object['email'] = self.email

        return json_object

    def getUser(access_token, user_id):
        getUserErrors = [
            "invalid_token",
            "user_not_found"
        ]

        if Accounts.isValidAccessToken(access_token):
            if user_id:
                requested_user = Accounts.get(Accounts.user_id == user_id)
            
                if requested_user == None:
                    return UtilitiesAPI.errorJson(getUserErrors[1])
                else:
                    return requested_user.getJSON()
            else:
                return Accounts.get(Accounts.access_token == access_token).getJSON(advanced=True)
        else:
            return UtilitiesAPI.errorJson(getUserErrors[0])

    def login(user_email, user_password):
        loginErrors = [
            "incorrect_password_or_email"
        ]

        searchable_user = Accounts.get_or_none(Accounts.email == user_email)

        if searchable_user != None:
            if check_password_hash(searchable_user.password, user_password):
                return {
                    'success': True,
                    'data': {
                        'access_token': searchable_user.access_token,
                        'user_id': searchable_user.user_id
                    }
                }  
            else:
                return UtilitiesAPI.errorJson(loginErrors[0])
        else:
            return UtilitiesAPI.errorJson(loginErrors[0])

    def register(user_email, user_password, first_name, last_name, gender):
        registerErrors = [
            "incorrect_account_email",
            "incorrect_account_password",
            "incorrect_first_and_last_name",
            "incorrect_gender",
            "this_mail_already_exists"
        ]

        email_regex = r"^((\w[^\W]+)[\.\-]?){1,}\@(([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$"
        
        is_email_already_exists = Accounts.get_or_none(Accounts.email == user_email)

        if is_email_already_exists == None:
            if bool(re.search(email_regex, user_email)):
                if UtilitiesAPI.password_check(user_password):
                    if len(first_name) > 2 and len(last_name) > 2:
                        if int(gender) == 1 or int(gender) == 2:
                            new_user_id = secrets.token_hex(8)
                            
                            Accounts.create(
                                email=user_email, 
                                password=generate_password_hash(user_password), 
                                first_name=first_name,
                                last_name=last_name,
                                gender=gender,
                                access_token=secrets.token_hex(24),
                                user_id=new_user_id
                            )

                            new_user = Accounts.get(Accounts.user_id == new_user_id)

                            return {
                                'success': True,
                                'data': {
                                    'access_token': new_user.access_token,
                                    'user_id': new_user.user_id
                                }
                            }
                        else:
                            return UtilitiesAPI.errorJson(registerErrors[3])
                    else:
                        return UtilitiesAPI.errorJson(registerErrors[2])
                else:
                    return UtilitiesAPI.errorJson(registerErrors[1])
            else:
                return UtilitiesAPI.errorJson(registerErrors[0])
        else:
            return UtilitiesAPI.errorJson(registerErrors[4])

