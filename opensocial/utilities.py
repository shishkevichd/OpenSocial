from peewee import *
from opensocial.model import database


class UtilitiesAPI:
    def create_db():
        from opensocial.api.accounts import Accounts
        from opensocial.api.friends import Friends
        from opensocial.api.notes import Notes 
        from opensocial.api.groups import Groups 
        from opensocial.api.subscribers import Subscribers 
        from opensocial.api.posts import Posts 
        from opensocial.api.messages import Dialogs, Messages

        with database:
            database.create_tables([Accounts, Friends, Notes, Groups, Subscribers, Posts, Dialogs, Messages])

    def errorJson(reason):
        return { "status": False, "why": reason }, 400
    
    def password_check(password):     
        if len(password) < 6 or len(password) > 20 or not any(char.isdigit() for char in password):
            return False
        else:
            return True