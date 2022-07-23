from flask import Blueprint, request
from opensocial.api.accounts import Accounts
from opensocial.api.friends import Friends


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