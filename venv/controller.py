from flask import Flask
from flask_bootstrap import Bootstrap
from authlib.integrations.flask_client import OAuth
from venv.views import views
from venv.auths import auths
from venv.keys import key1, key2, key3, key4, key5,key6, key7, key8, key9, key10, key11, key12
from venv.keys import key13, key14, key15, key16, key17, key18, key19, key20, key21, key22, key23
from flask_mail import Mail
from pytrends.request import TrendReq
from newsapi import NewsApiClient
from flask_apscheduler import APScheduler
import pandas as pd
import datetime
import pytz


app = Flask(__name__)

app.config['SECRET_KEY'] = 'ProjectBlueBook'
app.config['SCHEDULER_API_ENABLED'] = 'True'
app.config['SQLACHEMY_DATABASE_URI'] = 'postgres://adffdgsrywxhsa:d483d23a6d3ac240757343c3b1ab826b05e8211a219306a9b271da8b964ee6f7@ec2-54-174-31-7.compute-1.amazonaws.com:5432/ddi35hde1c4juj'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False

app.register_blueprint(views, url_prefix='/')
app.register_blueprint(auths, url_prefix='/')


Bootstrap(app)
oauth = OAuth(app)
mail = Mail(app)
scheduler = APScheduler()
scheduler.init_app(app)

from venv.models import User, Nw_Data, User_Activity, User_Message, User_Fr_List, Watch_List, Share_List, User_Bl_List


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
    return


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
        dt.append([nw.Title, nw.Desc, nw.Link, nw.id, nw.Likes])

    return dt

def User_Act_Add(u_id, det):
    act_dt = datetime.datetime.now(pytz.timezone('America/Montreal'))
    User_Activity.Add_Activity(u_id, act_dt, det)
    return

def User_Act_Get(u_id): 
    u_acts = User_Activity.Fetch_Activity(u_id)
    dt = []
    for u_act in u_acts:
        dt.append([u_act.det, u_act.act_dt])
    
    dt.reverse()
    return dt


def Send_Fr_Req(u_rec, u_send):
    msg = 'Please add me as a Friend'
    msg_tp = 1
    msg_res = 0
    User_Message.User_Add_Msg(u_rec,u_send, msg_tp, msg_res, msg)
    return

def Get_Fr_Req(u_id):
    dt = []
    u_reqs = User_Message.User_Pen_Req(u_id)

    for u_req in u_reqs:
        u_send = u_req.u_send
        u_detail = User.User_Details(u_send)
        u_s_name = u_detail[0]
        dt.append([u_send, u_s_name, u_req.id])
    
    return dt

def Decide_Fr_Req(msg_id, u_dec):
    msg_data = User_Message.Msg_Detail(msg_id)
    u_id = msg_data.u_rec
    u_fr = msg_data.u_send
    
    if u_dec == 1:
        User_Fr_List.User_Add_Fr(u_id, u_fr)
        User_Fr_List.User_Add_Fr(u_fr, u_id)
        User_Message.Msg_Update(msg_id)
    
    elif u_dec == 2:
        User_Bl_List.User_Block(u_id, u_fr)
        User_Bl_List.User_Block(u_fr, u_id)
        User_Message.Msg_Update(msg_id)

    else:
        User_Message.Msg_Update(msg_id)
    return

def Print_All_Msg():
    all_msgs = User_Message.Get_All_Msg()
    dt = []
    for all_msg in all_msgs:
        dt.append([all_msg.u_rec, all_msg.u_send,all_msg.msg_tp, all_msg.msg_res])
    return dt

def Print_All_Frd():
    all_frds = User_Fr_List.All_Fr_List()
    dt = []
    for all_frd in all_frds:
        dt.append([all_frd.id, all_frd.u_id, all_frd.u_fr])
    return dt


