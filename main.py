from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_mysqldb import MySQL
from user import User
from model_user import ModelUser
from connection import config
from datetime import datetime as dt
from get_hours_available import AvailableSchedule

# IMPORT CLASES:
from patient_history import PatientHistory
from create_account import CreateAccount

app = Flask(__name__)

# DB
database = MySQL(app)
login_manager = LoginManager(app)

# USER LOGGED
class Logged:
    patient_id = 0
    patient_name = ""
    patient_username = ""
    patient_room = 0

@login_manager.user_loader
def load_user(user_id):
    return ModelUser.get_by_id(database, user_id)

#************************************************************************************************


@app.route('/', methods=['GET','POST'])
def index():
    try:
        if request.method == 'POST':
            usr = request.form['myUser']
            psw = request.form['myPass']

            user = User(None, usr, None, None, None, psw)
            logged_user = ModelUser.login(database, user)
            
            if logged_user != None:
                if logged_user.password:
                    Logged.patient_id = logged_user.id
                    Logged.patient_name = logged_user.name
                    Logged.patient_username = logged_user.username
                    Logged.patient_room = logged_user.room

                    login_user(logged_user)
                    return redirect(url_for('profile'))
                else:
                    flash("Wrong keys")
                    return render_template('index.html')
            else:
                flash("Wrong keys")
                return render_template('index.html')
        return render_template('index.html')
    except:
        flash("Empty fields...")
        return render_template('index.html')



@app.route('/signin', methods=['GET','POST'])
def sign_in():
    if request.method == 'POST':
        user = request.form['user']
        name = request.form['user_name']
        date = request.form['user_date']
        room = request.form['user_room']
        password = request.form['password']

        check = CreateAccount.check_user(database, user)

        if check:
            return render_template('sign_in.html', dnp=check)
        else:
            CreateAccount.create_account(database, user, name,
                                                date, room, password)
            
            return render_template('signed_in.html')
    
    return render_template('sign_in.html')



@app.route('/profile', methods=['GET','POST'])
@login_required
def profile():
    if request.method == 'POST':
        condition = request.form['myCondition']
        if condition == "Cancelation":
            get_id = Logged.patient_id
            get_date = request.form['myDates']
            get_hour = request.form['myHour']
            try:
                cursor = database.connection.cursor()
                cursor.execute(f"DELETE FROM medical_appointment WHERE (id={get_id} AND appt_date='{get_date}' AND appt_hour='{get_hour}')")
                database.connection.commit()

                return render_template('appt_sent.html', cs="cancelled")

            except:
                result = "Something wrong happened! You will be redirected to your profile. Thank you"

                return render_template('cancel_sent.html', msg=result)

    id = Logged.patient_id
    room = Logged.patient_room

    pt_history = PatientHistory()
    data_history = pt_history.patient_history(database, id, room)

    return render_template('profile.html', data=data_history)



@app.route('/add', methods=['GET','POST'])
@login_required
def add_patient():
    try:
        if request.method == 'POST':
            get_date = request.form['pt_date']
            get_reason = request.form['reason'].upper()
            room = Logged.patient_room

            search_hours = AvailableSchedule()
            hours = search_hours.making_appointment(database, room, get_date)

            current_date = dt.now()
            cur_date_string = dt.strftime(current_date, "%Y-%m-%d")

            hours_available = len(hours)

            date_time = True
            display_table = True

            return render_template('add.html', cd=cur_date_string,
                                                date=get_date,
                                                rsn=get_reason,
                                                show_date=date_time, 
                                                display=display_table,
                                                qty=hours_available,
                                                hr=hours)
    except:
        pass

    current_date = dt.now()
    cur_date_string = dt.strftime(current_date, "%Y-%m-%d")

    date_time = False
    display_table = False

    return render_template('add.html', cd=cur_date_string,
                                    show_date=date_time,
                                    display=display_table)



@app.route('/sent', methods=['GET','POST'])
@login_required
def appt_sent():
    if request.method == 'POST':
        get_date = request.form['new_date']
        get_reason = request.form['new_reason']
        get_hour = request.form['one']
        
        cursor = database.connection.cursor()
        cursor.execute(f"""INSERT INTO medical_appointment 
                       (id, pt_name, reason, appt_date, appt_hour, room)
                    VALUES ({Logged.patient_id},'{Logged.patient_name}','{get_reason}',
                    '{get_date}','{get_hour}',{Logged.patient_room})""")
        database.connection.commit()

        return render_template('appt_sent.html', cs="sent")
    
    else:
        return f"<h1>SOMETHING WENT WRONG...</h1>"


@app.route('/logout')
def logout():
    Logged.patient_id = 0
    Logged.patient_username = ""
    Logged.patient_room = 0

    session.clear()
    logout_user()
    return redirect(url_for('index'))



if __name__=='__main__':
    app.config.from_object(config['development'])
    app.run()