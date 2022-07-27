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