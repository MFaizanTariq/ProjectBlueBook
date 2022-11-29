from flask import Flask
from flask_bootstrap import Bootstrap
from venv.views import views
from venv.auths import auths
import datetime
import pytz

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'ProjectBlueBook'
app.register_blueprint(views, url_prefix='/')
app.register_blueprint(auths, url_prefix='/')

from venv.models import User, Nw_Data, User_Activity, User_Message

def User_Pre_Req(uname, email):
    msg_uname = 'Username aready exists'
    msg_email = 'Email already exists'
    chk_1 = User.Chk_Uname(uname)
    chk_2 = User.Chk_Email(email)
    if chk_1 == 1:
        msg_uname = ''
    if chk_2 == 1:
        msg_email = ''
    msg = msg_uname + " " + msg_email
    return msg

def Add_Def_User(uname, fullname, firstname, lastname, email, password, location):
    def_nw_pp = 10
    def_cat_1 = ' '
    def_cat_2 = ' '
    def_cat_3 = ' '

    User.Add_User(uname, fullname, firstname, lastname, email, password, location, def_nw_pp,
             def_cat_1, def_cat_2, def_cat_3)

def User_Data(u_id):
    cat = User.User_Cat(u_id)
    u_detail = User.User_Details(u_id)
    return u_detail[0], u_detail[1], u_detail[2], u_detail[3], u_detail[4], u_detail[5], cat[0], cat[1], cat[2], cat[3]

def Cat_Update(uname, password, nw_per_page, cat_1, cat_2, cat_3):
    u_id = User.Check_Pass(uname, password)
    User.Update_Cat(u_id, nw_per_page, cat_1, cat_2, cat_3)
    return

def Validate_User(uname, password):
    u_id = User.Check_Pass(uname, password)
    return u_id

def User_Update(u_id, firstname, lastname, location):
    User.Update_User(u_id, firstname, lastname, location)
    return

def User_News(country, cat_1):
    dt = []
    nws = Nw_Data.News_Fetch(country, cat_1)
    for nw in nws:
        dt.append([nw.Title, nw.Desc, nw.Link])

    return dt

def User_Act_Add(u_id, det):
    act_dt = datetime.datetime.now(pytz.timezone('America/Montreal'))
    User_Activity.Add_Activity(u_id, act_dt, det)
    return

def Send_Fr_Req(u_rec, u_send):
    msg = 'Please add me as a Friend'
    msg_tp = 1
    msg_res = 0
    User_Message.User_Add_Msg(u_rec,u_send, msg_tp, msg_res, msg)
    return