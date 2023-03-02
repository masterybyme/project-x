from flask import Flask, render_template, current_app, request, redirect, flash, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, logout_user, login_required, UserMixin, login_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, IntegerField, RadioField, TimeField, DateField, SelectField
from wtforms.validators import DataRequired, EqualTo
from datetime import datetime, timedelta, date, time
import datetime
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

#Config
#----------------------------------------------------------------------------------

app = Flask(__name__, template_folder='template')


#SET SQLALCHEMY
app.config["SECRET_KEY"] = "mysecret"
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mynewdb.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:ProjectX2023@localhost/projectxdb'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


#SET FLASK LOGIN
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


#Define Login Requirement

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()
        elif current_user.access_level != 'Admin':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


def user_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()
        elif current_user.access_level != 'User':
            abort(403)
        return f(*args, **kwargs)

    return decorated_function


#Create of Forms
#--------------------------------------------------------------------------------

class EmployeeForm(FlaskForm):
    id = IntegerField("Id", validators=[DataRequired()])
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    employment_level = SelectField("Employment Level", choices=[(1, '100%'), (0.9, '90%'), (0.8, '80%'), (0.7, '70%'),
                                                                (0.6, '60%'), (0.5, '50%'), (0.4, '40%'), (0.3, '30%'),
                                                                (0.2, '20%'), (0.1, '10%')])
    company_name = StringField("Company Name", validators=[DataRequired()])
    department = StringField("Department", validators=[DataRequired()])
    access_level = SelectField("Access Level", choices=[('Admin', 'Admin'), ('User', 'User')])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField("Repeat Password", validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    remove = IntegerField("Remove")
    submit = SubmitField("Submit")
    update = SubmitField("Update")

class PlanningForm(FlaskForm):
    id = IntegerField("Id", validators=[DataRequired()])
    days = RadioField('Working Days', choices=[('value', 'Monday'), ('value_two', 'Tuesday'),
                                               ('value_three', 'Wednesday'), ('value_four', 'Thursday'),
                                               ('value_five', 'Friday'), ('value_six', 'Saturday'),
                                               ('value_seven', 'Sunday'),])
    submit = SubmitField('Submit')



class UpdateForm(FlaskForm):
    first_name = StringField("First Name")
    last_name = StringField("Last Name")
    email = StringField("Email")
    employment_level = SelectField("Employment Level", choices=[(1, '100%'), (0.9, '90%'), (0.8, '80%'), (0.7, '70%'),
                                                                (0.6, '60%'), (0.5, '50%'), (0.4, '40%'), (0.3, '30%'),
                                                                (0.2, '20%'), (0.1, '10%')])
    company_name = StringField("Company Name")
    department = StringField("Department")
    access_level = SelectField("Access Level", choices=[('Admin', 'Admin'), ('User', 'User')])
    password = PasswordField("Password")
    password2 = PasswordField("Repeat Password",
                              validators=[EqualTo('password', message='Passwords must match')])
    remove = IntegerField("Remove")
    submit = SubmitField("Submit")
    update = SubmitField("Update")

class TimeReqForm(FlaskForm):
    id = IntegerField("Id", validators=[DataRequired()])
    weeks = RadioField('Weeks', choices=[(1, 1), (2, 2), (3, 3), (4, 4)])
    date = DateField('Date', format='%Y-%m-%d')
    time = TimeField('Time', format='%H:%M')
    worker = IntegerField('FTE')
    submit = SubmitField('Submit')
    remove = SubmitField('Remove')




#Create of Database
#-------------------------------------------------------------------------

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), index=True, unique=False)
    last_name = db.Column(db.String(100), index=True, unique=False)
    email = db.Column(db.String(200), index=True, unique=True)
    password = db.Column(db.String(200))
    employment_level = db.Column(db.Float, index=True, unique=False)
    company_name = db.Column(db.String(200), index=True, unique=False)
    department = db.Column(db.String(200), index=True, unique=False)
    access_level = db.Column(db.String(200), index=True, unique=False)

    def __init__(self, id, first_name, last_name, email, password, employment_level, company_name, department, access_level):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.employment_level = employment_level
        self.company_name = company_name
        self.department = department
        self.access_level = access_level


class Availability(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), index=True, unique=False)
    date = db.Column(db.Date, index=True)
    weekday = db.Column(db.String(200), index=True, unique=False)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)

    def __init__(self, id, email, date, weekday, start_time, end_time):
        self.id = id
        self.email = email
        self.date = date
        self.weekday = weekday
        self.start_time = start_time
        self.end_time = end_time


class TimeReq(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, index=True)
    start_time = db.Column(db.Time)
    worker = db.Column(db.Integer)

    def __init__(self, id, date, start_time, worker):
        self.id = id
        self.date = date
        self.start_time = start_time
        self.worker = worker


