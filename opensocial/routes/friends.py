from flask import Blueprint, request
from opensocial.api.friends import Friends


FriendsRAPI = Blueprint('Friends', __name__, url_prefix='/friends')


@FriendsRAPI.post('/sendFriendRequest')
def AccountSendFriendRequestAPI():
    params = request.json
    return Friends.sendRequest(params['access_token'], params['user_id'])


@FriendsRAPI.post('/acceptFriendRequest')
def AccountAcceptFriendRequestAPI():
    params = request.json
    return Friends.acceptRequest(params['access_token'], params['user_id'])


@FriendsRAPI.post('/declineFriendRequest')
def AccountDeclineFriendRequestAPI():
    params = request.json
    return Friends.declineRequest(params['access_token'], params['user_id'])


@FriendsRAPI.post('/deleteFriend')
def AccountDeleteFriendAPI():
    params = request.json
    return Friends.deleteFromFriends(params['access_token'], params['user_id'])
