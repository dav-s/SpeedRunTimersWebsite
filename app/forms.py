from app import app
from flask.ext.wtf import Form, RecaptchaField
from wtforms import TextField, TextAreaField, BooleanField, PasswordField, validators

class LoginForm(Form):
    uName = TextField("Username", validators = [
    	validators.Required(),
    	validators.Regexp("^[A-Za-z0-9_]{4,32}$")])
    pWord = PasswordField("Password", validators = [
    	validators.Required(),
    	validators.Regexp("^[A-Za-z0-9]{4,40}$")])
    remMe = BooleanField("Remember Me", default = False)

class SignupForm(Form):
	uName = TextField("Username", validators = [
		validators.Required(),
		validators.Regexp("^[A-Za-z0-9_]{4,32}$")])
	eMail = TextField("E-Mail", validators = [
		validators.Required(),
		validators.Email(),
		validators.Length(max=254)])
	confMail = TextField("Confirm E-Mail", validators = [
		validators.Required(),
		validators.Email(),
		validators.EqualTo("eMail")])
	pWord = PasswordField("Password", validators = [
		validators.Required(),
		validators.Regexp("^[A-Za-z0-9]{4,40}$")])
	confPass = PasswordField("Confirm Password", validators = [
		validators.Required(),
		validators.EqualTo("pWord")])
	agToS = BooleanField("I agree to the terms of services.", default=False, validators=[validators.Required()])
	#recap = RecaptchaField(validators=[validators.Required()])

class ContactForm(Form):
	name = TextField("Name", validators = [
		validators.Required(),
		validators.Regexp("^[A-Za-z ]{,128}$")])
	email = TextField("E-Mail", validators = [
		validators.Required(),
		validators.Email(),
		validators.Length(max=254)])
	title = TextField("Title", validators = [
		validators.Required(),
		validators.Length(max=140)])
	message = TextAreaField("Message", validators = [validators.Required()])