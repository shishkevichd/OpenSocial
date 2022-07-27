from flask import Blueprint, request
from opensocial.api.messages import Dialogs


MessagesRAPI = Blueprint('Messages', __name__, url_prefix='/messages')


@MessagesRAPI.post('/sendMessage')
def SendMessageAPI():
    params = request.json
    return Dialogs.sendMessageTo(params['access_token'], params['user_id'], params['content'])


@MessagesRAPI.post('/getDialog')
def GetDialogAPI():
    params = request.json
    return Dialogs.getDialog(params['access_token'], params['dialog_id'])


@MessagesRAPI.post('/getDialogs')
def GetDialogsAPI():
    params = request.json
    return Dialogs.getDialogs(params['access_token'])


@MessagesRAPI.post('/editMessage')
def EditMessageAPI():
    params = request.json
    return Dialogs.editMessage(params['access_token'], params['message_id'], params['content'])


@MessagesRAPI.post('/deleteMessage')
def DeleteMessageAPI():
    params = request.json
    return Dialogs.deleteMessage(params['access_token'], params['message_id'])