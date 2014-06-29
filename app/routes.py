from app import app, lm, db
from flask import request, render_template, flash, redirect, url_for, jsonify, g, session, Markup, abort
from flask.ext.login import login_user, logout_user, current_user
from forms import LoginForm, SignupForm, ContactForm, GameSubmitForm, SplitSubmitPage
from models import User, Game, Split, Race
from sqlalchemy import func
from wrappers import apikey_req
import written, time_format, json

navigationBar = [{"title": "About",   "mName": "about"},
                 {"title": "Contact", "mName": "contact"},
                 {"title": "Users",   "mName": "users"},
                 {"title": "Splits",  "mName": "splits"},
                 {"title": "Games",   "mName": "games"},
                 {"title": "Races",   "mName": "races"}]


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
def fot_page(e):
    return render_template("errorpage.html", title="Forbidden, Bro!",
                           mainMess="You don't have permission to view this page!",
                           sideMess="Please don't snoop around!"), 403


@app.errorhandler(404)
def fof_page(e):
    return render_template("errorpage.html", title="Not Found, Bro!",
                           mainMess="This page doesn't exist!",
                           sideMess="You might have typed in the wrong url or you are just stupid."), 404


@app.errorhandler(500)
def server_error_page(e):
    return render_template("errorpage.html", title="Whoops!",
                           mainMess="There was a server error!",
                           sideMess="This is a problem on our part. We will attend to this shortly..."), 500


def mod_cs_search(mod, modattr, term, fun=None):
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
    search_user = mod_cs_search(User, User.username, terms).first()
    games = mod_cs_search(Game, Game.name, terms).all()
    splits = mod_cs_search(Split, Split.name, terms).all()
    return render_template("searchresults.html",
                           terms=terms,
                           title="Search: " + terms,
                           user=search_user,
                           splits=splits,
                           games=games)


@app.route("/about/")
def about():
    return render_template("about.html", title="About")


