from app import app
from flask.ext.wtf import Form, RecaptchaField
from wtforms import TextField, TextAreaField, BooleanField, PasswordField, validators


class LoginForm(Form):
    uName = TextField("Username", validators=[
        validators.Required(),
        validators.Length(min=4, max=32, message="Usernames are 4 to 32 characters in length."),
        validators.Regexp("^[A-Za-z0-9_]+$", message="Usernames can only contain numbers, letters, and underscores.")])
    pWord = PasswordField("Password", validators=[
        validators.Required(),
        validators.Length(min=4, max=40, message="Password are 4 40 characters in length."),
        validators.Regexp("^[A-Za-z0-9]+$", message="Passwords are only numbers and letters.")])
    remMe = BooleanField("Remember Me", default=False)


class SignupForm(Form):
    uName = TextField("Username", validators=[
        validators.Required(),
        validators.Length(min=4, max=32, message="Usernames are 4 to 32 characters in length."),
        validators.Regexp("^[A-Za-z0-9_]+$", message="Usernames can only contain numbers, letters, and underscores.")])
    eMail = TextField("E-Mail", validators=[
        validators.Required(),
        validators.Email(message="The E-Mail must be valid."),
        validators.Length(max=254, message="An Email address is a max of 254 characters.")])
    confMail = TextField("Confirm E-Mail", validators=[
        validators.Required(message="You must confirm your email."),
        validators.EqualTo("eMail", message="The Email addresses must match.")])
    pWord = PasswordField("Password", validators=[
        validators.Required(),
        validators.Length(min=4, max=40, message="Password are 4 40 characters in length."),
        validators.Regexp("^[A-Za-z0-9]+$", message="Passwords are only numbers and letters.")])
    confPass = PasswordField("Confirm Password", validators=[
        validators.Required(message="You must confirm your password."),
        validators.EqualTo("pWord", message="Passwords must match.")])
    agToS = BooleanField("I agree to the terms of services.", default=False, validators=[
        validators.Required(message="You must agree to the Terms of Service.")])


class ContactForm(Form):
    name = TextField("Name", validators=[
        validators.Required(),
        validators.Length(max=128, message="Name must be less than 128 characters."),
        validators.Regexp("^[A-Za-z ]+$", message="Name can only be letters and spaces.")])
    email = TextField("E-Mail", validators=[
        validators.Required(),
        validators.Email(message="The E-Mail must be valid."),
        validators.Length(max=254, message="An Email address is a max of 254 characters.")])
    title = TextField("Title", validators=[
        validators.Required(message="A title is required."),
        validators.Length(max=140, message="Title must be less than 140 characters.")])
    message = TextAreaField("Message", validators=[
        validators.Required(message="You must have a message.")])


class GameSubmitForm(Form):
    name = TextField("Game Title", validators=[
        validators.Required(),
        validators.Length(min=1, max=80, message="The game title must be between 1 and 80 characters.")
    ])


class SplitSubmitPage(Form):
    name = TextField("Name:", validators=[
        validators.Required(message="You must provide a name for your split.")
    ])
    game = TextField("Game:", validators=[
        validators.Required(message="You must provide a game name.")
    ])