from flask_sqlalchemy import SQLAlchemy
from venv.controller import app
from os import path

DB_NAME = "nw_db.db"
db = SQLAlchemy()
app.config['SECRET_KEY'] = 'EMS'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

db.init_app(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(25), nullable=False)
    fullname = db.Column(db.String(25), nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(25), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    nw_per_page = db.Column(db.Integer, nullable=False)
    cat_1 = db.Column(db.String(15), nullable=False)
    cat_2 = db.Column(db.String(15), nullable=False)
    cat_3 = db.Column(db.String(15), nullable=False)
    u_act = db.relationship('User_Activity', backref=db.backref('user'))

    def Add_User(uname, fullname, firstname, lastname, email, password, location, nw_per_page, cat_1, cat_2, cat_3):
        new_user = User(uname=uname, fullname=fullname, firstname=firstname, lastname=lastname, email=email, 
            password=password, location=location, nw_per_page=nw_per_page, cat_1=cat_1, cat_2=cat_2, cat_3=cat_3)
        db.session.add(new_user)
        db.session.commit()
    
    def Chk_Uname(uname):
        u_name = db.session.query(User).filter(User.uname == uname).first()
        if u_name:
            return 0
        else:
            return 1

    def Chk_Email(email):
        uemail = db.session.query(User).filter(User.email == email).first()
        if uemail:
            return 0
        else:
            return 1
        
    def Check_Pass(uname, password):
        u_data = db.session.query(User).filter(User.uname == uname, User.password == password).first()
        if u_data:
            return u_data.id
        else:
            return 0

    def User_Details(u_id):
        u_data = db.session.query(User).filter(User.id == u_id).first()
        uname = u_data.uname
        password = u_data.password
        email = u_data.email
        fullname = u_data.fullname
        firstname = u_data.firstname
        lastname = u_data.lastname
        location = u_data.location
        return uname, password, firstname, lastname, email, location

    def User_Cat(u_id):
        u_data = db.session.query(User).filter(User.id == u_id).first()
        cat_1 = u_data.cat_1
        cat_2 = u_data.cat_2
        cat_3 = u_data.cat_3
        nw_per_pg = u_data.nw_per_page
        return cat_1, cat_2, cat_3, nw_per_pg

    def Update_Cat(u_id, nw_per_page, cat_1, cat_2, cat_3):
        db.session.query(User).filter(User.id == u_id).update({'nw_per_page':nw_per_page, 'cat_1' : cat_1, 'cat_2' : cat_2, 'cat_3' : cat_3})
        db.session.commit()
        return

    def Update_User(u_id, firstname, lastname, location):
        db.session.query(User).filter(User.id == u_id).update({'firstname':firstname, 'lastname' : lastname, 'location' : location})
        db.session.commit()
        return

class Nw_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Category = db.Column(db.String(25), nullable=False)
    Country = db.Column(db.String(25), nullable=False)
    Nw_date = db.Column(db.Date, nullable=False)
    Title = db.Column(db.String(100), nullable=False)
    Desc = db.Column(db.String(250), nullable=False)
    Link = db.Column(db.String(100))

    def News_Fetch(Country, Category):
        news = db.session.query(Nw_Data).filter(Nw_Data.Country == Country, Nw_Data.Category == Category)
        return news
    
    def Add_News(Category, Country, Nw_date, Title, Desc, Link):
        news = Nw_Data(Category=Category, Country=Country, Nw_date=Nw_date, Title=Title, Desc=Desc, Link=Link) 
        db.session.add(news)
        db.session.commit()

class User_Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    u_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    act_dt = db.Column(db.DateTime, nullable=False)
    det = db.Column(db.String(100), nullable=False)
    
    def Add_Activity(u_id, act_dt, det):
        nw_act = User_Activity(u_id=u_id, act_dt=act_dt, det=det)
        db.session.add(nw_act)
        db.session.commit()


if not path.exists('instance/' + DB_NAME):
   with app.app_context():
        db.create_all()
        print('Created Database!')
        