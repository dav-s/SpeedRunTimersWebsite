from app import app
from flask import request, render_template, flash, abort

navigationBar = [{
		"title" : "Get it",
		"mName" : "getit"
	},{
		"title" : "About",
		"mName" : "about"
	},{
		"title" : "Contact",
		"mName" : "contact"
}]

@app.context_processor
def injectNav():
	return dict(nBar = navigationBar)

@app.errorhandler(404)
def fofPage(e):
	return render_template("404page.html", title="Not found, Bro!")

@app.errorhandler(401)
def fooPage(e):
	return render_template("401page.html", title="Unauthorized, Bro!")

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/search/<terms>")
def search(terms):
	return render_template("searchresults.html", terms=terms, title="Search: "+terms+" | Speedruntimers")

@app.route("/about/")
def about():
	return render_template("about.html", title="About")

@app.route("/contact/")
def contact():
	return render_template("contact.html", title="Contact")

@app.route("/signup/")
def signup():
	return render_template("signup.html", title="Signup")

@app.route("/login/", methods=["GET","POST"])
def login():
	if request.method == "POST":
		return "Logged in"
	return render_template("login.html", title="Login")

@app.route("/getit/")
def getit():
	return render_template("getit.html", title="Get it")

@app.route("/dowload/")
def download():
	return render_template("download.html", title="Download")

@app.route("/webclient/")
def webclient():
	return render_template("webclient.html")

