import json
from typing import List


def parse_json(json_str: str,
               required_fields: List[str] = None,
               keywords: List[str] = None,
               keyword_callback=None):
    """Parsing the json string json_str according
    to the list of fields required_fields,
     a list of keywords names
     and a handler function named keyword_callback"""
    if keyword_callback is None:
        return
    try:
        json_doc: dict = json.loads(json_str)
    except json.decoder.JSONDecodeError as json_error:
        print("Error parsing json string:", json_error)
        return
    for required_field in required_fields:
        if json_doc.get(required_field, ""):
            for keyword in keywords:
                if keyword in json_doc.get(required_field, ""):
                    keyword_callback(required_field, keyword)
