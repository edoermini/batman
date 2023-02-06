import os
from flask import Flask, redirect, url_for, request, session, render_template
import flask_login
import base64

from settings import USERS, CONTRACT_ADDRESS, ABI, PRIVATE_KEYS
from batoken import BAToken

batoken = BAToken(CONTRACT_ADDRESS, os.environ.get("NODE_URL"), ABI, PRIVATE_KEYS)

app = Flask(__name__)
app.secret_key = 'super secret string'  # Change this!

login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@app.template_filter("base64_decode")
def base64_decode(value):
    return base64.b64decode(value).decode('utf-8')

class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(username):
    if username not in USERS:
        return

    user = User()
    user.id = username
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in USERS:
        return

    user = User()
    user.id = email
    return user


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form['username']
    if username in USERS and request.form['password'] == USERS[username]['password']:
        user = User()
        user.id = username
        flask_login.login_user(user)

        return redirect(url_for('index'))

    return 'Bad login'

@app.route('/publish', methods=['GET', 'POST'])
@flask_login.login_required
def publish():
    username=flask_login.current_user.id

    if request.method == 'GET':
        return render_template("publish.html", contract_abi=ABI, contract_address=CONTRACT_ADDRESS, user_address=USERS[username]['address'], username=username)
    
    # ajax request
    title = request.form['title']
    cve = request.form['cve']
    type = request.form['type']
    severity = request.form['severity']
    language = request.form['language']
    poc = request.form['poc']

    try:
        batoken.publish(USERS[username]['address'], poc, severity, cve, type, title, language)
    except Exception as msg:
        return {"error":True, "message":str(msg).split(" revert ")[1]}
    
    return {"error":False, "message":"Poc successfully published"}


@app.route('/')
@flask_login.login_required
def index():

    pocs = batoken.retrieve_pocs()
    username=flask_login.current_user.id

    return render_template("index.html", contract_abi=ABI, contract_address=CONTRACT_ADDRESS, user_address=USERS[username]['address'], pocs=pocs, username=username)

@app.route("/logout")
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect(url_for("login"))

@app.route("/mint", methods=['GET', 'POST'])
@flask_login.login_required
def mint():
    username=flask_login.current_user.id

    if request.method == 'GET':
        return render_template('mint.html', contract_abi=ABI, contract_address=CONTRACT_ADDRESS, user_address=USERS[username]['address'], username=username)
    
    value = request.form['value']
    batoken.mint(USERS[username]['address'], value)

    return redirect(url_for("mint"))

@app.route("/verify", methods=['POST'])
@flask_login.login_required
def ajax_verify():
    username=flask_login.current_user.id

    if request.method == 'POST':
        poc_id = request.form['pocid']
        try:
            batoken.verify(USERS[username]['address'], poc_id)
        except Exception as msg:
            return {"error":True, "message":str(msg).split(" revert ")[1]}
        
        return {"error":False, "message":"Poc successfully verified"}
    
    return redirect(url_for('index'))