class Company(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(200), index=True, unique=False)
    weekly_hours = db.Column(db.Integer)
    shifts = db.Column(db.Integer)

    def __init__(self, id, company_name, weekly_hours, shifts):
        self.id = id
        self.company_name = company_name
        self.weekly_hours = weekly_hours
        self.shifts = shifts


class OpeningHours(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    weekday = db.Column(db.String(200), index=True, unique=False)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)

    def __init__(self, id, weekday, start_time, end_time):
        self.id = id
        self.weekday = weekday
        self.start_time = start_time
        self.end_time = end_time


class Timetable(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), index=True, unique=False)
    first_name = db.Column(db.String(100), index=True, unique=False)
    last_name = db.Column(db.String(100), index=True, unique=False)
    date = db.Column(db.Date, index=True)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)


    def __init__(self, id, email, first_name, last_name, date, start_time, end_time):
        self.id = id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.date = date
        self.start_time = start_time
        self.end_time = end_time


class TemplateTimeRequirement(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    template_name = db.Column(db.String(200), index=True, unique=False)
    date = db.Column(db.Date, index=True)
    start_time = db.Column(db.Time)
    worker = db.Column(db.Integer)

    def __init__(self, id, template_name, date, start_time, worker):
        self.id = id
        self.template_name = template_name
        self.date = date
        self.start_time = start_time
        self.worker = worker


class TemplateAvailability(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    template_name = db.Column(db.String(200), index=True, unique=False)
    email = db.Column(db.String(200), index=True, unique=False)
    date = db.Column(db.Date, index=True)
    weekday = db.Column(db.String(200), index=True, unique=False)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)

    def __init__(self, id, template_name, email, date, weekday, start_time, end_time):
        self.id = id
        self.template_name = template_name
        self.email = email
        self.date = date
        self.weekday = weekday
        self.start_time = start_time
        self.end_time = end_time


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


#Define functions
#----------------------------------------------------------------------------------

    #General functions
    #-----------------------------------------------------------------------------
@app.route('/', methods=["GET", "POST"])
def homepage():
    data_form = EmployeeForm(csrf_enabled=False)
    if request.method == 'POST':
        id = data_form.remove.data
        remove = User.query.get(id)

        db.session.delete(remove)
        db.session.commit()
        flash('Successful')
    return render_template('/homepage.html', template_form=data_form)


@app.route('/registration', methods = ['GET', 'POST'])
def registration():
    data_form = EmployeeForm(csrf_enabled=False)
    if request.method =='POST':
        last = User.query.order_by(User.id.desc()).first()
        hash = generate_password_hash(data_form.password.data)
        if last is None:
            new_id = 1
        else:
            new_id = last.id + 1

        data = User(id = new_id, first_name = data_form.first_name.data, last_name = data_form.last_name.data,
                    employment_level = data_form.employment_level.data, company_name = data_form.company_name.data,
                    department = data_form.department.data, access_level = data_form.access_level.data,
                    email = data_form.email.data, password = hash)

        try:
            db.session.add(data)
            db.session.commit()
            flash('Registration successful submitted')
            return redirect(url_for('login'))
        except:
            db.session.rollback()
            flash('Error occured - Your mail might be already in use :(')
            return redirect(url_for('registration'))
    else:
        return render_template('registration.html', data_tag=User.query.all(), template_form=data_form)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    login_form = EmployeeForm(csrf_enabled = False)
    if request.method == 'POST':
        user = User.query.filter_by(email = login_form.email.data).first()
        login_user(user)
        if user and check_password_hash(user.password, login_form.password.data):
            flash('Successfully logged in')
            return redirect(url_for('user'))

        else:
            flash('Please try again')
            return render_template('login.html', template_form=login_form)

    else:
        return render_template('login.html', template_form = login_form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('homepage'))


@app.route('/about')
def about():
    return f'About Us'


    #User functions
    #---------------------------------------------------

@app.route('/user', methods=["GET", "POST"])
@login_required
def user():
    account = User.query.get(current_user.id)
    user_form = UpdateForm(csrf_enabled=False, obj=account)

    return render_template('user.html', available=Availability.query.filter_by(email=account.email), account=account, template_form=user_form)


@app.route('/update', methods=["GET", "POST"])
@login_required
def update():
    new_data = User.query.get(current_user.id)
    user_form = UpdateForm(csrf_enabled=False, obj=new_data)
    if request.method == 'POST':

        user_form.populate_obj(new_data)
        try:

            db.session.commit()
            flash('Update successful submitted')
            return redirect(url_for('user'))
        except:
            db.session.rollback()
            flash('Error occured :(')
            return redirect(url_for('user'))
    else:
        return render_template('update.html', data_tag=User.query.all(), account=new_data, template_form=user_form)


@app.route('/planning', methods = ['GET', 'POST'])
@login_required
def planning():
    # today's date
    today = datetime.date.today()
    monday = today - datetime.timedelta(days=today.weekday())
    weekdays = {0:'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday', 5:'Saturday', 6:'Sunday'}
    day_num = 7

    #In order to define tamples a seperate DB is needed

    user = User.query.get(current_user.id)
    planning_form = PlanningForm(csrf_enabled = False)

    if request.method == 'POST':
        for i in range(day_num):
            entry1 = request.form.get(f'day_{i}_0')
            entry2 = request.form.get(f'day_{i}_1')
            if entry1:
                last = Availability.query.order_by(Availability.id.desc()).first()
                if last is None:
                    new_id = 1
                else:
                    new_id = last.id + 1
                new_date = monday + datetime.timedelta(days=i)
                new_entry1 = datetime.datetime.strptime(entry1, '%H:%M').time()
                new_entry2 = datetime.datetime.strptime(entry2, '%H:%M').time()
                new_weekday = weekdays[i]

                data = Availability(id=new_id, date=new_date, weekday=new_weekday, email=user.email,
                                    start_time=new_entry1, end_time=new_entry2)

                db.session.add(data)
                db.session.commit()

    return render_template('planning.html', template_form=planning_form, monday=monday, weekdays=weekdays, day_num=day_num)



@app.route('/delete_availability/<int:id>')
def delete_availability(id):
    account = User.query.get(current_user.id)
    user_form = UpdateForm(csrf_enabled=False, obj=account)
    remove = Availability.query.get(id)

    db.session.delete(remove)
    db.session.commit()
    flash('Successful')
    return render_template('/user.html', account=account, template_form=user_form)

@app.route('/delete/<int:id>')
def delete(id):
    data_form = EmployeeForm(csrf_enabled=False)
    remove = User.query.get(id)

    db.session.delete(remove)
    db.session.commit()
    flash('Successful')
    return render_template('/registration.html', template_form=data_form)


    #Admin function
    #-----------------------------------------------------------------


@app.route('/admin', methods = ['GET', 'POST'])
@admin_required
def admin():
    time_form = TimeReqForm(csrf_enbled=False)
    Time = TimeReq.query.all()
    today = datetime.date.today()
    monday = today - datetime.timedelta(days=today.weekday())
    day_num = 7

    #Submit the required FTE per hour
    if request.method == 'POST' and 'submit' in request.form:
        for i in range(day_num):
            for hour in range(24):
                capacity = request.form.get(f'worker_{i}_{hour}')
                if capacity:
                    last = TimeReq.query.order_by(TimeReq.id.desc()).first()
                    if last is None:
                        new_id = 1
                    else:
                        new_id = last.id + 1
                    new_date = monday + datetime.timedelta(days=i)
                    time_num = hour * 100
                    time = f'{time_num:04d}'
                    new_time = datetime.datetime.strptime(time, '%H%M').time()

                    req = TimeReq(id=new_id, date=new_date, start_time=new_time, worker=capacity)

                    db.session.add(req)
                    db.session.commit()
                    return render_template('admin.html', monday=monday, timedelta=timedelta, day_num=day_num, template_form=time_form)

    #Remove entries of single dates
    if request.method == 'POST' and 'remove' in request.form:
        remove_date = time_form.date.data
        remove_date_formatted = remove_date.strftime('%Y-%m-%d')
        remove = TimeReq.query.filter_by(date=remove_date_formatted).all()

        for entry in remove:
            db.session.delete(entry)

        db.session.commit()
        flash('Successful')
        return render_template('admin.html', monday=monday, timedelta=timedelta, day_num=day_num, Time=Time, template_form=time_form)


    return render_template('admin.html', monday=monday, timedelta=timedelta, day_num=day_num, Time=Time, template_form=time_form)


@app.route('/dashboard')
@admin_required
def dashboard():
    return render_template('dashboard.html', data_tag=User.query.all(), open_tag=OpeningHours.query.all())


@app.route('/opening', methods = ['GET', 'POST'])
@admin_required
def opening():
    opening_hour = OpeningHours.query.all()
    weekdays = {0:'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday', 5:'Saturday', 6:'Sunday'}
    day_num = 7
    opening_form = UpdateForm(csrf_enabled = False, obj=opening_hour)

    if request.method == 'POST':
        for i in range(day_num):
            entry1 = request.form.get(f'day_{i}_0')
            entry2 = request.form.get(f'day_{i}_1')
            if entry1:
                last = OpeningHours.query.order_by(OpeningHours.id.desc()).first()
                if last is None:
                    new_id = 1
                else:
                    new_id = last.id + 1
                new_entry1 = datetime.datetime.strptime(entry1, '%H:%M').time()
                new_entry2 = datetime.datetime.strptime(entry2, '%H:%M').time()
                new_weekday = weekdays[i]

                data = OpeningHours(id=new_id, weekday=new_weekday, start_time=new_entry1, end_time=new_entry2)

                db.session.add(data)
                db.session.commit()

    return render_template('opening.html', template_form=opening_form, weekdays=weekdays, day_num=day_num)



if __name__ == '__main__':
    app.run()

