from functools import wraps

import flask
from bottle import static_file
from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import url_for
from flask_login import LoginManager
from flask_login import login_user

from Model.Task import Task
from Model.User import User

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

users = []
u = User("asd", "Adsa", "123", "123")
users.append(u)

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login = flask.request.form["login"]
        password = flask.request.form["password"]
        user = check_auth(login, password)
        if user:
            login_user(user)
            return redirect(url_for("/"))
    return render_template("login.html")


@app.route("/css/<path:path>")
def css(path):
    return send_from_directory("css", path)


def check_auth(username, password):
    for u in users:
        if u.login == username and u.password == password:
            print(u.id)
            return u
    return None


app.run("localhost")
