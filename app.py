from flask import Flask, render_template, current_app, request, redirect, flash, url_for, abort, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, logout_user, login_required, UserMixin, login_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, IntegerField, RadioField, TimeField, DateField, SelectField
from wtforms.validators import DataRequired, EqualTo
from datetime import datetime, timedelta
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
    template1 = SubmitField('Template1')
    template2 = SubmitField('Template2')
    template3 = SubmitField('Template 3')
    template_name = StringField('Template Name')
    template = SubmitField('Save Template')
    prev_week = SubmitField('Previous Week')
    next_week = SubmitField('Next Week')



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
    template1 = SubmitField('Template1')
    template2 = SubmitField('Template2')
    template3 = SubmitField('Template 3')
    template_name = StringField('Template Name')
    template = SubmitField('Save Template')
    prev_week = SubmitField('Previous Week')
    next_week = SubmitField('Next Week')




#Create of Database
#-------------------------------------------------------------------------

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, index=True, unique=False)
    first_name = db.Column(db.String(100), index=True, unique=False)
    last_name = db.Column(db.String(100), index=True, unique=False)
    email = db.Column(db.String(200), index=True, unique=True)
    password = db.Column(db.String(200))
    employment_level = db.Column(db.Float, index=True, unique=False)
    company_name = db.Column(db.String(200), index=True, unique=False)
    department = db.Column(db.String(200), index=True, unique=False)
    access_level = db.Column(db.String(200), index=True, unique=False)
    created_by = db.Column(db.Integer, index=True, unique=False)
    changed_by = db.Column(db.Integer, index=True, unique=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now)


    def __init__(self, id, company_id, first_name, last_name, email, password, employment_level, company_name, department,
                 access_level, created_by, changed_by):
        self.id = id
        self.company_id = company_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.employment_level = employment_level
        self.company_name = company_name
        self.department = department
        self.access_level = access_level
        self.created_by = created_by
        self.changed_by = changed_by



class Availability(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), index=True, unique=False)
    date = db.Column(db.Date, index=True)
    weekday = db.Column(db.String(200), index=True, unique=False)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    start_time2 = db.Column(db.Time)
    end_time2 = db.Column(db.Time)
    start_time3 = db.Column(db.Time)
    end_time3 = db.Column(db.Time)
    created_by = db.Column(db.Integer, index=True, unique=False)
    changed_by = db.Column(db.Integer, index=True, unique=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, id, email, date, weekday, start_time, end_time, start_time2, end_time2, start_time3, end_time3,
                 created_by, changed_by):
        self.id = id
        self.email = email
        self.date = date
        self.weekday = weekday
        self.start_time = start_time
        self.end_time = end_time
        self.start_time2 = start_time2
        self.end_time2 = end_time2
        self.start_time3 = start_time3
        self.end_time3 = end_time3
        self.created_by = created_by
        self.changed_by = changed_by



class TimeReq(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, index=True)
    start_time = db.Column(db.Time)
    worker = db.Column(db.Integer)
    created_by = db.Column(db.Integer, index=True, unique=False)
    changed_by = db.Column(db.Integer, index=True, unique=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, id, date, start_time, worker, created_by, changed_by):
        self.id = id
        self.date = date
        self.start_time = start_time
        self.worker = worker
        self.created_by = created_by
        self.changed_by = changed_by



class Company(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(200), index=True, unique=False)
    weekly_hours = db.Column(db.Integer)
    shifts = db.Column(db.Integer)
    created_by = db.Column(db.Integer, index=True, unique=False)
    changed_by = db.Column(db.Integer, index=True, unique=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, id, company_name, weekly_hours, shifts, created_by, changed_by):
        self.id = id
        self.company_name = company_name
        self.weekly_hours = weekly_hours
        self.shifts = shifts
        self.created_by = created_by
        self.changed_by = changed_by



