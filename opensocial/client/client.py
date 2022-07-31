from flask import Blueprint, render_template, session, redirect, url_for, flash
from functools import wraps

from opensocial.client.forms.login import LoginForm
from opensocial.client.forms.register import RegisterForm

import json

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
        from opensocial.api.accounts import Accounts
        
        if session.get('account_data') == None:
            return redirect(url_for('MainClientAPI.login'))
        else:
            check_token = Accounts.isValidAccessToken(session.get('account_data')['access_token'])
            if not check_token:
                return redirect(url_for('MainClientAPI.login'))
        return f(*args, **kwargs)
    return decorated_function


@MainClientAPI.context_processor
def context_processor():
    def getUser(user_id=""):
        from opensocial.api.accounts import Accounts

        if len(user_id) != 0:
            return Accounts.getUser("", user_id=user_id, without_token=True)[0]['data']
        else:
            return Accounts.getUser(session.get('account_data')['access_token'], "")[0]['data']
    
    def getPostComp():
        from opensocial.api.accounts import Accounts
        return Accounts.getPostCompilation(session.get('account_data')['access_token'])
    
    return dict(getUser=getUser, getPostComp=getPostComp)


# ===================================
# Routes: Account Managment
# ===================================


@MainClientAPI.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        from opensocial.api.accounts import Accounts

        register_request = Accounts.register(form.email.data, form.password.data, form.first_name.data, form.last_name.data, form.gender.data)

        if register_request[0]['success']:
            session['account_data'] = register_request[0]['data']
            return redirect('/')
        else:
            flash('Не удалось зарегистрироваться')
            return redirect('/register')

    if session.get('account_data') == None:
        return render_template('register.html', form=form)
    else:
        return redirect('/')


@MainClientAPI.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        from opensocial.api.accounts import Accounts

        loginData = {
            'email': form.email.data,
            'password': form.password.data,
            'save_me': form.save_me.data
        }

        login_request = Accounts.login(loginData['email'], loginData['password'])

        if login_request[0]['success']:
            session['account_data'] = login_request[0]['data']
            session.permanent = False if loginData['save_me'] == None else True

            return redirect('/')
        else:
            flash('Неверный логин или пароль')
            return redirect(url_for('MainClientAPI.login'))

    if session.get('account_data') == None:
        return render_template('login.html', form=form)
    else:
        return redirect('/')


@MainClientAPI.route('/logout')
@login_required
def logout():
    try:
        session.pop('account_data')
        return redirect('/')
    except KeyError:
        return redirect('/')


# ===================================
# Routes: Account Managment
# ===================================


@MainClientAPI.route('/')
@login_required
def home():
    return render_template('index.html')


@MainClientAPI.route('/user', defaults={'user_id': ""})
@MainClientAPI.route('/user/<user_id>')
@login_required
def profile(user_id):
    return render_template('profile.html')