def Pr_User(u_id):
    u_datas = User.All_Data()
    dt = []
    ur = []
    fr_lt = []
    bl_lt = []
    nw_lt = []

    for u_data in u_datas:
        if u_data.id != u_id:
            dt.append([u_data.id, u_data.location, u_data.cat_1, u_data.cat_2, u_data.cat_3,0,u_data.uname])
            nw_lt.append([u_data.id])
        else:
            frs=u_data.u_fr
            blks=u_data.u_bk
            ur.append([u_data.id, u_data.location, u_data.cat_1, u_data.cat_2, u_data.cat_3])

    for fr in frs:
        fr_lt.append([fr.u_fr])

    for blk in blks:
        bl_lt.append([blk.u_bl])

    sz = len(dt)
    sz2 = len(fr_lt)
    sz3 = len(bl_lt)

    for x in range(sz):
        frd_ind = 0
        for y in range(1, 5):
            print(dt[x][y])
            if ur[0][1] == dt[x][y]:
                frd_ind += 1
            elif ur[0][2] == dt[x][y]:
                frd_ind += 1
            elif ur[0][3] == dt[x][y]:
                frd_ind += 1
            elif ur[0][4] == dt[x][y]:
                frd_ind += 1
        dt[x][5] = frd_ind
    print(dt)

    for x in range(sz):
        for y in range(sz2):
            if nw_lt[x]==fr_lt[y]:
                dt[x][0]=0
                break

    for x in range(sz):
        for y in range(sz3):
            if nw_lt[x]==bl_lt[y]:
                dt[x][0]=0
                break


    dt.sort(key=lambda tup:tup[5], reverse=True)
    print(dt)
    return dt


def Fetch_Fr_List(u_id):
    u_data = User.Fr_List(u_id)
    frs = u_data.u_fr
    dt = []
    for fr in frs:
        fr_id = fr.u_fr
        fr_detail = User.User_Details(fr_id)
        dt.append([fr_id, fr_detail[0]])

    return dt

def Send_Fr_Msg(u_send, u_rec, msg):
    msg_tp = 2
    msg_res = 0
    User_Message.User_Add_Msg(u_rec, u_send, msg_tp, msg_res, msg)
    return

def Get_Fr_Msg(u_id):
    dt = []
    u_msgs = User_Message.User_Pen_Msg(u_id)

    for u_msg in u_msgs:
        u_send = u_msg.u_send
        u_detail = User.User_Details(u_send)
        u_s_name = u_detail[0]
        dt.append([u_send, u_s_name, u_msg.msg, u_msg.id])

    return dt

def Mark_Read(msg_id):
    User_Message.Msg_Update(msg_id)
    return


def Friends_Fr_List(u_id):
    u_data = User.Fr_List(u_id)
    frs = u_data.u_fr
    dt = []
    for fr in frs:
        fr_id = fr.u_fr
        if fr_id != u_id:
            fr_data = User.Fr_List(fr_id)
            fr_frs = fr_data.u_fr
            for fr_fr in fr_frs:
                fr_fr_id = fr_fr.u_fr
                if fr_fr_id != u_id:
                    fr_detail = User.User_Details(fr_fr_id)
                    dt.append([fr_fr_id, fr_detail[0]])
    return dt


def Add_to_Wlist(u_id,nw_id):
    Watch_List.Read_News(u_id,nw_id)
    return


def Add_to_Slist(u_id,nw_id):
    Share_List.Share_News(u_id,nw_id)
    return


def Fetch_Watch_List(u_id):
    datas = Watch_List.U_Wlist(u_id)
    dt = []
    for data in datas:
        nw_id = data.nw_id
        nw = Nw_Data.Get_News(nw_id)
        dt.append([nw.Title, nw.Desc, nw.Link, nw.id, nw.Likes])
    return dt


def Nw_Add_Like(nw_id):
    Nw_Data.Add_Like(nw_id)
    return

