import pytest

from expression_evaluation import (
    is_number,
    tokenize,
    shunting_yard
)

@pytest.mark.parametrize("test_token, expected", [
    ("3", True),
    ("3.0", True),
    ("+", False),
    ("3,0", False),
    ("1+2.0", False),
    ("", False)
])
def test_is_number(test_token: str, expected: bool) -> None:
    assert is_number(test_token) == expected

@pytest.mark.parametrize("test_expression, expected", [
    ("", []),
    ("3", ["3"]),
    ("3.0", ["3.0"]),
    ("+", ["+"]),
    ("1+2", ["1", "+", "2"]),
    ("1 + 2.0 * 3.7", ["1", "+", "2.0", "*", "3.7"]),
    ("3 + 7(5 - 4)", ["3", "+", "7", "(", "5", "-", "4", ")"]),
    ("2^3", ["2", "^", "3"])
])
def test_tokenize(test_expression: str, expected: list[str]) -> None:
    assert tokenize(test_expression) == expected

@pytest.mark.parametrize("test_expression, expected", [
    ("3+4", ["3", "4", "+"]),
    ("3 + 4 * (2 - 1)", ["3", "4", "2", "1", "-", "*", "+"]),
    ("6 / 3 + (2 - 1)", ["6", "3", "/", "2", "1", "-", "+"]),
    ("3 + 4 * 2 / (1 - 5)^2^3", ["3", "4", "2", "*", "1", "5", "-", "2", "3", "^", "^", "/", "+"])
])
def test_shunting_yard(test_expression: str, expected: list[str]) -> None:
    assert shunting_yard(test_expression) == expected