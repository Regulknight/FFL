import os

import flask
from flask import Flask
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import send_from_directory
from flask_login import login_required
from flask_login import confirm_login
from flask_login import LoginManager
from flask_login import current_user
from flask_login import login_user

from Model.User import User

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

users = []
u = User("asd", "Adsa", "123", "123")
users.append(u)


@app.before_request
def before_request():
    g.user = current_user


@login_manager.user_loader
def load_user(user_id):
    for u in users:
        if u.id == user_id:
            return u
    return None


@app.route("/")
def index():
    print(g.user.name)
    return render_template('index.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login = flask.request.form["login"]
        password = flask.request.form["password"]
        user = check_auth(login, password)
        if user:
            login_user(user)
            return redirect("/")
    return render_template("login.html")


@app.route("/css/<path:path>")
def css(path):
    return send_from_directory("css", path)


def check_auth(username, password):
    for u in users:
        if u.login == username and u.password == password:
            return u
    return None


app.secret_key = os.urandom(24)
app.run("localhost")
