from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, IntegerField, RadioField, TimeField, DateField
from wtforms.validators import DataRequired, EqualTo
from app import app

#SET SQLALCHEMY
app.config["SECRET_KEY"] = "mysecret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mynewdb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)

class EmployeeForm(FlaskForm):
    id = IntegerField("Id", validators=[DataRequired()])
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    street = TextAreaField("Street", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField("Repeat Password", validators=[DataRequired(), EqualTo('password')])
    remove = IntegerField("Remove")
    submit = SubmitField("Submit")
    update = SubmitField("Update")

class PlanningForm(FlaskForm):
    id = IntegerField("Id", validators=[DataRequired()])
    days = RadioField('Working Days', choices=[('value', 'Monday'), ('value_two', 'Tuesday'),
                                               ('value_three', 'Wednesday'), ('value_four', 'Thursday'),
                                               ('value_five', 'Friday'), ('value_six', 'Saturday'),
                                               ('value_seven', 'Sunday'),])
    monday_start = TimeField('Start at', format='%H:%M')
    monday_end = TimeField('End at', format='%H:%M')
    tuesday_start = TimeField('Start at', format='%H:%M')
    tuesday_end = TimeField('End at', format='%H:%M')
    wednesday_start = TimeField('Start at', format='%H:%M')
    wednesday_end = TimeField('End at', format='%H:%M')
    thursday_start = TimeField('Start at', format='%H:%M')
    thursday_end = TimeField('End at', format='%H:%M')
    friday_start = TimeField('Start at', format='%H:%M')
    friday_end = TimeField('End at', format='%H:%M')
    saturday_start = TimeField('Start at', format='%H:%M')
    saturday_end = TimeField('End at', format='%H:%M')
    sunday_start = TimeField('Start at', format='%H:%M')
    sunday_end = TimeField('End at', format='%H:%M')
    date = DateField('Date', format='%d.%m.%y')
    week = DateField('Week', format='%m')
    submit = SubmitField('Submit')




class UpdateForm(FlaskForm):
    id = IntegerField("Id", validators=[DataRequired()])
    first_name = StringField("First Name")
    last_name = StringField("Last Name")
    street = TextAreaField("Street")
    email = StringField("Email")
    password = PasswordField("Password")
    password2 = PasswordField("Repeat Password", validators=[EqualTo('password')])
    remove = IntegerField("Remove")
    submit = SubmitField("Submit")
    update = SubmitField("Update")


class TimeReqForm(FlaskForm):
    id = IntegerField("Id", validators=[DataRequired()])
    date = DateField('Date', format='%d.%m.%y')
    time = TimeField('Time', format='%H:%M')
    worker = IntegerField('FTE')


class Test1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))

    def __repr__(self):
        return f'{self.id}, {self.first_name}'

class Test2(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), index=True, unique=False)
    last_name = db.Column(db.String(100), index=True, unique=False)
    street = db.Column(db.String(300), index=True, unique=False)
    email = db.Column(db.String(200), index=True, unique=False)
    password = db.Column(db.String(200))

    def __init__(self, id, first_name, last_name, street, email, password):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.street = str(street)
        self.email = email
        self.password = password



    def __repr__(self):
        return f'{self.id}, {self.first_name}, {self.last_name}, {self.street}, {self.email}, {self.password}'


class Availability(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), index=True, unique=False)
    date = db.Column(db.Date, index=True)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)

    def __init__(self, id, email, date, start_time, end_time):
        self.id = id
        self.email = email
        self.date = date
        self.start_time = start_time
        self.end_time = end_time

