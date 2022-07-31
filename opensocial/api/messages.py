from datetime import datetime
from opensocial.utilities import UtilitiesAPI
import secrets
from peewee import *
from opensocial.model import BaseModel
from opensocial.api.accounts import Accounts


class Dialogs(BaseModel):
    id = IntegerField(primary_key=True)
    sender = ForeignKeyField(Accounts)
    receiver = ForeignKeyField(Accounts)
    dialog_id = CharField(10)

    # ===================================
    # Gets
    # ===================================

    def getMessages(self):
        return Messages.select().where(Messages.to_dialog == self).order_by(Messages.send_date.asc())

    def getLastMessage(self):
        return Messages.select().where(Messages.to_dialog == self).order_by(Messages.send_date.desc()).first()

    def getRecipient(self, access_token):
        if Accounts.isValidAccessToken(access_token):
            if self.sender == Accounts.get(Accounts.access_token == access_token):
                return self.receiver
            else:
                return self.sender
        else:
            return None

    def getJSON(self, access_token, advanced=False):
        jsonObject = {
            "chat_with": self.getRecipient(access_token=access_token).getJSON(),
            "id": self.dialog_id
        }

        if advanced:
            messages_array = []

            for message in self.getMessages():
                messages_array.append(message.getJSON())

            jsonObject['messages'] = messages_array
        else:
            jsonObject['last_message'] = self.getLastMessage().getJSON()

        return jsonObject

    def getDialog(access_token, dialog_id):
        getDialogErrors = [
            'invalid_token',
            'dialog_not_found'
        ]

        if Accounts.isValidAccessToken(access_token):
            target_dialog = Dialogs.get_or_none(Dialogs.dialog_id == dialog_id)

            if target_dialog != None:
                return {
                    'success': True,
                    'data': target_dialog.getJSON(advanced=True, access_token=access_token)
                }
            else:
                return UtilitiesAPI.errorJson(getDialogErrors[1])
        else:
            return UtilitiesAPI.errorJson(getDialogErrors[0])

    def getDialogs(access_token):
        getDialogsErrors = [
            'invalid_token',
            'dialogs_empty'
        ]

        if Accounts.isValidAccessToken(access_token):
            user_dialogs = Dialogs.select().where((Dialogs.sender == Accounts.get(Accounts.access_token == access_token)) | (Dialogs.receiver == Accounts.get(Accounts.access_token == access_token)))

            if user_dialogs.exists():
                user_dialogs_array = []

                for dialog in user_dialogs:
                    user_dialogs_array.append(dialog.getJSON(advanced=False, access_token=access_token))

                return {
                    'success': True,
                    'data': user_dialogs_array
                }
            else:
                return UtilitiesAPI.errorJson(getDialogsErrors[1])
        else:
            return UtilitiesAPI.errorJson(getDialogsErrors[0])
    
    # ===================================
    # Message manage
    # ===================================

    def deleteMessage(access_token, message_id):
        deleteMessageErrors = [
            'invalid_token',
            'message_not_found'
        ]

        if Accounts.isValidAccessToken(access_token):
            target_message = Messages.get_or_none((Messages.sender == Accounts.get(Accounts.access_token == access_token)) & (Messages.message_id == message_id))

            if target_message != None:
                target_message.deleteMessage()

                return {
                    'success': True
                }
            else:
                return UtilitiesAPI.errorJson(deleteMessageErrors[1])
        else:
            return UtilitiesAPI.errorJson(deleteMessageErrors[0])

    def editMessage(access_token, message_id, content):
      editMessageErrors = [
        'invalid_token',
        'message_not_found',
        'short_content'
      ]
     
      if Accounts.isValidAccessToken(access_token):
        target_message = Messages.get_or_none((Messages.sender == Accounts.get(Accounts.access_token == access_token)) & (Messages.message_id == message_id))

        if target_message != None:
            if len(content) >= 1 & len(content) < 2048:
                target_message.is_edited = True
                target_message.edited_time = datetime.utcnow()
                target_message.content = content

                target_message.save()

                return {
                    'success': True
                }
            else:
                return UtilitiesAPI.errorJson(editMessageErrors[2])
        else:
            return UtilitiesAPI.errorJson(editMessageErrors[1])
      else:
        return UtilitiesAPI.errorJson(editMessageErrors[0])

    def sendMessageTo(access_token, user_id, messageContent):
        sendMessageErrors = [
            'invalid_token',
            'user_not_found',
            'short_message'
        ]

        if Accounts.isValidAccessToken(access_token):
            target_user = Accounts.get_or_none(
                Accounts.user_id == user_id
            )

            if target_user != None:
                if len(messageContent) >= 1:
                    target_dialog = Dialogs.select().where(
                        ((Dialogs.sender == Accounts.get(Accounts.access_token == access_token)) & (Dialogs.receiver == target_user)) | ((Dialogs.sender == target_user) & (Dialogs.receiver == Accounts.get(Accounts.access_token == access_token)))
                    )

                    if target_dialog.exists():
                        Messages.create(
                            sender=Accounts.get(Accounts.access_token == access_token),
                            content=messageContent,
                            to_dialog=target_dialog.first(),
                            message_id=secrets.token_hex(8)
                        )

                        return {
                            'success': True
                        }
                    else:
                        new_dialog_id = secrets.token_hex(5)
                        
                        Dialogs.create(
                            sender=Accounts.get(Accounts.access_token == access_token),
                            receiver=target_user,
                            dialog_id=new_dialog_id
                        )

                        Messages.create(
                            sender=Accounts.get(Accounts.access_token == access_token),
                            content=messageContent,
                            to_dialog=Dialogs.get(Dialogs.dialog_id == new_dialog_id),
                            message_id=secrets.token_hex(8)
                        )

                        return {
                            'success': True
                        }
                else:
                    return UtilitiesAPI.errorJson(sendMessageErrors[2])
            else:
                return UtilitiesAPI.errorJson(sendMessageErrors[1])
        else:
            return UtilitiesAPI.errorJson(sendMessageErrors[0])


class Messages(BaseModel):
    id = IntegerField(primary_key=True)
    sender = ForeignKeyField(Accounts)
    content = CharField(2048)
    send_date = DateTimeField(default=datetime.utcnow)
    is_edited = BooleanField(default=False, null=True)
    edited_time = DateTimeField(default=None, null=True)
    to_dialog = ForeignKeyField(Dialogs, backref="messages")
    message_id = CharField(16)

    # ===================================
    # Gets
    # ===================================

    def getJSON(self):
        jsonObject = {
            "sender": self.sender.getJSON(),
            "content": self.content,
            "date": self.send_date,
            "id": self.message_id
        }

        if self.is_edited:
            jsonObject['editData'] = {
                "isEdited": True,
                "editTime": self.edited_time
            }
        
        return jsonObject

    # ===================================
    # Message manage
    # ===================================

    def deleteMessage(self):
        return self.delete_instance()