from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app  = Flask(__name__)
 
app.config['SECRET_KEY'] = '5bea12aecb8640f427d035193b6f7670'
 
 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://gmsucprazblqpk:e69554b485ca09626dbfa172848b1a34cfa2b7b5ff8004f893e1089fccb2c57e@ec2-44-193-178-122.compute-1.amazonaws.com:5432/de9r775n46n148'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from santa import routes