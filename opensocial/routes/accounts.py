from flask import Blueprint, request
from opensocial.api.accounts import Accounts
from opensocial.api.friends import Friends
from opensocial.api.messages import Dialogs


AccountsRAPI = Blueprint('Accounts', __name__, url_prefix='/users')


@AccountsRAPI.post('/login')
def AccountLogin():
    params = request.json
    return Accounts.login(params['email'], params['password'])


@AccountsRAPI.post('/reg')
@AccountsRAPI.post('/register')
def AccountRegister():
    params = request.json
    return Accounts.register(params['email'], params['password'], params['first_name'], params['last_name'], params['gender'])


@AccountsRAPI.post('/getUser')
def AccountGet():
    params = request.json
    return Accounts.getUser(params['access_token'], params['user_id'])

# Friends

@AccountsRAPI.post('/sendFriendRequest')
def AccountSendFriendRequestAPI():
    params = request.json
    return Friends.sendRequest(params['access_token'], params['user_id'])


@AccountsRAPI.post('/acceptFriendRequest')
def AccountAcceptFriendRequestAPI():
    params = request.json
    return Friends.acceptRequest(params['access_token'], params['user_id'])


@AccountsRAPI.post('/declineFriendRequest')
def AccountDeclineFriendRequestAPI():
    params = request.json
    return Friends.declineRequest(params['access_token'], params['user_id'])


@AccountsRAPI.post('/deleteFriend')
def AccountDeleteFriendAPI():
    params = request.json
    return Friends.deleteFromFriends(params['access_token'], params['user_id'])

# Posts

@AccountsRAPI.post('/getPosts')
def GetPostsAPI():
    params = request.json
    return Accounts.getUserPosts(params['access_token'], params['user_id'])


@AccountsRAPI.post('/createPost')
def CreatePostUserAPI():
    params = request.json
    return Accounts.createPost(params['access_token'], params['content'])


@AccountsRAPI.post('/deletePost')
def DeletePostUserAPI():
    params = request.json
    return Accounts.deletePost(params['access_token'], params['post_id'])


@AccountsRAPI.post('/editPost')
def EditPostUserAPI():
    params = request.json
    return Accounts.editPost(params['access_token'], params['post_id'], params['content'])


@AccountsRAPI.post('/getPostCompilation')
def GetPostCompilationAPI():
    params = request.json
    return Accounts.getPostCompilation(params['access_token'])

# Messages

@AccountsRAPI.post('/sendMessage')
def SendMessageAPI():
    params = request.json
    return Dialogs.sendMessageTo(params['access_token'], params['user_id'], params['content'])


@AccountsRAPI.post('/getDialog')
def GetDialogAPI():
    params = request.json
    return Dialogs.getDialog(params['access_token'], params['dialog_id'])


@AccountsRAPI.post('/getDialogs')
def GetDialogsAPI():
    params = request.json
    return Dialogs.getDialogs(params['access_token'])


@AccountsRAPI.post('/editMessage')
def EditMessageAPI():
    params = request.json
    return Dialogs.editMessage(params['access_token'], params['message_id'], params['content'])


@AccountsRAPI.post('/deleteMessage')
def DeleteMessageAPI():
    params = request.json
    return Dialogs.deleteMessage(params['access_token'], params['message_id'])