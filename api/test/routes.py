from flask import Blueprint


TestRoutesAPI = Blueprint('TestAPI', __name__, url_prefix='/test')


@TestRoutesAPI.route('/ping')
def TestPingAPI():
    return { "result": "pong" }