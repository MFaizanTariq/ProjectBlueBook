from flask import Blueprint, render_template, request, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
import datetime

views = Blueprint('views', __name__)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired()])
    remember = BooleanField('Remember me')

@views.route('/')
def index():
    return render_template('index.html')

@views.route('/login', methods=['GET', 'POST'])
def login():
    from venv.controller import Validate_User
    form = LoginForm()
    if request.method == "POST":
        uname = form.username.data
        password = form.password.data
        u_id = Validate_User(uname, password)
        print(u_id)
        if not u_id == 0:
            session["u_id"] = u_id
            return redirect(url_for("views.main_page"))
        else:
            print("Incorrect credentials")
            msg = 'Incorrect credentials'
            return render_template('login.html', form=form, message=msg)

    return render_template('login.html', form=form)


@views.route('/choice', methods=['GET', 'POST'])
def choice():
    from venv.controller import Cat_Update, Validate_User
    uname = session["uname"]
    password = session["password"]
    session ["u_id"] = Validate_User(uname, password)

    if request.method == 'POST':
        cat1 = request.form['cat-1']
        cat2 = request.form['cat-2']
        cat3 = request.form['cat-3']
        nw_per_page = request.form['newslmt']
        Cat_Update(uname, password, nw_per_page, cat1, cat2, cat3)
        return redirect(url_for("views.main_page"))
    return render_template('choice.html')

@views.route("/main_page", methods=['GET', 'POST'])
def main_page():
    from venv.controller import User_News, User_Data, User_Act_Add
    u_id = session["u_id"]
    user_data = User_Data(u_id)
    User_Act_Add(u_id,'Successful Login')
    
    nw1 = User_News(user_data[5], user_data[6])
    nw1.reverse()

    nw2 = User_News(user_data[5], user_data[7])
    nw2.reverse()

    nw3 = User_News(user_data[5], user_data[8])
    nw3.reverse()

    nw_lmt = int(user_data[9])

    size_nw1 = len(nw1)
    if size_nw1 > nw_lmt:
        size_nw1 = nw_lmt
    size_nw2 = len(nw2)
    if size_nw2 > nw_lmt:
        size_nw2 = nw_lmt
    size_nw3 = len(nw3)
    if size_nw3 > nw_lmt:
        size_nw3 = nw_lmt


    return render_template('main_page.html', Title1=nw1, Sz1=size_nw1, Title2=nw2, Sz2=size_nw2, Title3=nw3,
                           Sz3=size_nw3,Cat1=user_data[6], Cat2=user_data[7], Cat3=user_data[8])


@views.route("/profile", methods=['GET', 'POST'])
def profile_update():
    from venv.controller import User_Data, Cat_Update, User_Act_Add, Get_Fr_Req
    u_id = session["u_id"]
    user_data = User_Data(u_id)
    u_reqs = Get_Fr_Req(u_id)
    Sz = len(u_reqs)
    if request.method == 'POST':
        cat1 = request.form['cat-1']
        cat2 = request.form['cat-2']
        cat3 = request.form['cat-3']
        nw_per_page = request.form['newslmt']
        Cat_Update (user_data[0], user_data[1], nw_per_page, cat1, cat2, cat3)
        msg = 'Categories successfully updated'
        User_Act_Add(u_id,msg)
        return render_template('profile_update.html', username=user_data[0], email=user_data[4], firstname=user_data[2],
                lastname=user_data[3], country=user_data[5], cat1=cat1, cat2=cat2, cat3=cat3, message=msg)

        
    return render_template('profile_update.html', username=user_data[0], email=user_data[4], firstname=user_data[2],
        lastname=user_data[3], country=user_data[5], cat1=user_data[6], cat2=user_data[7], cat3=user_data[8], sz=Sz, ureq=u_reqs)


