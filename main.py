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

from Model.Task import Task
from Model.User import User
from controllers.Id_generator import IdGenerator

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
gen = IdGenerator()

users = []

t1 = Task(1, 1, "Покушать", "Сходить куда-нибудь покушать", "Шавермечная", "ночью", "Я", "Не комплитед", 10)
t2 = Task(2, 1, "Разбудить Лесю", "Потолкать её", "Справа", "Сейчас", "Я", "Не комплитед", 10)
t3 = Task(3, 1, "Отхватить от Леси люлей", "Защищаться", "На месте", "После выполнения второго таска", "Я", "Не комплитед совсем", 10)
task_l = t1, t2, t3


def search_task_by_ind(ind):
    for t in task_l:
        if t.id == ind:
            return t



@login_manager.user_loader
def load_user(user_id):
    for u in users:
        if u.id == user_id:
            return u
    return None


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
            if login_user(user, False, True):
                user.is_authenticated = True
            return redirect("/")
        else:
            return "Вы кто такой вообще?"
    return render_template("login.html")


@app.route("/tasks/add", methods=["GET", "POST"])
def add_task():
    if request.method == "POST":
        name = flask.request.form["name"]
        date = flask.request.form["date"]
        time = flask.request.form["time"]
        print(name + " " + date + " " + time)
    return render_template("add.html")


@app.route("/css/<path:path>")
def css(path):
    return send_from_directory("css", path)


def check_auth(username, password):
    for u in users:
        if u.login == username and u.password == password:
            return u
    return None


@app.route("/logup", methods=["GET", "POST"])
def logup():
    if request.method == "POST":
        fname = flask.request.form["fname"]
        name = flask.request.form["name"]
        login = flask.request.form["login"]
        password = flask.request.form["password"]
        if registraty(fname, name, login, password):
            user = check_auth(login, password)
            if user:
                if login_user(user, False, True):
                    user.is_authenticated = True
                return redirect("/")
    return render_template("logup.html")


def registraty(fname, name, login, password):
    for u in users:
        if u.login == login:
            return False
    u = User(gen.get_new_user_id(), name, fname, login, password)
    users.append(u)
    return True

@app.route("/tasks")
def tasks():
    return render_template('Card.html', task_list=task_l)


@app.route("/tasks/<int:task_ind>")
def task(task_ind):
    return render_template('task.html', task=search_task_by_ind(task_ind))

app.secret_key = os.urandom(24)
app.run("localhost",debug=True)
