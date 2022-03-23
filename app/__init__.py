# Every level/folder of a Python application has an __init__.py file. 
# The purpose of this file is to connect the levels
# of the app to each other. 
from mongoengine import connect
from flask import Flask
import os
from flask_moment import Moment
import base64
from flask_login import LoginManager
from flask_mail import Mail
import certifi

app = Flask(__name__)
#app.jinja_options['extensions'].append('jinja2.ext.do')
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY") or os.urandom(20)

from app.utils.secrets import getSecrets

secrets = getSecrets()

connect(secrets['MONGO_DB_NAME'], host=secrets['MONGO_HOST'], tlsCAFile=certifi.where())
moment = Moment(app)

login = LoginManager(app)
login.login_view = 'login'

app.config.update(dict(
   DEBUG = True,
   MAIL_SERVER = 'smtp.googlemail.com',
   MAIL_PORT = 587,
   MAIL_USE_TLS = 1,
   MAIL_USE_SSL = 0,
   MAIL_USERNAME = secrets['MAIL_USERNAME'],
   MAIL_PASSWORD = secrets['MAIL_PASSWORD']
))

mail = Mail(app)

def base64encode(img):
    image = base64.b64encode(img)
    image = image.decode('utf-8')
    return image

app.jinja_env.globals.update(base64encode=base64encode)

from .routes import *