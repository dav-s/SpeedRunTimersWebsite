from app import app, lm, db
from flask import request, render_template, flash, redirect, url_for, jsonify, g, session, Markup
from flask.ext.login import login_user, logout_user, current_user
from forms import LoginForm, SignupForm, ContactForm, GameSubmitForm
from models import User, Game, Split
from sqlalchemy import func

navigationBar = [{"title": "Get it",  "mName": "getit"},
                 {"title": "About",   "mName": "about"},
                 {"title": "Contact", "mName": "contact"},
                 {"title": "Users",   "mName": "users"},
                 {"title": "Splits",  "mName": "splits"},
                 {"title": "Games",   "mName": "games"}]


@app.context_processor
def inject_global_variables():
    return dict(nBar=navigationBar)


# Before Hand

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user

# Errors

def flash_errors(form):
    for name, errors in form.errors.iteritems():
        for error in errors:
            flash("%s" % error, "danger")


@app.errorhandler(401)
def foo_page(e):
    return render_template("errorpage.html", title="Unauthorized, Bro!",
                           mainMess="You don't have the authorization to this page!",
                           sideMess="You might not be logged in or are snooping in a place you shouldn't!"), 401


@app.errorhandler(403)
def fot_age(e):
    return render_template("errorpage.html", title="Forbidden, Bro!",
                           mainMess="You don't have permission to view this page!",
                           sideMess="Please don't snoop around!"), 403


@app.errorhandler(404)
def fof_page(e):
    return render_template("errorpage.html", title="Not Found, Bro!",
                           mainMess="This page doesn't exist!",
                           sideMess="You might of typed in the wrong url, or just stupid."), 404


@app.errorhandler(500)
def server_error_page(e):
    return render_template("errorpage.html", title="Whoops!",
                           mainMess="There was a server error!",
                           sideMess="This is a problem on our part. We will attend to this shortly..."), 404


def modCaseInsSearch(mod, modattr, term, fun=None):
    if not fun:
        return mod.query.filter(func.lower(modattr) == func.lower(term))
    return mod.query.filter(fun(mod, func.lower(modattr), func.lower(term)))



# Regular Routes

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search/")
def search():
    terms = request.args.get("terms", "")
    search_user = modCaseInsSearch(User, User.username, terms).first()
    games = modCaseInsSearch(Game, Game.name, terms).all()
    return render_template("searchresults.html",
                           terms=terms,
                           title="Search: " + terms,
                           user=search_user,
                           repositories=None,
                           games=games)


@app.route("/about/")
def about():
    return render_template("about.html", title="About")


@app.route("/contact/", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        flash(Markup("<strong>Thank you %s!</strong> Your message was sent!") % form.name.data, "success")
        return redirect(url_for("contact"))
    flash_errors(form)
    return render_template("contact.html", title="Contact", conForm=form)


@app.route("/signup/", methods=["GET", "POST"])
def signup():
    if g.user is not None and g.user.is_authenticated():
        flash("You are already logged in!", "info")
        return redirect(url_for("index"))
    form = SignupForm()
    if form.validate_on_submit():
        if not User.query.filter(func.lower(User.username) == func.lower(form.uName.data)).first():
            addedUser = User(form.uName.data, form.eMail.data, form.pWord.data)
            db.session.add(addedUser)
            db.session.commit()
            login_user(addedUser)
            flash(Markup("<strong>Thank you %s!</strong> Your were successfully signed up!")  % form.uName.data, "success")
            return redirect(url_for("index"))
        flash("That username is already taken!", "danger")
        return render_template("signup.html", title="Signup", sigForm=form)
    flash_errors(form)
    return render_template("signup.html", title="Signup", sigForm=form)


@app.route("/login/", methods=["GET", "POST"])
def login():
    if g.user is not None and g.user.is_authenticated():
        flash("You are already logged in!", "info")
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        attempUser = User.query.filter(func.lower(User.username) == func.lower(form.uName.data)).first()
        if attempUser and attempUser.check_password(form.pWord.data):
            session["remember_me"] = form.remMe.data
            login_user(attempUser, remember=form.remMe.data)
            flash("%s, you have been signed in." % attempUser.username, "info")
            return redirect(url_for("index"))
        flash("You have entered the wrong username and/or password.", "danger")
        return render_template("login.html", title="Login", logForm=form)
    flash_errors(form)
    return render_template("login.html", title="Login", logForm=form)


@app.route("/logout/")
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))

@app.route("/getit/")
def getit():
    return render_template("getit.html", title="Get it")


@app.route("/download/")
def download():
    return render_template("download.html", title="Download")


@app.route("/webclient/")
def webclient():
    return render_template("webclient.html")


@app.route("/g/")
def games():
    return render_template("games.html", title="Games", games=Game.query.all())

@app.route("/g/<int:gid>/")
def game_page(gid):
    gq = Game.query.get(gid)
    if gq:
        return render_template("game.html", title=gq.name, game=gq)
    return render_template("errorpage.html", title="Game not found.",
                           mainMess="A game with the id of %s was not found" % gid,
                           sideMess="Please make sure the link is valid.")

@app.route("/g/submit/", methods=["GET", "POST"])
def game_submit():
    form = GameSubmitForm()
    if form.validate_on_submit():
        if Game.query.filter(func.lower(Game.name) == func.lower(form.name.data)).first():
            flash("This game has already been submitted.", "danger")
            return render_template("submitgame.html", title="Game Submission", form=form)
        gameToAdd = Game(form.name.data)
        db.session.add(gameToAdd)
        db.session.commit()
        flash("The game was successfully submitted!","success")
        return redirect(url_for("game_submit"))
    return render_template("submitgame.html", title="Game Submission", form=form)


@app.route("/s/")
def splits():
    return render_template("splits.html", title="Splits", splits=Split.query.all())

@app.route("/s/<int:sid>/")
def split_page(sid):
    sq = Split.query.get(sid)
    if sq:
        return render_template("game.html", title=sq.name, split=sq)
    return render_template("errorpage.html", title="Split not found.",
                           mainMess="A split with the id of %s was not found" % sid,
                           sideMess="Please make sure the link is valid.")


# User Pages

@app.route("/u/")
def users():
    return render_template("users.html", title="All users",
                           users=User.query.all())

@app.route("/u/<int:uid>/")
def user_page(uid):
    uq = User.query.get(uid)
    if uq:
        if g.user is not None and g.user.is_authenticated() and uid == g.user.id:
            return render_template("user.html", title=uq.username, user=uq, userspage=True)
        return render_template("user.html", title=uq.username, user=uq)
    return render_template("errorpage.html", title="User not found.",
                           mainMess="A user with the id of %s was not found." % uid,
                           sideMess="Please make sure the link is valid.")



#Split Pages

@app.route("/split/create/")
def splitcreate():
    return render_template("createsplit.html", title="Create splits")


# APIs

@app.route("/api/")
def api_home():
    return "Much Wow, Many API"

@app.route("/api/user_by_id/<int:uid>/")
def get_user(uid):
    uq = User.query.get(uid)
    if uq:
        return jsonify(id=uq.id, username=uq.username)
    return "No User with that id was found."