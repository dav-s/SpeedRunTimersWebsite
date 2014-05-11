from app import db
import json
from werkzeug.security import generate_password_hash, check_password_hash
import _md5, os

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(254))
    password_hash = db.Column(db.String(160))

    def __init__(self, username, email, password):
        self.username = username
        self.change_email(email)
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_md5_email(self):
        return _md5.new(self.email).hexdigest()

    def change_email(self, email):
        self.email = email.strip().lower()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def get_gravatar_url(self, size=None):
        if(size):
            return "http://gravatar.com/avatar/%s.jpg?d=retro&s=%s" % (self.get_md5_email(), size)
        return "http://gravatar.com/avatar/%s.jpg?d=retro" % (self.get_md5_email())

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

    def __init__(self, name, game, user):
        self.name = name
        self.game = game
        self.user = user

    def write_file(self, contents):
        path = "generated/splits/"
        if not os.path.exists(path):
            os.makedirs(path)
        fname = "%s.splt" % (self.id)
        f = open(os.path.join(path, fname), "w+")
        f.write(contents)
        f.close()

    def get_file_array(self):
        path = os.path.join("generated/splits/", ("%s.splt" % self.id))
        if not os.path.exists(path):
            return None
        f = open(path)
        resp = f.read()
        f.close()
        lines = resp.splitlines()
        return [(lines[i], lines[i+1]) for i in range(1, int(lines[0])*2, 2)]

    def file_to_dict(self):
        fa = self.get_file_array()
        return [dict(name=l[0], time=l[1]) for l in fa]

    def __repr__(self):
        return "<Split %r>" % self.name


class Race(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    finished = db.Column(db.Boolean)

    split_id = db.Column(db.Integer, db.ForeignKey("split.id"))
    split = db.relationship("Split",
                            backref=db.backref("races", lazy="dynamic"))

    def __init__(self, split):
        self.split = split
        self.finished = False


