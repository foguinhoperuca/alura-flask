from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators


class UserForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired(), validators.Length(min=8, max=16)])
    password = PasswordField('Password', [validators.DataRequired(), validators.Length(min=8, max=256)])
    login = SubmitField('Login')
