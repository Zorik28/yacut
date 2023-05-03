from secrets import token_urlsafe

from flask import render_template, redirect

from . import app, db
from .constants import HYPHEN, UNDERSCORE
from .forms import URLMapForm
from .models import URLMap


def get_unique_short_id() -> str:
    url = token_urlsafe(4)
    if UNDERSCORE in url:
        url = url.replace(UNDERSCORE, 'U')
    if HYPHEN in url:
        url = url.replace(HYPHEN, 'H')
    return url


@app.route('/', methods=['GET', 'POST'])
def index_view():
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
        return render_template('index.html', form=form, url=url)
    return render_template('index.html', form=form)


@app.route('/<string:short>')
def follow_short_url(short: str):
    original_link = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(original_link.original)
