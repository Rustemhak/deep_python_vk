"""
Unit tests of the parse_json function.
"""
import pytest
from factory_json import JSONFactory
from json_parse import parse_json


def keyword_callback_mock(count: list):
    """Mock object for testing parse_json"""

    def mock_func(required_field: str, keyword: str):
        nonlocal count
        count.append(count.pop() + 1)

    return mock_func


# keyword_callback, json_str: str, required_fields=None, keywords=None

def test_parse_json_main():
    """Implementation of the case from the task"""
    count = [0]
    str_json = '{"key1": "Word1 word2", "key2": "word2 word3"}'
    parse_json(str_json, required_fields=["key1"],
               keywords=["word2"],
               keyword_callback=keyword_callback_mock(count))
    assert count[0] == 1


@pytest.mark.parametrize("len_keywords", list(range(1, 10)))
def test_parse_json_count_keyword_callback(len_keywords: int):
    """A test that checks the correctness of parse_json by keyword"""
    count = [0]
    str_json = JSONFactory.generate([1, len_keywords])
    parse_json(str_json, required_fields=JSONFactory.get_fields(),
               keywords=JSONFactory.get_keywords(),
               keyword_callback=keyword_callback_mock(count))
    assert count[0] == len_keywords


@pytest.mark.parametrize("len_fields", list(range(1, 10)))
def test_parse_json_count_field_callback(len_fields: int):
    """A test that checks the correctness of parse_json on field"""
    count = [0]
    str_json = JSONFactory.generate([len_fields, 1])
    parse_json(str_json, required_fields=JSONFactory.get_fields(),
               keywords=JSONFactory.get_keywords(),
               keyword_callback=keyword_callback_mock(count))
    assert count[0] == len_fields


def test_parse_json_fail():
    """Test when erroneous json string is served"""
    count = [0]
    error_str = "}{asdasd"
    parse_json(error_str, required_fields=JSONFactory.get_fields(),
               keywords=JSONFactory.get_keywords(),
               keyword_callback=keyword_callback_mock(count))
    assert count[0] == 0


@pytest.mark.parametrize("len_fields", list(range(1, 10)))
def test_parse_json_empty_keyword_callback(len_fields):
    count = [0]
    str_json = JSONFactory.generate([len_fields, 1])
    parse_json(str_json, required_fields=JSONFactory.get_fields(),
               keywords=JSONFactory.get_keywords(),
               keyword_callback=None)
    assert count[0] == 0
