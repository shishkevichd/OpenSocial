from flask import Blueprint


from api.accounts.routes import AccountRoutesAPI
from api.test.routes import TestRoutesAPI


MainAPI = Blueprint('MainAPI', __name__, url_prefix='/api')


MainAPI.register_blueprint(AccountRoutesAPI)
MainAPI.register_blueprint(TestRoutesAPI)