from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, URL

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = '123456QWERTYqwerty123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///static/database/todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    task = db.relationship("Tasks", lazy="select", backref=db.backref("author", lazy="joined"))


class Tasks(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
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
    description = SubmitField("Task", validators=[DataRequired()])
    data = DateTimeField("Data")
    category = SelectField("Category")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login")
def login():
    form = LogInForm()
    return render_template("login.html", form=form)


@app.route("/registration", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    return render_template("register.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
