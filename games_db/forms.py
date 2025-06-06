from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators


class GamesDBForm(FlaskForm):
    name = StringField('Game Name', [validators.DataRequired(), validators.Length(min=1, max=64)])
    save = SubmitField('Save')
