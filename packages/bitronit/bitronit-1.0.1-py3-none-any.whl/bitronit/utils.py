import re
from dateutil import parser

def parse_date(date_str: str):
    if date_str:
        return parser.parse(date_str)


def json_to_object(json_data, obj):
    for k, v in json_data.items():
        k = re.sub('([A-Z]+)', r'_\1', k).lower()
        if type(v) == str:
            try: v = parse_date(v)
            except: pass
        setattr(obj, k, v)
    return obj