from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app= Flask(__name__)
app.config['SECRET_KEY']='meowmeow'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
bcrypt= Bcrypt(app)

db = SQLAlchemy(app)
login_manager= LoginManager(app)

from ownblog import routes
from ownblog.models import User