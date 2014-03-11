from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(32), unique=True)
	email = db.Column(db.String(254), unique=True)
	passwordHash = db.Column(db.String(160))

	def __init__(self, uName, eMail, pWord):
		self.username = uName
		self.email = eMail
		self.setPass(pWord)

	def setPass(self, pWord):
		self.passwordHash = generate_password_hash(pWord)

	def checkPass(self, pWord):
		return check_password_hash(self.passwordHash, pWord)

	def __repr__(self):
		return "<User %r>" % self.username

class Game(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), unique=True)

	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return "<Game %r>" % self.name

