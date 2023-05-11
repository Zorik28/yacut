from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp, URL

from .constants import SHORT_ID_MAX_LENGTH, ONLY_NUMBERS_AND_ENGLISH


class URLMapForm(FlaskForm):
    original_link = URLField(
        'Long link',
        validators=[
            DataRequired('Required field!'),
            URL(message="Damn, pal! This is not a link.")
        ]
    )
    custom_id = StringField(
        'Your short link',
        validators=[
            Length(1, SHORT_ID_MAX_LENGTH),
            Regexp(
                regex=ONLY_NUMBERS_AND_ENGLISH,
                message='You can only use numbers and English letters.'
            ),
            Optional()
        ]
    )
    submit = SubmitField('Create')
