import datetime

from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, SubmitField, PasswordField, SelectField, HiddenField
from wtforms.fields.datetime import DateTimeLocalField
from wtforms.validators import DataRequired

LIST_OF_CATEGORIES = ["Home", "Shop", "Work", "Ideas", "Places"]
LIST_OF_PERIODS = ["Today", "Month", "3 Month", "6 Month", "Year"]
LIST_OF_STATES = ["Done", "Undone"]

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = '123456QWERTYqwerty123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///static/database/todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    task = db.relationship("Tasks", lazy="select", backref=db.backref("author", lazy="joined"))


class Tasks(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    author_task_id = db.Column(db.Integer, nullable=False)
    check = db.Column(db.Boolean, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    data = db.Column(db.DateTime, nullable=False)
    category = db.Column(db.String(30), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)


# db.create_all()


class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign Me Up")


class LogInForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log Me In")


class AddTaskForm(FlaskForm):
    descriptions = StringField("Task",
                               validators=[DataRequired()]
                               )
    date = DateTimeLocalField('Task Deadline',
                              default=datetime.datetime.today,
                              format='%Y-%m-%dT%H:%M',
                              validators=[DataRequired()]
                              )
    category = SelectField("Category",
                           choices=LIST_OF_CATEGORIES,
                           validators=[DataRequired()]
                           )
    submit = SubmitField("Add Task")


class ChangeStatusForm(FlaskForm):
    task_id = HiddenField()
    url = HiddenField()
    options = HiddenField()
    submit = SubmitField()


@app.route("/")
def home():
    return render_template("index.html", current_user=current_user)


@app.route("/change_status", methods=["GET", "POST"])
def change_status():
    if request.method == 'POST':
        task_id = request.form['task_id'],
        url = request.form['url']
        options = request.form['options']
        print(options)
        print(url, options)
        print("cos")
        task = Tasks.query.get(task_id)
        if task.check:
            task.check = False
        else:
            task.check = True
        db.session.commit()
        return redirect(url_for(url, options=options))
    return render_template("index.html")


@app.route("/add_new_task", methods=["GET", "POST"])
def add_new_task():
    form = AddTaskForm()
    print(form.validate_on_submit())

    if form.validate_on_submit():
        task = Tasks(
            author_task_id=len(current_user.task) + 1,
            check=False,
            description=form.descriptions.data,
            data=form.date.data,
            category=form.category.data,
            author_id=current_user.id
        )
        db.session.add(task)
        db.session.commit()
        return redirect(url_for("user_todo_list_sorted_by_states", options="Undone"))
    return render_template("add-task.html", current_user=current_user, form=form)


@app.route("/list_by_category/<options>")
@login_required
def user_todo_list_sorted_by_category(options):
    form = ChangeStatusForm()
    user_tasks = current_user.task
    if options not in LIST_OF_CATEGORIES:
        return redirect(url_for("logout"))
    tasks = [task for task in user_tasks if task.category == options and task.check is False]

    return render_template("index.html", tasks=tasks, form=form,
                           url="user_todo_list_sorted_by_category", options=options)


@app.route("/list_by_period/<options>")
@login_required
def user_todo_list_sorted_by_periods(options):
    data = datetime.datetime.now()
    form = ChangeStatusForm()
    user_tasks = current_user.task
    if options not in LIST_OF_PERIODS:
        print(options)
        return redirect(url_for("logout"))
    if options == "Today":
        delta1 = datetime.timedelta(days=1)
        tasks = []
        for task in user_tasks:
            date2 = datetime.datetime.now() + delta1
            print(date2, task.data)
            if task.data < date2 and task.check is False:
                tasks.append(task)
    elif options == "Month":
        delta1 = datetime.timedelta(days=30)
        tasks = []
        for task in user_tasks:
            date2 = datetime.datetime.now() + delta1
            print(date2, task.data)
            if task.data < date2 and task.check is False:
                tasks.append(task)
    elif options == "3 Month":
        delta1 = datetime.timedelta(days=91)
        tasks = []
        for task in user_tasks:
            date2 = datetime.datetime.now() + delta1
            print(date2, task.data)
            if task.data < date2 and task.check is False:
                tasks.append(task)
    elif options == "6 Month":
        delta1 = datetime.timedelta(days=182)
        tasks = []
        for task in user_tasks:
            date2 = datetime.datetime.now() + delta1
            print(date2, task.data)
            if task.data < date2 and task.check is False:
                tasks.append(task)
    elif options == "Year":
        delta1 = datetime.timedelta(days=365)
        tasks = []
        for task in user_tasks:
            date2 = datetime.datetime.now() + delta1
            print(task.data, date2)
            if task.data < date2 and task.check is False:
                tasks.append(task)

        # tasks = [task for task in user_tasks]

    return render_template("index.html", tasks=tasks, form=form,
                           url="user_todo_list_sorted_by_periods", options=options)


@app.route("/list_by_status/<options>")
@login_required
def user_todo_list_sorted_by_states(options):
    user_tasks = current_user.task
    form = ChangeStatusForm()
    print(options)
    if options not in LIST_OF_STATES:
        return redirect(url_for("logout"))
    if options == "Done":
        tasks = [task for task in user_tasks if task.check is True]
    else:
        tasks = [task for task in user_tasks if task.check is False]

    return render_template("index.html", tasks=tasks, form=form,
                           url="user_todo_list_sorted_by_states", options=options)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LogInForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        if not user:
            flash("That account does not exist, please try again.")
            return redirect(url_for("login"))
        elif not check_password_hash(user.password, password):
            flash("Password is incorrect, please try again")
            return redirect(url_for("login"))
        else:
            login_user(user)
            return redirect(url_for("user_todo_list_sorted_by_states", options="Undone"))

    return render_template("login.html", form=form, current_user=current_user)


@app.route("/registration", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data

        if User.query.filter_by(email=email).first():
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for("login"))

        hash_and_salted_password = generate_password_hash(
            password,
            method='pbkdf2:sha256',
            salt_length=8)

        user = User(
            name=name,
            email=email,
            password=hash_and_salted_password
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for("user_todo_list_sorted_by_states", options="Undone"))
    return render_template("register.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