@views.route("/profile2", methods=['GET', 'POST'])
def profile_update2():
    from venv.controller import User_Data, User_Update, User_Act_Add
    u_id = session["u_id"]
    user_data = User_Data(u_id)
    if request.method == 'POST':
        nw_firstname = request.form['firstname']
        nw_lastname = request.form['lastname']
        nw_country = request.form['country']
        User_Update(u_id, nw_firstname, nw_lastname, nw_country)
        msg = 'User details successfully updated!!!'
        User_Act_Add(u_id, msg)
        return render_template('profile_update.html', username=user_data[0], email=user_data[4], firstname=nw_firstname,
                lastname=nw_lastname, country=nw_country, cat1=user_data[6], cat2=user_data[7], cat3=user_data[8], message=msg)

    return render_template('profile_update.html', username=user_data[0], email=user_data[4], firstname=user_data[2],
                lastname=user_data[3], country=user_data[5], cat1=user_data[6], cat2=user_data[7], cat3=user_data[8])

@views.route('/send_fr_req', methods=['GET', 'POST'])
def send_fr_req():
    from venv.controller import User_Act_Add, Send_Fr_Req
    u_send = session["u_id"]
    u_rec = int(request.form["u_fr"])
    if request.method == 'POST':
        msg='Friend request sent'
        Send_Fr_Req(u_rec, u_send)
        User_Act_Add(u_send, msg)
        return render_template('messages.html', message=msg)

    return redirect(url_for("views.messages"))


@views.route('/messages', methods=['GET', 'POST'])
def messages():
    from venv.controller import User_Data, Get_Fr_Req, Pr_User
    u_id = session["u_id"]
    user_data = User_Data(u_id)
    u_reqs = Get_Fr_Req(u_id)
    Sz1 = len(u_reqs)
    s_reqs = Pr_User(u_id)
    Sz2 = len(s_reqs)

    if Sz2 > 5:
        Sz2 = 5

    return render_template('messages.html', Sz1=Sz1, ureq=u_reqs, Sz2=Sz2, sreq=s_reqs)

@views.route('/accept_req', methods=['GET', 'POST'])
def accept_req():
    from venv.controller import Decide_Fr_Req, User_Act_Add
    u_id = session["u_id"]

    if request.method == 'POST':
        msg_id = int(request.form['decision'])
        u_dec = 1
        Decide_Fr_Req(msg_id, u_dec)
        msg = "Accepted Friend Request"
        User_Act_Add(u_id, msg)
        return render_template('messages.html', message=msg)

    return redirect(url_for("views.messages"))

@views.route('/reject_req', methods=['GET', 'POST'])
def reject_req():
    from venv.controller import Decide_Fr_Req, User_Act_Add
    u_id = session["u_id"]

    if request.method == 'POST':
        msg_id = int(request.form['decision'])
        u_dec = 0
        Decide_Fr_Req(msg_id, u_dec)
        msg = "Rejected Friend Request"
        User_Act_Add(u_id, msg)
        return render_template('messages.html', message=msg)

    return redirect(url_for("views.messages"))

@views.route('/send_invite', methods=['GET', 'POST'])
def send_invite():
    from venv.controller import app, mail
    fr_mail = request.form['email']
    email = session['email']
    passwrd = request.form['pass']
    app.config['MAIL_USERNAME'] = email
    app.config['MAIL_PASSWORD'] = passwrd
    mail = Mail(app)

    if request.method == 'POST':
        msg = Message("Project BlueBook invite", sender=email, recipients=[fr_mail])
        msg.body = "Hey There, inviting you to the BlueBook web application @ bluebookcanada.herokuapp.com, JOIN TODAY!!!)"
        mail.send(msg)
        msg1='Invite email sent successfully'
        return render_template('profile_update.html', message=msg1)

    return redirect(url_for("views.profile_update"))



@views.route("/logout")
def logout():
    from venv.controller import User_Act_Add
    u_id = session["u_id"]
    User_Act_Add(u_id,'Logout')
    session.clear()
    return redirect(url_for("views.index"))