import json
from app.database.sqlalchemy_extension import db

from typing import Union

class JsonCustomType(db.TypeDecorator):
    """Enables JSON storage by encoding and decoding to Text field."""

    impl = db.Text

    @classmethod
    def process_bind_param(cls, value, dialect) -> Union[str, dict]:
        if value is None:
            return "{}"
        else:
            return json.dumps(value)

    @classmethod
    def process_result_value(cls, value, dialect) -> Union[str, dict, None]:
        if value is None:
            return {}
        else:
            try:
                return json.loads(value)
            except (ValueError, TypeError):
                return None
