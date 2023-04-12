"""
Unit tests of the parse_json function.
"""
import pytest
from factory_json import JSONFactory
from json_parse import parse_json


def keyword_callback_mock():
    calls = []

    def mock_func(required_field: str, keyword: str):
        nonlocal calls
        calls.append((required_field, keyword))

    mock_func.calls = calls
    return mock_func


def test_parse_json_main():
    """Implementation of the case from the task"""
    mock = keyword_callback_mock()
    str_json = '{"key1": "Word1 word2", "key2": "word2 word3"}'
    parse_json(
        str_json, required_fields=["key1"], keywords=["word2"], keyword_callback=mock
    )
    assert len(mock.calls) == 1
    assert mock.calls[0] == ("key1", "word2")


def test_parse_json_full_match():
    mock = keyword_callback_mock()
    str_json = '{"key1": "cactusly", "key2": "cactus"}'
    parse_json(
        str_json,
        required_fields=["key1", "key2"],
        keywords=["cactus"],
        keyword_callback=mock,
    )
    assert len(mock.calls) == 1
    assert mock.calls[0] == ("key2", "cactus")


def test_parse_json_multiple_matches():
    mock = keyword_callback_mock()
    str_json = '{"key1": "Cactus Flower", "key2": "Flower Cactus"}'
    parse_json(
        str_json,
        required_fields=["key1", "key2"],
        keywords=["Cactus", "Flower"],
        keyword_callback=mock,
    )
    assert len(mock.calls) == 4
    assert set(mock.calls) == {
        ("key1", "Cactus"),
        ("key1", "Flower"),
        ("key2", "Cactus"),
        ("key2", "Flower"),
    }


def test_parse_json_no_matches():
    mock = keyword_callback_mock()
    str_json = '{"key1": "cactus cactusly", "key2": "Flower"}'
    parse_json(
        str_json,
        required_fields=["key1", "key2"],
        keywords=["NotExisting"],
        keyword_callback=mock,
    )
    assert len(mock.calls) == 0


def test_parse_json_with_none_arguments():
    mock = keyword_callback_mock()
    str_json = '{"key1": "Cactus cactusly", "key2": "Flower"}'
    parse_json(
        str_json, required_fields=None, keywords=["Cactus"], keyword_callback=mock
    )
    assert len(mock.calls) == 0

    parse_json(
        str_json, required_fields=["key1", "key2"], keywords=None, keyword_callback=mock
    )
    assert len(mock.calls) == 0

    parse_json(
        str_json,
        required_fields=["key1", "key2"],
        keywords=["Cactus"],
        keyword_callback=None,
    )
    assert len(mock.calls) == 0


@pytest.mark.parametrize("len_keywords", list(range(1, 10)))
def test_parse_json_count_keyword_callback(len_keywords: int):
    """A test that checks the correctness of parse_json by keyword"""
    mock = keyword_callback_mock()
    str_json = JSONFactory.generate([1, len_keywords])
    parse_json(
        str_json,
        required_fields=JSONFactory.get_fields(),
        keywords=JSONFactory.get_keywords(),
        keyword_callback=mock,
    )
    assert len(mock.calls) == len_keywords


@pytest.mark.parametrize("len_fields", list(range(1, 10)))
def test_parse_json_count_field_callback(len_fields: int):
    """A test that checks the correctness of parse_json on field"""
    mock = keyword_callback_mock()
    str_json = JSONFactory.generate([len_fields, 1])
    parse_json(
        str_json,
        required_fields=JSONFactory.get_fields(),
        keywords=JSONFactory.get_keywords(),
        keyword_callback=mock,
    )
    assert len(mock.calls) == len_fields


def test_parse_json_fail():
    """Test when erroneous json string is served"""
    mock = keyword_callback_mock()
    error_str = "}{asdasd"
    parse_json(
        error_str,
        required_fields=JSONFactory.get_fields(),
        keywords=JSONFactory.get_keywords(),
        keyword_callback=mock,
    )
    assert len(mock.calls) == 0
