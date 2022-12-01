from flask import Blueprint, render_template, session, redirect, request, url_for
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from pip._vendor import cachecontrol
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
import google.auth.transport.requests
import os
import pathlib
import requests

auths = Blueprint('auths', __name__)

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
google_client_id = "34999991030-aqbafnvun525nhodv9kjsl1b33n7do92.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="https://bluebookcanada.herokuapp.com/callback"
)

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    fullname = StringField('Full Name', validators=[InputRequired()])
    firstname = StringField('First Name', validators=[InputRequired()])
    lastname = StringField('Last Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    location = StringField('Country', validators=[InputRequired()])


@auths.route("/signup", methods=['GET', 'POST'])
def signup():
    return render_template('signupuption.html')

@auths.route("/signup_google")
def signup_google():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@auths.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=google_client_id
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    session["email"] = id_info.get("email")
    return redirect("/protected_area")

@auths.route("/protected_area", methods=['GET', 'POST'])
def protected_area():
    from venv.controller import User_Pre_Req, Add_Def_User
    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)
    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=google_client_id
    )
    str(id_info)
    print(id_info['given_name'])

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    session["email"] = id_info.get("email")

    form = RegisterForm()
    if request.method == "POST":
        uname = form.username.data
        fullname = session["name"]
        email = session["email"]
        firstname = form.firstname.data
        lastname = form.lastname.data
        password = form.password.data
        location = form.location.data
        msg = User_Pre_Req(uname, email)
        if msg == " ":
            Add_Def_User(uname, fullname, firstname, lastname, email, password, location)
            session["uname"] = uname
            session["password"] = password
            return redirect(url_for("views.choice"))
        else:
            return render_template('signup.html', form=form, message=msg)

    return render_template('signup.html', form=form)


@auths.route('/signup_facebook')
def signup_facebook():
    from venv.controller import oauth

    oauth.register(
        name='facebook',
        client_id='628408715694502',
        client_secret='9e64fe0d94db22cb7517074b7bc38c0d',
        access_token_url='https://graph.facebook.com/oauth/access_token',
        access_token_params=None,
        authorize_url='https://www.facebook.com/dialog/oauth',
        authorize_params=None,
        api_base_url='https://graph.facebook.com/',
        client_kwargs={'scope': 'email'},
    )
    redirect_uri = url_for('auths.facebook_auth', _external=True)
    return oauth.facebook.authorize_redirect(redirect_uri)

@auths.route('/facebook/auth/')
def facebook_auth():
    from venv.controller import oauth
    token = oauth.facebook.authorize_access_token()

    resp = oauth.facebook.get(
        'https://graph.facebook.com/me?fields=id,name,email,picture{url}')
    profile = resp.json()

    session["name"] = profile['name']
    session["email"] = profile['email']

    return redirect("/protected_area2")

@auths.route("/protected_area2", methods=['GET', 'POST'])
def protected_area2():
    from venv.controller import User_Pre_Req, Add_Def_User
    form = RegisterForm()
    if request.method == "POST":
        uname = form.username.data
        fullname = session["name"]
        email = session["email"]
        firstname = form.firstname.data
        lastname = form.lastname.data
        password = form.password.data
        location = form.location.data
        msg = User_Pre_Req(uname, email)
        if msg == " ":
            Add_Def_User(uname, fullname, firstname, lastname, email, password, location)
            session["uname"] = uname
            session["password"] = password
            return redirect(url_for("views.choice"))
        else:
            return render_template('signup2.html', form=form, message=msg)

    return render_template('signup2.html', form=form)
