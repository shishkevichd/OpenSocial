from flask import Blueprint, request
from api.accounts.api import AccountAPI


AccountRoutesAPI = Blueprint("AccountAPI", __name__, url_prefix='/accounts')


@AccountRoutesAPI.post('/login')
def AccountLoginAPI():
    params = request.json
    return AccountAPI.login(params['email'], params['password'])


@AccountRoutesAPI.post('/register')
def AccountRegisterAPI():
    params = request.json
    return AccountAPI.register(params['email'], params['password'], params['first_name'], params['last_name'], params['gender'])


@AccountRoutesAPI.post('/getUser')
def AccountGetUserAPI():
    params = request.json
    return AccountAPI.getUser(params['access_token'], params['user_id'])


@AccountRoutesAPI.post('/sendFriendRequest')
def AccountSendFriendRequestAPI():
    params = request.json
    return AccountAPI.sendFriendRequest(params['access_token'], params['user_id'])


@AccountRoutesAPI.post('/acceptFriendRequest')
def AccountAcceptFriendRequestAPI():
    params = request.json
    return AccountAPI.acceptFriendRequest(params['access_token'], params['user_id'])


@AccountRoutesAPI.post('/declineFriendRequest')
def AccountDeclineFriendRequestAPI():
    params = request.json
    return AccountAPI.declineFriendRequest(params['access_token'], params['user_id'])


@AccountRoutesAPI.post('/deleteFriend')
def AccountDeleteFrienAPI():
    params = request.json
    return AccountAPI.deleteFriend(params['access_token'], params['user_id'])