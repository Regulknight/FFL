import os

import flask
from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import send_from_directory
from flask_login import LoginManager
from flask_login import current_user
from flask_login import login_user

from Model.Category import Category
from Model.Task import Task
from Model.User import User
from controllers.Id_generator import IdGenerator

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
gen = IdGenerator()

users = []

idGen = IdGenerator()

u1 = User(idGen.get_new_user_id(), "pam", "pam", "123", "123")
users.append(u1)

t1 = Task(idGen.get_new_task_id(), 1, "Покушать", "Сходить куда-нибудь покушать", "Шавермечная", "ночью", "Я",
          "Не комплитед", 10)
t2 = Task(idGen.get_new_task_id(), 1, "Разбудить Лесю", "Потолкать её", "Самара, 5 просека, 99Б", "Сейчас", "Я",
          "Не комплитед", 10)
t3 = Task(idGen.get_new_task_id(), 1, "Отхватить от Леси люлей", "Защищаться", "На месте",
          "После выполнения второго таска", "Я",
          "Не комплитед совсем", 10)
task_l = [t1, t2, t3]

c1 = Category(1, "Котики")
c2 = Category(2, "Собачки")
с3 = Category(3, "Бабушки")

c_l = [c1, c2, с3]


def search_task_by_ind(ind):
    for t in task_l:
        if t.id == ind:
            return t


def search_category_by_id(id):
    result = []
    for x in task_l:
        if x.category_index == id:
            result.append(x)
    return result



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
    next = flask.request.args.get('next')
    if request.method == "POST":
        login = flask.request.form["login"]
        password = flask.request.form["password"]
        next = flask.request.form["next"]
        user = check_auth(login, password)
        if user:
            if login_user(user, False, True):
                user.is_authenticated = True
            if next == "None":
                return flask.redirect("/")
            return flask.redirect(next)
        else:
            return "Вы кто такой вообще?"
    return render_template("login.html", next=next)


@app.route("/tasks/add", methods=["GET", "POST"])
@login_required
def add_task():
    if request.method == "POST":
        name = flask.request.form["name"]
        date = flask.request.form["date"]
        time = flask.request.form["time"]
        location = flask.request.form["location"]
        id = idGen.get_new_task_id()
        task = Task(id, "", name, "", location, date + " " + time, "", "")
        task_l.append(task)
        current_user.task_list.append(task)
        print(name + " " + date + " " + time)
        return redirect("/tasks/" + str(id))
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
    cat = request.args.get('category', '')
    if cat is not None:
        t_l = search_category_by_id(int(cat))
    else:
        t_l = task_l
    return render_template('Card.html', task_list=t_l, category_list=c_l)


@app.route("/tasks/<int:task_ind>")
def task(task_ind):
    return render_template('task.html', task=search_task_by_ind(task_ind), members = get_task_by_id(task_ind).members)


@app.route("/assigntask", methods=["POST"])
@login_required
def assign_task():
    current_user.assign_list.append(flask.request.form["id"])
    get_task_by_id(int(flask.request.form["id"])).members.append(current_user)
    return redirect("/tasks/" + flask.request.form["id"])


def get_task_by_id(id):
    for t in task_l:
        if t.id == id:
            return t


app.secret_key = os.urandom(24)
app.run("localhost", debug=True)
