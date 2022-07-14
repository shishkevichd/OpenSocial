from flask import Blueprint


TestAPI = Blueprint('TestAPI', __name__, url_prefix='/test')


@TestAPI.route('/ping')
def TestPingAPI():
    return { "result": "pong" }