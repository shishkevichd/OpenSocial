from flask import Blueprint


from api.accounts.routes import AccountRoutesAPI
from api.test.routes import TestRoutesAPI


MainAPI = Blueprint('MainAPI', __name__, url_prefix='/api')


MainAPI.register_blueprint(AccountRoutesAPI)
MainAPI.register_blueprint(TestRoutesAPI)


@MainAPI.errorhandler(KeyError)
def APIServerError(error):
    return { "success": False, "why": "incorrect_request" }


@MainAPI.errorhandler(404)
def APINotFoundError(error):
    return { "success": False, "why": "page_not_found" }