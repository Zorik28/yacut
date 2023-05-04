from secrets import token_urlsafe

from flask import flash, redirect, render_template

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
    return url if is_unique(url) else get_unique_short_id()


def is_unique(short_link: str) -> bool:
    if not URLMap.query.filter_by(short=short_link).first():
        return True


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        short_link = form.custom_id.data
        if not short_link:
            short_link = get_unique_short_id()
        if not is_unique(short_link):
            flash('This short link already exists, try creating another one.')
            return render_template('index.html', form=form)
        url = URLMap(original=form.original_link.data, short=short_link)
        db.session.add(url)
        db.session.commit()
        return render_template('index.html', form=form, url=url)
    return render_template('index.html', form=form)


@app.route('/<string:short>')
def follow_short_url(short: str):
    original_link = URLMap.query.filter_by(short=short).first_or_404().original
    return redirect(original_link)
