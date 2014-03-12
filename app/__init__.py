from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

try:
    app.config.from_object('config') # config.py is supposed to be put in root of application
except Exception:
    pass

db = SQLAlchemy(app)

from app import routes, models, forms