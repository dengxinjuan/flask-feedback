from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField
from wtforms.validators import InputRequired

class RegisterForm(FlaskForm):
    """form for register user"""
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired()])
    first_name= StringField("Firstname", validators=[InputRequired()])
    last_name= StringField("Lastname", validators=[InputRequired()])


class LoginForm(FlaskForm):
    """Form for login a user."""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