def Fetch_Recomm_List(u_id):
    u_data = User.Fr_List(u_id)
    frs = u_data.u_fr
    dt = []
    for fr in frs:
        fr_id = fr.u_fr
        sr_nws = Share_List.Get_Shared_News(fr_id)
        for sr in sr_nws:
            nw_id = sr.nw_id
            nw = Nw_Data.Get_News(nw_id)
            dt.append([nw.Title, nw.Desc, nw.Link, nw.id, nw.Likes])
    return dt


def news_fetch1(cat, loc, key):
    nw_dt = datetime.datetime.now()
    nw_dt = nw_dt.date()

    newsapi = NewsApiClient(api_key=key)

    pytrend = TrendReq()
    tr_keys = pytrend.trending_searches(loc)
    x1 = len(tr_keys)

    for x in range(x1):
        kw4 = tr_keys.iloc[x, 0]
        print(kw4)
        nw_key = newsapi.get_top_headlines(q=kw4, category=cat, language='en')
        nw_art = nw_key['articles']
        nw_art_sz = len(nw_art)
        if nw_art_sz != 0:
            for i in range(nw_art_sz):
                nw_t = nw_art[i]['title']
                nw_desc = nw_art[i]['description']
                nw_link = nw_art[i]['url']
                print(nw_t)
                print(nw_desc)
                print(nw_link)
                if nw_desc:
                    if nw_link:
                        with app.app_context():
                            nw_likes = 0
                            Nw_Data.Add_News(cat, loc, nw_dt, nw_t, nw_desc, nw_link, nw_likes)
                        print('added')

  
    print('Successfully updated NEWS database with country: ', loc, ' and category: ', cat)


@scheduler.task('cron', id='1', hour='11', minute='00')
def news_fetch_sch():
    news_fetch1('entertainment', 'australia', key1)
    news_fetch1('business', 'australia', key1)
    news_fetch1('sports', 'australia', key2)
    news_fetch1('health', 'australia', key2)
    news_fetch1('science', 'australia', key3)
    news_fetch1('technology', 'australia', key3)
    news_fetch1('entertainment', 'canada', key4)
    news_fetch1('business', 'canada', key4)
    news_fetch1('sports', 'canada', key5)
    news_fetch1('health', 'canada', key5)
    news_fetch1('technology', 'canada', key6)
    news_fetch1('science', 'canada', key6)
    news_fetch1('entertainment', 'india', key7)
    news_fetch1('business', 'india', key7)
    news_fetch1('sports', 'india', key8)
    news_fetch1('health', 'india', key8)
    news_fetch1('technology', 'india', key9)
    news_fetch1('science', 'india', key9)
    news_fetch1('entertainment', 'united_kingdom', key10)
    news_fetch1('business', 'united_kingdom', key10)
    news_fetch1('sports', 'united_kingdom', key11)
    news_fetch1('health', 'united_kingdom', key11)
    news_fetch1('technology', 'united_kingdom', key12)
    news_fetch1('science', 'united_kingdom', key12)
    news_fetch1('entertainment', 'united_states', key13)
    news_fetch1('business', 'united_states', key13)
    news_fetch1('sports', 'united_states', key14)
    news_fetch1('health', 'united_states', key14)
    news_fetch1('technology', 'united_states', key15)
    news_fetch1('science', 'united_states', key15)
    news_fetch1('entertainment', 'italy', key16)
    news_fetch1('business', 'italy', key16)
    news_fetch1('sports', 'italy', key17)
    news_fetch1('health', 'italy', key17)
    news_fetch1('technology', 'italy', key18)
    news_fetch1('science', 'italy', key18)
    news_fetch1('entertainment', 'germany', key19)
    news_fetch1('business', 'germany', key19)
    news_fetch1('sports', 'germany', key20)
    news_fetch1('health', 'germany', key20)
    news_fetch1('technology', 'germany', key21)
    news_fetch1('science', 'germany', key21)

scheduler.start()