class OpeningHours(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    weekday = db.Column(db.String(200), index=True, unique=False)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    created_by = db.Column(db.Integer, index=True, unique=False)
    changed_by = db.Column(db.Integer, index=True, unique=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, id, weekday, start_time, end_time, created_by, changed_by):
        self.id = id
        self.weekday = weekday
        self.start_time = start_time
        self.end_time = end_time
        self.created_by = created_by
        self.changed_by = changed_by



class Timetable(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), index=True, unique=False)
    first_name = db.Column(db.String(100), index=True, unique=False)
    last_name = db.Column(db.String(100), index=True, unique=False)
    date = db.Column(db.Date, index=True)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    start_time2 = db.Column(db.Time)
    end_time2 = db.Column(db.Time)
    start_time3 = db.Column(db.Time)
    end_time3 = db.Column(db.Time)
    created_by = db.Column(db.Integer, index=True, unique=False)
    changed_by = db.Column(db.Integer, index=True, unique=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now)


    def __init__(self, id, email, first_name, last_name, date, start_time, end_time, start_time2, end_time2,
                 start_time3, end_time3, created_by, changed_by):
        self.id = id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.start_time2 = start_time2
        self.end_time2 = end_time2
        self.start_time3 = start_time3
        self.end_time3 = end_time3
        self.created_by = created_by
        self.changed_by = changed_by



