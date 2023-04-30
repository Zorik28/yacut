from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp, URL


class URLMapForm(FlaskForm):
    original_link = URLField(
        'Long link',
        validators=[
            DataRequired('Required field!'),
            URL(message="Damn, pal! This is not a link")
        ]
    )
    custom_id = StringField(
        'Your short link',
        validators=[
            Length(1, 16),
            Regexp(
                regex=r'^[a-zA-Z0-9]+$',
                message='You can only use numbers and English letters!'
            ),
            Optional()
        ]
    )
    submit = SubmitField('Create')
