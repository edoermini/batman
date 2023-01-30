from flask import Flask, redirect, url_for, request, session, render_template
import flask_login

app = Flask(__name__)
app.secret_key = 'super secret string'  # Change this!

login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


users = {'foo@bar.tld': {'password': 'secret'}}

class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(username):
    if username not in users:
        return

    user = User()
    user.id = username
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return '''
               <form action='login' method='POST'>
                <input type='text' name='username' id='test' placeholder='username'/>
                <input type='password' name='password' id='password' placeholder='password'/>
                <input type='submit' name='submit'/>
               </form>
               '''

    username = request.form['username']
    if username in users and request.form['password'] == users[username]['password']:
        user = User()
        user.id = username
        flask_login.login_user(user)
        return redirect(url_for('index'))

    return 'Bad login'


@app.route('/')
@flask_login.login_required
def index():
    return render_template("index.html")

@app.route("/logout")
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect(url_for("login"))