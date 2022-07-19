from flask import Blueprint, request
from opensocial.api.groups import Groups


GroupsRAPI = Blueprint('Groups', __name__, url_prefix='/groups')


@GroupsRAPI.post('/createGroup')
def GroupsCreateGroupAPI():
    params = request.json
    return Groups.createGroup(params['access_token'], params['group_name'])


@GroupsRAPI.post('/createPost')
def GroupsCreatePostAPI():
    params = request.json
    return Groups.createPost(params['access_token'], params['group_id'], params['content'])


@GroupsRAPI.post('/deletePost')
def GroupsDeletePostAPI():
    params = request.json
    return Groups.deletePost(params['access_token'], params['group_id'], params['post_id'])


@GroupsRAPI.post('/editPost')
def GroupsEditPostAPI():
    params = request.json
    return Groups.editPost(params['access_token'], params['group_id'], params['post_id'], params['content'])


@GroupsRAPI.post('/setUserGroupRole')
def GroupsSetUserGroupRoleAPI():
    params = request.json
    return Groups.setUserGroupRole(params['access_token'], params['group_id'], params['user_id'], params['status'])


@GroupsRAPI.post('/subscribe')
def GroupsSubscribeAPI():
    params = request.json
    return Groups.subscribeAtGroup(params['access_token'], params['group_id'])


@GroupsRAPI.post('/unsubscribe')
def GroupsUnsubscribeAPI():
    params = request.json
    return Groups.unsubscribeFromGroup(params['access_token'], params['group_id'])


@GroupsRAPI.post('/deleteSubscriberFromGroup')
def GroupsDeleteSubscriberFromGroupAPI():
    params = request.json
    return Groups.deleteSubscriberFromGroup(params['access_token'], params['group_id'], params['user_id'])