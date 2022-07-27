from flask import Blueprint


from opensocial.routes.accounts import AccountsRAPI
from opensocial.routes.notes import NotesRAPI
from opensocial.routes.groups import GroupsRAPI
from opensocial.routes.messages import MessagesRAPI
from opensocial.routes.friends import FriendsRAPI


MainServerAPI = Blueprint('MainServerAPI', __name__, url_prefix='/api')


MainServerAPI.register_blueprint(AccountsRAPI)
MainServerAPI.register_blueprint(NotesRAPI)
MainServerAPI.register_blueprint(GroupsRAPI)
MainServerAPI.register_blueprint(MessagesRAPI)
MainServerAPI.register_blueprint(FriendsRAPI)


@MainServerAPI.errorhandler(KeyError)
def APIServerError(error):
    return { "success": False, "why": "incorrect_request" }, 400

    