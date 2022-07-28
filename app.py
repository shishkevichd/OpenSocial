from flask import Flask
from flask_cors import CORS
from opensocial.server import MainServerAPI
from opensocial.client.client import MainClientAPI
from opensocial.utilities import UtilitiesAPI
from opensocial.config import ConfigAPI


# Init app
app = Flask(__name__)
app.secret_key = ConfigAPI.secret_key
CORS(app=app, resources={r"/api/*": {"origins": "*"}})

# Register API Blueprint
app.register_blueprint(MainServerAPI)
app.register_blueprint(MainClientAPI)


# Start application
if __name__ == '__main__':
    UtilitiesAPI.create_db()
    app.run(
        host=ConfigAPI.server['host'],
        port=ConfigAPI.server['port'],
        debug=ConfigAPI.server['debug']
    )