from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    email = db.Column(db.String(254), unique=True)
    password_hash = db.Column(db.String(160))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)


    def __repr__(self):
        return "<User %r>" % self.username


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Game %r>" % self.name


class Split(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    game_id = db.Column(db.Integer, db.ForeignKey("game.id"))
    game = db.relationship("Game",
                           backref=db.backref("splits", lazy="dynamic"))

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User",
                           backref=db.backref("splits", lazy="dynamic"))

    def __init__(self, title, game, user):
        self.title = title
        self.game = game
        self.user = user

