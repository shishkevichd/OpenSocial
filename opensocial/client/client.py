from flask import Blueprint, render_template

MainClientAPI = Blueprint('MainClientAPI', __name__, url_prefix='/', template_folder='./views')

@MainClientAPI.route('/')
def index():
    return render_template('index.html')