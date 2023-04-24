from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, URL


class URLMapForm(FlaskForm):
    original = URLField(
        'Long link',
        validators=[
            DataRequired('Required field!'),
            URL(message="Damn, pal! This is not a link")
        ]
    )
    short = StringField(
        'Your short link',
        validators=[Length(1, 16), Optional()]
    )
    submit = SubmitField('Create')
