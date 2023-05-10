import re
from http import HTTPStatus

from flask import jsonify, request

from . import app, db
from .constants import MAX_LENGTH, ONLY_NUMBERS_AND_ENGLISH
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import get_unique_short_id, is_unique


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id: str):
    """Retrieves original url."""
    urlmap = URLMap.query.filter_by(short=short_id).first()
    if urlmap is None:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': urlmap.original}), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def create_custom_id():
    """Creates a new unique short url."""
    data = request.get_json()       # Getting data from a query as a dictionary
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if data.get('url') is None:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    short_id = data.get('custom_id')
    if short_id in [None, "", '']:
        short_id = get_unique_short_id()
    if (
        not re.search(ONLY_NUMBERS_AND_ENGLISH, short_id) or
        len(short_id) > MAX_LENGTH
    ):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    if not is_unique(short_id):
        raise InvalidAPIUsage(f'Имя "{short_id}" уже занято.')
    urlmap = URLMap(original=data.get('url'), short=short_id)
    db.session.add(urlmap)
    db.session.commit()
    return jsonify(urlmap.to_serializer()), HTTPStatus.CREATED