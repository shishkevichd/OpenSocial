from flask import Flask
from api.main import MainAPI


# Init app
app = Flask(__name__)


# Register API Blueprint
app.register_blueprint(MainAPI)


# Start application
if __name__ == '__main__':
    app.run(port=8000, debug=True)