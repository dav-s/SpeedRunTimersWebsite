from app import app
from flask import request, render_template, flash, abort, redirect, url_for, jsonify
from forms import LoginForm, SignupForm, ContactForm

navigationBar = [{
                 "title": "Get it",
                 "mName": "getit"
                 }, {
                 "title": "About",
                 "mName": "about"
                 }, {
                 "title": "Contact",
                 "mName": "contact"
                 }]


@app.context_processor
def injectGlobs():
    return dict(nBar=navigationBar)


# Errors

def flashErrors(form):
    for name, errors in form.errors.iteritems():
        for error in errors:
            flash("%s" % error, "danger")


@app.errorhandler(401)
def fooPage(e):
    return render_template("errorpage.html", title="Unauthorized, Bro!",
                           mainMess="You don't have the authorization to this page!",
                           sideMess="You might not be logged in or are snooping in a place you shouldn't!"), 401


@app.errorhandler(403)
def fotPage(e):
    return render_template("errorpage.html", title="Forbidden, Bro!",
                           mainMess="You don't have permission to view this page!",
                           sideMess="Please don't snoop around!"), 403


@app.errorhandler(404)
def fofPage(e):
    return render_template("errorpage.html", title="Not Found, Bro!",
                           mainMess="This page doesn't exist!",
                           sideMess="You might of typed in the wrong url, or just stupid."), 404


# Regular Routes

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search/")
def search():
    terms = request.args.get("terms", "")
    return render_template("searchresults.html", terms=terms, title="Search: " + terms + " | Speedruntimers")


@app.route("/about/")
def about():
    return render_template("about.html", title="About")


@app.route("/contact/", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        flash("<strong>Thank you %s!</strong> Your message was sent!" % form.name.data, "success")
        return redirect(url_for("contact"))
    flashErrors(form)
    return render_template("contact.html", title="Contact", conForm=form)


@app.route("/signup/", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        flash("<strong>Thank you %s!</strong> Your were successfully signed up!" % form.uName.data, "success")
        return redirect(url_for("index"))
    flashErrors(form)
    return render_template("signup.html", title="Signup", sigForm=form)


@app.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash("%s, you have been signed in." % form.uName.data, "info")
        return redirect(url_for("index"))
    flashErrors(form)
    return render_template("login.html", title="Login", logForm=form)


@app.route("/getit/")
def getit():
    return render_template("getit.html", title="Get it")


@app.route("/dowload/")
def download():
    return render_template("download.html", title="Download")


@app.route("/webclient/")
def webclient():
    return render_template("webclient.html")


# APIs

@app.route("/api/")
def apiHome():
    return "Much Wow, Many API"
