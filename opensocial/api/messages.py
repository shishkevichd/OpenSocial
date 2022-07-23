from datetime import datetime
from peewee import *
from opensocial.model import BaseModel
from opensocial.api.accounts import Accounts


class Dialogs(BaseModel):
    id = IntegerField(primary_key=True)
    sender = ForeignKeyField(Accounts)
    receiver = ForeignKeyField(Accounts)
    dialog_id = CharField(10)

    def getMessages(self):
        return self.messages


class Messages(BaseModel):
    id = IntegerField(primary_key=True)
    sender = ForeignKeyField(Accounts)
    content = CharField(2048),
    send_date = DateTimeField(default=datetime.utcnow)
    is_edited = BooleanField(default=False)
    edited_time = DateTimeField(default=None)
    to_dialog = ForeignKeyField(Dialogs, backref="messages")

    def getJSON(self):
        jsonObject = {
            "sender_id": self.sender.user_id,
            "content": self.content,
            "date": self.send_date
        }

        if self.is_edited:
            jsonObject['editData'] = {
                "isEdited": True,
                "editTime": self.edited_time
            }
        
        return jsonObject