class TemplateTimeRequirement(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    template_name = db.Column(db.String(200), index=True, unique=False)
    date = db.Column(db.Date, index=True)
    weekday = db.Column(db.String(200), index=True, unique=False)
    start_time = db.Column(db.Time)
    worker = db.Column(db.Integer)
    created_by = db.Column(db.Integer, index=True, unique=False)
    changed_by = db.Column(db.Integer, index=True, unique=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, id, template_name, date, weekday, start_time, worker, created_by, changed_by):
        self.id = id
        self.template_name = template_name
        self.date = date
        self.weekday = weekday
        self.start_time = start_time
        self.worker = worker
        self.created_by = created_by
        self.changed_by = changed_by



class TemplateAvailability(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    template_name = db.Column(db.String(200), index=True, unique=False)
    email = db.Column(db.String(200), index=True, unique=False)
    date = db.Column(db.Date, index=True)
    weekday = db.Column(db.String(200), index=True, unique=False)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    start_time2 = db.Column(db.Time)
    end_time2 = db.Column(db.Time)
    start_time3 = db.Column(db.Time)
    end_time3 = db.Column(db.Time)
    created_by = db.Column(db.Integer, index=True, unique=False)
    changed_by = db.Column(db.Integer, index=True, unique=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, id, template_name, email, date, weekday, start_time, end_time, start_time2, end_time2,
                 start_time3, end_time3, created_by, changed_by):
        self.id = id
        self.template_name = template_name
        self.email = email
        self.date = date
        self.weekday = weekday
        self.start_time = start_time
        self.end_time = end_time
        self.start_time2 = start_time2
        self.end_time2 = end_time2
        self.start_time3 = start_time3
        self.end_time3 = end_time3
        self.created_by = created_by
        self.changed_by = changed_by




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
            new_id = 1000
        else:
            new_id = last.id + 1

        last_company_id = User.query.filter_by(company_name=data_form.company_name.data).order_by(User.company_id.desc()).first()
        if last_company_id is None:
            new_company_id = 1000
        else:
            new_company_id = last_company_id + 1

        data = User(id = new_id, company_id = new_company_id, first_name = data_form.first_name.data,
                    last_name = data_form.last_name.data, employment_level = data_form.employment_level.data,
                    company_name = data_form.company_name.data, department = data_form.department.data,
                    access_level = data_form.access_level.data, email = data_form.email.data, password = hash,
                    created_by = new_company_id, changed_by = new_company_id)

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
        if user is None:
            flash('User does not exist')
            return redirect(url_for('user'))
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

    return render_template('user.html', available=Availability.query.filter_by(email=account.email),
                           account=account, template_form=user_form)


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
    week_adjustment = session.get('week_adjustment', 0)

    user = User.query.get(current_user.id)
    company_id = current_user.company_id
    planning_form = PlanningForm(csrf_enabled = False)


    if planning_form.prev_week.data:
        week_adjustment -=7
        session['week_adjustment'] = week_adjustment

        monday = monday + datetime.timedelta(days=week_adjustment)

        return render_template('planning.html', template_form=planning_form, monday=monday, weekdays=weekdays,
                               day_num=day_num)

    if planning_form.next_week.data:
        week_adjustment +=7
        session['week_adjustment'] = week_adjustment

        monday = monday + datetime.timedelta(days=week_adjustment)

        return render_template('planning.html', template_form=planning_form, monday=monday, weekdays=weekdays,
                               day_num=day_num)

    #Set Template
    if planning_form.template1.data:
        temp_dict = {}
        for i in range(day_num):
            temp = TemplateAvailability.query.filter_by(email=user.email, weekday=weekdays[i]).first()
            if temp is None:
                pass
            else:
                new_i = i + 1
                temp_dict[str(new_i) + '&0'] = temp.start_time
                temp_dict[str(new_i) + '&1'] = temp.end_time
                temp_dict[str(new_i) + '&2'] = temp.start_time2
                temp_dict[str(new_i) + '&3'] = temp.end_time2
                temp_dict[str(new_i) + '&4'] = temp.start_time3
                temp_dict[str(new_i) + '&5'] = temp.end_time3

        return render_template('planning.html', template_form=planning_form, monday=monday, weekdays=weekdays,
                               day_num=day_num, temp_dict=temp_dict)


    #Save Availability
    if request.method == 'POST' and 'submit' in request.form:
        for i in range(day_num):
            entry1 = request.form.get(f'day_{i}_0')
            entry2 = request.form.get(f'day_{i}_1')
            entry3 = request.form.get(f'day_{i}_2')
            entry4 = request.form.get(f'day_{i}_3')
            entry5 = request.form.get(f'day_{i}_4')
            entry6 = request.form.get(f'day_{i}_5')
            if entry1:
                last = Availability.query.order_by(Availability.id.desc()).first()
                if last is None:
                    new_id = 1000
                else:
                    new_id = last.id + 1
                new_date = monday + datetime.timedelta(days=i) + datetime.timedelta(days=week_adjustment)
                try:
                    new_entry1 = datetime.datetime.strptime(entry1, '%H:%M:%S').time()
                    new_entry2 = datetime.datetime.strptime(entry2, '%H:%M:%S').time()
                    new_entry3 = datetime.datetime.strptime(entry3, '%H:%M:%S').time()
                    new_entry4 = datetime.datetime.strptime(entry4, '%H:%M:%S').time()
                    new_entry5 = datetime.datetime.strptime(entry5, '%H:%M:%S').time()
                    new_entry6 = datetime.datetime.strptime(entry6, '%H:%M:%S').time()
                except:
                    new_entry1 = datetime.datetime.strptime(entry1, '%H:%M').time()
                    new_entry2 = datetime.datetime.strptime(entry2, '%H:%M').time()
                    new_entry3 = datetime.datetime.strptime(entry3, '%H:%M').time()
                    new_entry4 = datetime.datetime.strptime(entry4, '%H:%M').time()
                    new_entry5 = datetime.datetime.strptime(entry5, '%H:%M').time()
                    new_entry6 = datetime.datetime.strptime(entry6, '%H:%M').time()
                new_weekday = weekdays[i]


                data = Availability(id=new_id, date=new_date, weekday=new_weekday, email=user.email,
                                    start_time=new_entry1, end_time=new_entry2, start_time2=new_entry3,
                                    end_time2=new_entry4, start_time3=new_entry5, end_time3=new_entry6,
                                    created_by=company_id, changed_by=company_id)


                db.session.add(data)
                db.session.commit()

    #Save templates
    if request.method == 'POST' and 'template' in request.form:
        for i in range(day_num):
            entry1 = request.form.get(f'day_{i}_0')
            entry2 = request.form.get(f'day_{i}_1')
            entry3 = request.form.get(f'day_{i}_2')
            entry4 = request.form.get(f'day_{i}_3')
            entry5 = request.form.get(f'day_{i}_4')
            entry6 = request.form.get(f'day_{i}_5')
            if entry1:
                last = TemplateAvailability.query.order_by(TemplateAvailability.id.desc()).first()
                if last is None:
                    new_id = 1000
                else:
                    new_id = last.id + 1
                new_name = planning_form.template_name.data
                new_date = monday + datetime.timedelta(days=i)
                new_entry1 = datetime.datetime.strptime(entry1, '%H:%M').time()
                new_entry2 = datetime.datetime.strptime(entry2, '%H:%M').time()
                new_entry3 = datetime.datetime.strptime(entry3, '%H:%M').time()
                new_entry4 = datetime.datetime.strptime(entry4, '%H:%M').time()
                new_entry5 = datetime.datetime.strptime(entry5, '%H:%M').time()
                new_entry6 = datetime.datetime.strptime(entry6, '%H:%M').time()
                new_weekday = weekdays[i]

                data = TemplateAvailability(id=new_id, template_name=new_name, date=new_date, weekday=new_weekday, email=user.email,
                                            start_time=new_entry1, end_time=new_entry2, start_time2=new_entry3,
                                            end_time2=new_entry4, start_time3=new_entry5, end_time3=new_entry6,
                                            created_by=company_id, changed_by=company_id)

                db.session.add(data)
                db.session.commit()

    #Update Planning - Still not working
    pass

    return render_template('planning.html', template_form=planning_form, monday=monday, weekdays=weekdays,
                           day_num=day_num)


@app.route('/delete_availability/<int:id>')
def delete_availability(id):
    account = User.query.get(current_user.id)
    user_form = UpdateForm(csrf_enabled=False, obj=account)
    remove = Availability.query.get(id)

    db.session.delete(remove)
    db.session.commit()
    flash('Successful')
    return render_template('user.html', available=Availability.query.filter_by(email=account.email),
                           account=account, template_form=user_form)

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
    weekdays = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    today = datetime.date.today()
    monday = today - datetime.timedelta(days=today.weekday())
    day_num = 7
    week_adjustment = session.get('week_adjustment', 0)
    user = User.query.get(current_user.id)
    company_id = current_user.company_id

    #Prev Week
    if time_form.prev_week.data:
        week_adjustment -=7
        session['week_adjustment'] = week_adjustment

        monday = monday + datetime.timedelta(days=week_adjustment)

        return render_template('admin.html', template_form=time_form, timedelta=timedelta, monday=monday,
                               Time=Time, weekdays=weekdays, day_num=day_num)
    #Next Week
    if time_form.next_week.data:
        week_adjustment +=7
        session['week_adjustment'] = week_adjustment

        monday = monday + datetime.timedelta(days=week_adjustment)

        return render_template('admin.html', template_form=time_form, timedelta=timedelta, monday=monday,
                               Time=Time, weekdays=weekdays, day_num=day_num)

    # Set Template
    if time_form.template1.data:
        temp_dict = {}
        for i in range(day_num):
            for hour in range(24):
                time_num = hour * 100
                time = f'{time_num:04d}'
                new_time = datetime.datetime.strptime(time, '%H%M').time()
                temp = TemplateTimeRequirement.query.filter_by(weekday=weekdays[i], start_time=new_time).first()
                if temp is None:
                    pass
                else:
                    new_i = i + 1
                    temp_dict[str(new_i) + '&' + str(hour)] = temp.worker

        return render_template('admin.html', template_form=time_form, timedelta=timedelta, monday=monday,
                               weekdays=weekdays, day_num=day_num, temp_dict=temp_dict)

    #Submit the required FTE per hour
    if request.method == 'POST' and 'submit' in request.form:
        for i in range(day_num):
            for hour in range(24):
                capacity = request.form.get(f'worker_{i}_{hour}')
                if capacity:
                    last = TimeReq.query.order_by(TimeReq.id.desc()).first()
                    if last is None:
                        new_id = 1000
                    else:
                        new_id = last.id + 1
                    new_date = monday + datetime.timedelta(days=i)
                    time_num = hour * 100
                    time = f'{time_num:04d}'
                    new_time = datetime.datetime.strptime(time, '%H%M').time()

                    req = TimeReq(id=new_id, date=new_date, start_time=new_time, worker=capacity, created_by=company_id,
                                  changed_by=company_id)

                    db.session.add(req)
                    db.session.commit()
        return render_template('admin.html', monday=monday, timedelta=timedelta, day_num=day_num, template_form=time_form)

    # Save templates
    if request.method == 'POST' and 'template' in request.form:
        for i in range(day_num):
            for hour in range(24):

                capacity = request.form.get(f'worker_{i}_{hour}')
                if capacity:
                    last = TemplateTimeRequirement.query.order_by(TemplateTimeRequirement.id.desc()).first()
                    if last is None:
                        new_id = 1000
                    else:
                        new_id = last.id + 1
                    new_name = time_form.template_name.data
                    new_date = monday + datetime.timedelta(days=i)
                    time_num = hour * 100
                    time = f'{time_num:04d}'
                    new_time = datetime.datetime.strptime(time, '%H%M').time()
                    new_weekday = weekdays[i]

                    data = TemplateTimeRequirement(id=new_id, template_name=new_name, date=new_date, weekday=new_weekday,
                                                   start_time=new_time, worker=capacity, created_by=company_id,
                                                   changed_by=company_id)

                    db.session.add(data)
                    db.session.commit()

    #Update TimeReq - Still not working
    pass

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


    return render_template('admin.html',  monday=monday, timedelta=timedelta, day_num=day_num, Time=Time, template_form=time_form)


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
    company_id = current_user.company_id

    temp_dict = {}
    for i in range(day_num):
        temp = OpeningHours.query.filter_by(weekday=weekdays[i]).first()
        if temp is None:
            pass
        else:
            new_i = i + 1
            temp_dict[str(new_i) + '&0'] = temp.start_time
            temp_dict[str(new_i) + '&1'] = temp.end_time

    #Save Opening
    if request.method == 'POST' and 'submit' in request.form:
        for i in range(day_num):
            entry1 = request.form.get(f'day_{i}_0')
            entry2 = request.form.get(f'day_{i}_1')
            if entry1:
                last = OpeningHours.query.order_by(OpeningHours.id.desc()).first()
                if last is None:
                    new_id = 1000
                else:
                    new_id = last.id + 1
                try:
                    new_entry1 = datetime.datetime.strptime(entry1, '%H:%M:%S').time()
                    new_entry2 = datetime.datetime.strptime(entry2, '%H:%M:%S').time()
                except:
                    new_entry1 = datetime.datetime.strptime(entry1, '%H:%M').time()
                    new_entry2 = datetime.datetime.strptime(entry2, '%H:%M').time()
                new_weekday = weekdays[i]


                data = OpeningHours(id=new_id, weekday=new_weekday, start_time=new_entry1,
                                    end_time=new_entry2, created_by=company_id, changed_by=company_id)


                db.session.add(data)
                db.session.commit()

    #Update Opening Hour - still not working
    if opening_form.update.data:
        try:
            for i in range(day_num):
                new_opening = OpeningHours.query.filter_by(id=i+1).first()
                entry1 = request.form.get(f'day_{i}_0')
                entry2 = request.form.get(f'day_{i}_1')
                new_start_time = datetime.datetime.strptime(entry1, '%H:%M:%S').time()
                new_end_time = datetime.datetime.strptime(entry2, '%H:%M:%S').time()
                new_opening.start_time = new_start_time
                new_opening.end_time = new_end_time
                db.session.commit()
                flash('Update successful submitted')
                return redirect(url_for('opening'))
        except:
            db.session.rollback()
            flash('Error occured :(')
            return redirect(url_for('opening'))

    return render_template('opening.html', template_form=opening_form, weekdays=weekdays, day_num=day_num, temp_dict=temp_dict)



if __name__ == '__main__':
    app.run()

