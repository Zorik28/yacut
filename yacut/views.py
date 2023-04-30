from datetime import datetime
from secrets import token_urlsafe

from flask import render_template

from . import app, db
from .forms import URLMapForm
from .models import URLMap


UNDERSCORE = '_'
HYPHEN = '-'


def get_unique_short_id() -> str:
    url = token_urlsafe(4)
    if UNDERSCORE in url:
        url = url.replace(UNDERSCORE, 'U')
    if HYPHEN in url:
        url = url.replace(HYPHEN, 'H')
    return url


@app.route('/', methods=['GET', 'POST'])
def index_view():
    year = datetime.now().year
    form = URLMapForm()
    if form.validate_on_submit():
        url = URLMap(
            original=form.original_link.data,
            # Assign the short link when the field 'custom_id' is empty
            short=(
                get_unique_short_id() if not form.custom_id.data
                else form.custom_id.data
            )
        )
        db.session.add(url)
        db.session.commit()
        return render_template('index.html', form=form, year=year, url=url)
    return render_template('index.html', form=form, year=year)
