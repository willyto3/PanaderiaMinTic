# import flask and sqlaclhemy
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_manager, login_required, login_user, logout_user, current_user

app = Flask(__name__)

# app configuration
UPLOADE_FOLDER = 'panaderia/static/uploads/'
app.config["SECRET_KEY"] = 'Es un Secreto'
app.config["UPLOAD_FOLDER"]= UPLOADE_FOLDER
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database\panaderia.db'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from panaderia import views
from panaderia import models