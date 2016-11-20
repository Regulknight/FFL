import os

import flask
from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import abort
from flask import send_from_directory
from flask_login import logout_user
from flask_login import LoginManager
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user

from Model.Category import Category
from controllers.Id_generator import IdGenerator

from Model.Task import Task
from Model.User import User
from controllers.Id_generator import IdGenerator

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

users = []

idGen = IdGenerator()

u1 = User(idGen.get_new_user_id(), "pam", "pam", "123", "123")
users.append(u1)

t1 = Task(idGen.get_new_task_id(), 3, "Помощь бабушке",
          "Одинокая старушка баба Валя вот уже пять лет живет в старом доме в центре Самары. "
          "Бабе Вале очень тяжело спускаться пешком с пятого этажа, поэтому мы ищем человека, "
          "который может сходить за хлебом в соседний магазин", "Самара", "21.11.2016", "", u1,
          False, 10)
t2 = Task(idGen.get_new_task_id(), 4, "Уборка мусора",
          "Жители Чапаевска хотят провести уборку мусора на улицах своего прекрасного "
          "города, и ищут желающих выйти на субботник и благоустроить территорию "
          "его территорию", "Чапаевск", "25.11.2016", "", u1,
          False, 10)
t3 = Task(idGen.get_new_task_id(), 1, "Игрушки для детей",
          "Требуется волонтер, который может помочь забрать игрушки и одежду и отнести "
          "их в Детский Дом №1", "Московское ш., 18-й км, 18А, Самара, Самарская обл., 443056",
          "22.11.2016", "", u1,
          False, 10)
t4 = Task(idGen.get_new_task_id(), 2, "Помощь бездомному щеночку",
          "Ищем любящего хозяина для щенка кавказской овчарки Малого, "
          "брошенного на произвол судьбы жестокими людьми", "Самара, Металлург",
          "23.11.2016", "", u1,
          False, 10)

task_l = [t1, t2, t3, t4]
u1.task_list.extend(task_l)

c1 = Category(1, "Дети")
c2 = Category(2, "Животные")
с3 = Category(3, "Пожилые жители")
с4 = Category(4, "Благоустройство")
с5 = Category(5, "Разное")

c_l = [c1, c2, с3, с4, с5]


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
    return redirect("/tasks")


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
        category = flask.request.form["category"]
        date = flask.request.form["date"]
        time = flask.request.form["time"]
        location = flask.request.form["location"]
        description = flask.request.form["description"]
        id = idGen.get_new_task_id()
        task = Task(id, get_category_by_id(int(category)), name, description, location, date, time, current_user, "")
        task_l.append(task)
        current_user.task_list.append(task)
        return redirect("/tasks/" + str(id))
    return render_template("add.html", category=c_l)


def get_category_by_id(id):
    for c in c_l:
        if c.id == id:
            return c


@app.route("/css/<path:path>")
def css(path):
    return send_from_directory("css", path)


@app.route("/js/<path:path>")
def js(path):
    return send_from_directory("js", path)


@app.route("/img/<path:path>")
def img(path):
    return send_from_directory("img", path)


@app.route("/fonts/<path:path>")
def fonts(path):
    return send_from_directory("fonts", path)


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
    u = User(idGen.get_new_user_id(), name, fname, login, password)
    users.append(u)
    return True


@app.route("/tasks")
def tasks():
    cat = request.args.get('category', '')
    if cat is not '':
        t_l = search_category_by_id(int(cat))
    else:
        t_l = task_l
    return render_template('Card.html', task_list=t_l, category_list=c_l)


@app.route("/tasks/<int:task_ind>")
def task(task_ind):
    return render_template('task.html', task=search_task_by_ind(task_ind), members=get_task_by_id(task_ind).members)


@app.route("/assigntask", methods=["POST"])
@login_required
def assign_task():
    current_user.assign_list.append(get_task_by_id(int(flask.request.form["id"])))
    get_task_by_id(int(flask.request.form["id"])).members.append(load_user(current_user.id))
    return redirect("/tasks/" + flask.request.form["id"])


def get_task_by_id(id):
    for t in task_l:
        if t.id == id:
            return t


@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user, assign_list=current_user.assign_list,
                           assign_list_size=len(current_user.assign_list))


@app.route("/profile/<int:user_id>")
@login_required
def profile_id(user_id):
    u = load_user(user_id)
    return render_template("profile.html", user=u, assign_list=u.assign_list,
                           assign_list_size=len(u.assign_list))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/delete/<int:id>")
@login_required
def delete(id):
    t = search_task_by_ind(id)
    if current_user.id == t.owner.id:
        task_l.remove(t)
        current_user.task_list.remove(t)
        return redirect("../tasks")
    abort(550)


@app.route("/accept/<int:task_index>", methods=["GET", "POST"])
@login_required
def accept(task_index):
    t = search_task_by_ind(task_index)
    if current_user.id != t.owner.id:
        abort(550)
    if request.method == "POST":
        i = 0
        list_of_values = request.form.listvalues()
        for j in list_of_values:
            values = j
        for tag in values:
            if t.members[i].id != t.owner.id:
                if tag == "on":
                    load_user(t.members[i].id).exp += 10
            i += 1
        t.status = True
        return redirect("../../tasks/"+str(t.id))

    return render_template("accept.html", members=t.members, task=t)


@app.route("/tasks/<int:task_ind>/edit", methods=["GET", "POST"])
def edit(task_ind):
    t = search_task_by_ind(task_ind)
    if current_user.id != t.owner.id:
        abort(550)
    if request.method == "POST":
        t.name = flask.request.form["name"]
        t.date = flask.request.form["date"]
        t.time = flask.request.form["time"]
        t.location = flask.request.form["location"]
        t.description = flask.request.form["description"]
        return redirect("/tasks/" + str(t.id))
    return render_template("edit.html", task=t)


app.secret_key = os.urandom(24)
app.run("localhost", debug=True)
