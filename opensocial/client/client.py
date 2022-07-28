from flask import Blueprint, render_template, session, redirect


# ===================================
# Init Application
# ===================================
MainClientAPI = Blueprint(
    'MainClientAPI', 
    __name__, 
    url_prefix='/', 
    template_folder='client_templates', 
    static_folder='client_static'
)

# ===================================
# Routes
# ===================================
@MainClientAPI.route('/')
def index():
    return render_template('index.html')


@MainClientAPI.route('/login')
def login():
    session['access_token'] = "bbb"
    return 'success'


@MainClientAPI.route('/logout')
def test():
    try:
        session.pop('access_token')
        return redirect('/')
    except KeyError:
        return redirect('/')