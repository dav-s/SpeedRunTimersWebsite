from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config') # config.py is supposed to be put in root of application
db = SQLAlchemy(app)

from app import routes, models