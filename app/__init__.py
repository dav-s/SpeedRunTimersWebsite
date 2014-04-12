from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

app = Flask(__name__)

try:
    app.config.from_object('config')  # config.py is supposed to be put in root of application
except Exception:
    pass

db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = "login"

from app import routes, models, forms