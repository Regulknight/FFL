from flask import Flask
from flask import render_template
from flask import send_from_directory

from Model.Task import Task
app = Flask(__name__)

t1 = Task(1, 1, "Покушать", "Сходить куда-нибудь покушать", "Шавермечная", "ночью", "Я", "Не комплитед", 10)
t2 = Task(2, 1, "Разбудить Лесю", "Потолкать её", "Справа", "Сейчас", "Я", "Не комплитед", 10)
t3 = Task(3, 1, "Отхватить от Леси люлей", "Защищаться", "На месте", "После выполнения второго таска", "Я", "Не комплитед совсем", 10)
task_l = t1, t2, t3


def search_task_by_ind(ind):
    for t in task_l:
        if t.id == ind:
            return t


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/tasks")
def tasks():
    return render_template('Card.html', task_list=task_l)


@app.route("/tasks/<int:task_ind>")
def task(task_ind):
    return render_template('task.html', task=search_task_by_ind(task_ind))


@app.route("/css/<path:path>")
def css(path):
    return send_from_directory("css", path)


app.run("localhost")

