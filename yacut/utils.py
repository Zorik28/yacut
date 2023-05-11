from secrets import token_urlsafe

from .constants import HYPHEN, UNDERSCORE
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
    return False
