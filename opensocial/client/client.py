from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from functools import wraps


# ===================================
# Init Application and Decorators
# ===================================

MainClientAPI = Blueprint(
    'MainClientAPI', 
    __name__, 
    url_prefix='/', 
    template_folder='client_templates', 
    static_folder='client_static'
)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            if session['account_data'] is None:
                return redirect(url_for('MainClientAPI.login'))
        except KeyError:
            return redirect(url_for('MainClientAPI.login'))
        return f(*args, **kwargs)
    return decorated_function


# ===================================
# Routes: Main
# ===================================
@MainClientAPI.route('/')
@login_required
def index():
    return render_template('index.html')


@MainClientAPI.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        from opensocial.api.accounts import Accounts

        loginData = {
            'email': request.form['email'],
            'password': request.form['password']
        }

        login_request = Accounts.login(loginData['email'], loginData['password'])

        print(login_request)

        if login_request[0]['success']:
            session['account_data'] = login_request[0]['data']
            session.permanent = False if request.form.get('save_me') == None else True

            return redirect('/')
        else:
            flash('Неверный логин или пароль')
            return redirect(url_for('MainClientAPI.login'))
    else:
        if session.get('account_data') == None:
            return render_template('login.html')
        else:
            return redirect('/')


@MainClientAPI.route('/logout')
@login_required
def test():
    try:
        session.pop('account_data')
        return redirect('/')
    except KeyError:
        return redirect('/')