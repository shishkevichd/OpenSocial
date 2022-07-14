from flask import Blueprint


AccountRoutesAPI = Blueprint("AccountAPI", __name__, url_prefix='/accounts')


@AccountRoutesAPI.route('/login')
def AccountLoginAPI():
    return { "result": "login" }