# import flask and sqlaclhemy
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_manager


app = Flask(__name__)

# app configuration
UPLOADE_FOLDER = 'panaderia/static/uploads/'
app.config["SECRET_KEY"] = 'Es un Secreto'
app.config["UPLOAD_FOLDER"]= UPLOADE_FOLDER
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database\panaderia.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)

from panaderia import views
from panaderia import models