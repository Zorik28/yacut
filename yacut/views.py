from secrets import token_urlsafe

from flask import flash, redirect, render_template

from . import app, db
from .constants import HYPHEN, UNDERSCORE
from .forms import URLMapForm
from .models import URLMap


def get_unique_short_id() -> str:
    """Create a new custom_id for URLMapForm."""
    custom_id = token_urlsafe(4)
    if UNDERSCORE in custom_id:
        custom_id = custom_id.replace(UNDERSCORE, 'U')
    if HYPHEN in custom_id:
        custom_id = custom_id.replace(HYPHEN, 'H')
    return custom_id if is_unique(custom_id) else get_unique_short_id()


def is_unique(custom_id: str) -> bool:
    """Сheck for uniqueness."""
    if not URLMap.query.filter_by(short=custom_id).first():
        return True


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        if not form.custom_id.data:
            # When user left the custom_id field empty
            form.custom_id.data = get_unique_short_id()
        if not is_unique(form.custom_id.data):
            flash(f'Имя {form.custom_id.data} уже занято!')
            return render_template('index.html', form=form)
        url = URLMap(
            original=form.original_link.data, short=form.custom_id.data
        )
        db.session.add(url)
        db.session.commit()
        return render_template('index.html', form=form, url=url)
    return render_template('index.html', form=form)


@app.route('/<string:short>')
def follow_short_url(short: str):
    """Redirects to a new link."""
    original_link = URLMap.query.filter_by(short=short).first_or_404().original
    return redirect(original_link)
