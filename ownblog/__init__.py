from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app= Flask(__name__)
app.config['SECRET_KEY']='meowmeow'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
bcrypt= Bcrypt(app)

db = SQLAlchemy(app)
login_manager= LoginManager(app)

from ownblog import routes
from ownblog.models import User,Post


admin= Admin(app)
admin.add_view(ModelView(User,db.session))
admin.add_view(ModelView(Post,db.session))