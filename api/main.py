from flask import Blueprint


from api.accounts.routes import AccountAPI
from api.test.routes import TestAPI


MainAPI = Blueprint('MainAPI', __name__, url_prefix='/api')


MainAPI.register_blueprint(AccountAPI)
MainAPI.register_blueprint(TestAPI)