from flask import Blueprint


from opensocial.routes.accounts import AccountsRAPI
from opensocial.routes.notes import NotesRAPI

MainAPI = Blueprint('MainAPI', __name__, url_prefix='/api')


MainAPI.register_blueprint(AccountsRAPI)
MainAPI.register_blueprint(NotesRAPI)


@MainAPI.errorhandler(KeyError)
def APIServerError(error):
    return { "success": False, "why": "incorrect_request" }