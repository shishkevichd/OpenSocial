from flask import Blueprint


from opensocial.routes.accounts import AccountsRAPI
from opensocial.routes.notes import NotesRAPI
from opensocial.routes.groups import GroupsRAPI


MainAPI = Blueprint('MainAPI', __name__, url_prefix='/api')


MainAPI.register_blueprint(AccountsRAPI)
MainAPI.register_blueprint(NotesRAPI)
MainAPI.register_blueprint(GroupsRAPI)


@MainAPI.errorhandler(KeyError)
def APIServerError(error):
    return { "success": False, "why": "incorrect_request" }


@MainAPI.errorhandler(404)
def page_not_found(error):
    return 'This page does not exist', 404