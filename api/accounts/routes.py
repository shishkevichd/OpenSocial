from flask import Blueprint


AccountAPI = Blueprint("AccountAPI", __name__, url_prefix='/accounts')


@AccountAPI.route('/login')
def AccountLoginAPI():
    return { "result": "login" }