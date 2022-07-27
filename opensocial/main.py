from flask import Blueprint


from opensocial.routes.accounts import AccountsRAPI
from opensocial.routes.notes import NotesRAPI
from opensocial.routes.groups import GroupsRAPI
from opensocial.routes.messages import MessagesRAPI
from opensocial.routes.friends import FriendsRAPI


MainAPI = Blueprint('MainAPI', __name__, url_prefix='/api')


MainAPI.register_blueprint(AccountsRAPI)
MainAPI.register_blueprint(NotesRAPI)
MainAPI.register_blueprint(GroupsRAPI)
MainAPI.register_blueprint(MessagesRAPI)
MainAPI.register_blueprint(FriendsRAPI)


@MainAPI.errorhandler(KeyError)
def APIServerError(error):
    return { "success": False, "why": "incorrect_request" }

    