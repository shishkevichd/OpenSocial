from flask import Flask
from opensocial.main import MainAPI
from opensocial.utilities import UtilitiesAPI


# Init app
app = Flask(__name__)


# Register API Blueprint
app.register_blueprint(MainAPI)


# Start application
if __name__ == '__main__':
    UtilitiesAPI.create_db()
    app.run(port=8000, debug=True)