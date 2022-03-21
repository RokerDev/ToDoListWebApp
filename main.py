from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, URL

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = '123456QWERTYqwerty123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////static/database/todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Tasks(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    check = db.Column(db.Boolean)
    description = db.Column(db.String(200))
    data = db.Column(db.DateTime)
    category = db.Column(db.String(30))
    author = relationship("User", back_populates="task")


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    task = relationship("Tasks", back_populates="author")


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


@app.route("/registration")
def register():
    pass


if __name__ == "__main__":
    app.run(debug=True)