@app.route("/contact/", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        written.write_message(form.name.data, form.email.data, form.title.data, form.message.data)
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
        if not mod_cs_search(User, User.username, form.uName.data).first():
            addedUser = User(form.uName.data, form.eMail.data, form.pWord.data)
            db.session.add(addedUser)
            db.session.commit()
            login_user(addedUser)
            flash(Markup("<strong>Thank you %s!</strong> Your were successfully signed up!") % form.uName.data, "success")
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


# Webclient Pages

@app.route("/webclient/<int:rid>/")
def webclient(rid):
    if g.user is None or not g.user.is_authenticated():
        return render_template("errorpage.html", title="Please log in.",
                               mainMess="You need to be logged in to view this page.",
                               sideMess="Please log in.")
    rq = Race.query.get(rid)
    if not rq:
        return abort(404)
    if rq.finished:
        return render_template("errorpage.html", title="This game has already finished",
                               mainMess="This game has already ended.",
                               sideMess="You could start a new game if you wanted to.")
    return render_template("webclient.html", title=rq.split.name, race=rq)

# Game Pages

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
        flash("The game was successfully submitted!", "success")
        return redirect(url_for("game_submit"))
    flash_errors(form)
    return render_template("submitgame.html", title="Game Submission", form=form)


# User Pages

@app.route("/u/")
def users():
    return render_template("users.html", title="Users",
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


# Race Pages

@app.route("/r/")
def races():
    races = Race.query.all()[::-1]
    return render_template("races.html", title="Races",
                           races=races,
                           active_races=[race for race in races if not race.finished])


@app.route("/r/<int:rid>/")
def race_page(rid):
    rq = Race.query.get(rid)
    if rq:
        if rq.finished:
            data = rq.get_file_results()
            for d in data:
                times = d["times"]
                d["times"] = [time_format.num_to_string(t) for t in times]
            users = [User.query.get(int(p["uid"])) for p in data]
            return render_template("race.html", title=rq.split.name, race=rq, rdata=data, users=users, split=rq.split.get_file_array())
        return render_template("race.html", title=rq.split.name, race=rq)
    return render_template("errorpage.html", title="Race not found.",
                           mainMess="A race with the id of %s was not found" % rid,
                           sideMess="Please make sure the link is valid.")


@app.route("/r/create/", methods=["POST"])
def create_race():
    sq = Split.query.get(int(request.form["split"]))
    if sq:
        race = Race(sq)
        db.session.add(sq)
        db.session.commit()
        return redirect(url_for("webclient", rid=race.id))
    return abort(404)


#Split Pages

@app.route("/s/")
def splits():
    return render_template("splits.html", title="Splits", splits=Split.query.all())


@app.route("/s/<int:sid>/")
def split_page(sid):
    sq = Split.query.get(sid)
    if sq:
        fa = sq.get_file_array()
        return render_template("split.html", title=sq.name, split=sq, sdata=fa)
    return render_template("errorpage.html", title="Split not found.",
                           mainMess="A split with the id of %s was not found" % sid,
                           sideMess="Please make sure the link is valid.")


@app.route("/s/create/", methods=["GET", "POST"])
def split_create():
    if g.user is not None and g.user.is_authenticated():
        form = SplitSubmitPage()
        if form.validate_on_submit():
            tgame = mod_cs_search(Game, Game.name, form.game.data).first()
            if not tgame:
                flash(Markup("That game was not found! Click <a href='%s'>here</a> to submit it!") % url_for("game_submit"), "danger")
                return render_template("createsplit.html", title="Create splits", form=form)
            tsplit = Split(form.name.data, tgame, g.user)
            db.session.add(tsplit)
            db.session.commit()
            flash("%s created a split for %s called %s." % (g.user.username, form.game.data, form.name.data), "info")
            return redirect(url_for("split_page", sid=tsplit.id))
        flash_errors(form)
        return render_template("createsplit.html", title="Create splits", form=form)
    flash(Markup('You need to be logged in to create splits. Sign up <a href="%s">here</a>.' % url_for("signup")), "danger")
    return redirect(url_for("index"))


@app.route("/s/<int:sid>/edit/", methods=["GET", "POST"])
def split_edit(sid):
    sq = Split.query.get(sid)
    if sq:
        if request.method == "POST":
            dat = request.form
            olist = [(dat["name%s" % n], dat["time%s" % n]) for n in range(1, int(dat["n"])+1)]
            flist = [el for el in olist]
            didfail = False

            for i in range(len(flist)):
                if len(flist[i][1]) > 0:
                    try:
                        temp = time_format.string_to_num(flist[i][1])
                        flist[i] = flist[i][0], temp
                    except:
                        didfail = True
                        break

            if didfail:
                flash("You did not format your times correctly!", "danger")
                return render_template("editsplit.html", title=sq.name, split=sq, sdata=olist)

            tflist = [f[1] for f in flist if f[1]]
            if not all(tflist[i] <= tflist[i+1] for i in xrange(len(tflist)-1)):
                flash("Times need to be in ascending order!", "danger")
                return render_template("editsplit.html", title=sq.name, split=sq, sdata=olist)


            if not (sq.user.id == g.user.id):
                sq = Split(dat["sname"], sq.game, g.user)
                db.session.add(sq)
                db.session.commit()
            else:
                sq.name = dat["sname"]
                db.session.commit()
            sq.write_file("%s\n%s\n" % (len(flist), "\n".join(["%s\n%s" % (t[0], t[1]) for t in flist])))
            flash("Success", "success")
            return redirect(url_for('split_page', sid=sq.id))


        sdata = sq.get_file_array()
        return render_template("editsplit.html", title=sq.name, split=sq, sdata=sdata)

    return render_template("errorpage.html", Title="Split not found",
                           mainMess="Split not found",
                           sideMess="Split not found.")


# APIs


@app.route("/api/u/<int:uid>/", methods=["POST"])
@apikey_req
def get_user(uid):
    uq = User.query.get(uid)
    if uq:
        return jsonify(id=uq.id, name=uq.username, avatar_url=uq.get_gravatar_url())
    return "none", 404

@app.route("/api/s/<int:sid>/", methods=["POST"])
@apikey_req
def get_split(sid):
    sq = Split.query.get(sid)
    if sq:
        return jsonify(id=sq.id, name=sq.name, splits=sq.file_to_dict())
    return "none", 404



@app.route("/api/r/<int:rid>/", methods=["POST"])
@apikey_req
def get_race(rid):
    rq = Race.query.get(rid)
    if rq:
        ts = rq.split
        if rq.finished:
            return jsonify(id = rid, split=dict(id=ts.id, name=ts.name, splits=ts.file_to_dict()), results=rq.get_file_results())
        return jsonify(id=rid, split=dict(id=ts.id, name=ts.name, splits=ts.file_to_dict()))
    return "none", 404

@app.route("/api/r/<int:rid>/results/", methods=["POST"])
@apikey_req
def post_race_results(rid):
    rq = Race.query.get(rid)
    if rq:
        if request.form.get("finished") == "yes":
            rq.finished = True
            db.session.commit()
            return "Successfully finished race", 200
        res = json.loads(request.form["res"])
        rq.add_res(res)
        return "Successfully posted results", 200
    return "none", 404

