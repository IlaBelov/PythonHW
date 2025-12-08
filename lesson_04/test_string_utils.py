import pytest
from string_utils import StringUtils

string_utils = StringUtils()


@pytest.mark.positive
@pytest.mark.parametrize("input_string, expected", [
    ("hello", "Hello"),
    ("a", "A"),
    ("123hello", "123hello"),
])
def test_capitalize_positive(input_string, expected):
    assert string_utils.capitalize(input_string) == expected


@pytest.mark.negative
@pytest.mark.parametrize("input_string, expected", [
    ("", ""),
    ("  hello", "  hello"),
    ("1st", "1st"),
])
def test_capitalize_negative(input_string, expected):
    assert string_utils.capitalize(input_string) == expected


@pytest.mark.positive
@pytest.mark.parametrize("input_string, expected", [
    ("     hello", "hello"),
    (" ", ""),
    ("hello", "hello"),
])
def test_trim_positive(input_string, expected):
    assert string_utils.trim(input_string) == expected


@pytest.mark.negative
@pytest.mark.parametrize("input_string, expected", [
    ("", ""),
    ("  \t  hello", "\t  hello"),
])
def test_trim_negative(input_string, expected):
    assert string_utils.trim(input_string) == expected


@pytest.mark.positive
@pytest.mark.parametrize("string, symbol, expected", [
    ("hello", "e", True),
    ("hello world", "o", True),
    ("Hello", "H", True),
])
def test_contains_positive(string, symbol, expected):
    assert string_utils.contains(string, symbol) == expected


@pytest.mark.negative
@pytest.mark.parametrize("string, symbol, expected", [
    ("hello", "x", False),
    ("", "a", False),
    ("test", "T", False),
])
def test_contains_negative(string, symbol, expected):
    assert string_utils.contains(string, symbol) == expected


@pytest.mark.positive
@pytest.mark.parametrize("string, symbol, expected", [
    ("hello", "l", "heo"),
    ("test123", "2", "test13"),
    ("aaaaa", "a", ""),
])
def test_delete_symbol_positive(string, symbol, expected):
    assert string_utils.delete_symbol(string, symbol) == expected


@pytest.mark.negative
@pytest.mark.parametrize("string, symbol, expected", [
    ("hello", "x", "hello"),
    ("test", "", "test"),
    ("   ", " ", ""),
])
def test_delete_symbol_negative(string, symbol, expected):
    assert string_utils.delete_symbol(string, symbol) == expected
