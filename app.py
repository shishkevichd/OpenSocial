from flask import Flask
from opensocial.main import MainAPI
from opensocial.utilities import UtilitiesAPI
from opensocial.config import ConfigAPI


# Init app
app = Flask(__name__)


# Register API Blueprint
app.register_blueprint(MainAPI)


# Start application
if __name__ == '__main__':
    UtilitiesAPI.create_db()
    app.run(
        host=ConfigAPI.server['host'],
        port=ConfigAPI.server['port'],
        debug=ConfigAPI.server['debug']
    )