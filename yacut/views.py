from flask import flash, redirect, render_template

from . import app, db
from .forms import URLMapForm
from .models import URLMap
from .utils import get_unique_short_id, is_unique


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """View function for main page."""
    form = URLMapForm()
    if form.validate_on_submit():
        short = form.custom_id.data
        if not short:
            # When user left the custom_id field empty
            short = get_unique_short_id()
        if not is_unique(short):
            flash(f'Имя {short} уже занято!')
            return render_template('index.html', form=form)
        url = URLMap(original=form.original_link.data, short=short)
        db.session.add(url)
        db.session.commit()
        return render_template('index.html', form=form, url=url)
    return render_template('index.html', form=form)


@app.route('/<string:short>')
def follow_short_url(short: str):
    """Redirects to a new link."""
    original_link = URLMap.query.filter_by(short=short).first_or_404().original
    return redirect(original_link)
