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
    return AccountAPI.register(params['email'], params['password'], params['first_name'], params['last_name'])


@AccountRoutesAPI.post('/getUser')
def AccountGetUserAPI():
    params = request.json
    return AccountAPI.getUserByID(params['access_token'], params['user_id'])