from datetime import datetime

from flask import url_for

from . import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, nullable=False)
    short = db.Column(db.String(16), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())

    def to_serializer(self) -> dict:
        return dict(
            url=self.original,
            short_link=url_for(
                'follow_short_url',
                short=self.short, _external=True
            )
        )
