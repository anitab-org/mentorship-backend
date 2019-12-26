from werkzeug.routing import BaseConverter


class ListOfStringConverter(BaseConverter):
    def __init__(self, url_map, randomify=False):
        self.regex = r'\d+(?:,\d+)*,?'

    def to_python(self, value):
        return [str(x) for x in value.split(',')]

    def to_url(self, value):
        return ','.join(str(x) for x in value)
