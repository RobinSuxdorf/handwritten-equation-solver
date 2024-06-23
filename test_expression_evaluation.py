import pytest

from expression_evaluation import (
    _evaluate_operator,
    _evaluate_rpn_expression,
    _is_number,
    _shunting_yard,
    _tokenize
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
    assert _is_number(test_token) == expected

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
    assert _tokenize(test_expression) == expected

@pytest.mark.parametrize("test_expression, expected", [
    ("3+4", ["3", "4", "+"]),
    ("3 + 4 * (2 - 1)", ["3", "4", "2", "1", "-", "*", "+"]),
    ("6 / 3 + (2 - 1)", ["6", "3", "/", "2", "1", "-", "+"]),
    ("3 + 4 * 2 / (1 - 3)^2^3", ["3", "4", "2", "*", "1", "3", "-", "2", "3", "^", "^", "/", "+"])
])
def test_shunting_yard(test_expression: str, expected: list[str]) -> None:
    assert _shunting_yard(test_expression) == expected

@pytest.mark.parametrize("operator, x, y, expected_result", [
    ("+", 1, 2, 3),
    ("-", 2, 1, 1),
    ("*", 3, 4, 12),
    ("/", 3, 2, 1.5),
    ("^", 2, 3, 8),
])
def test_evaluate_operator(operator: str, x: float, y: float, expected_result: float) -> None:
    assert _evaluate_operator(operator, x, y) == expected_result

def test_evaluate_operator_unknown_operator() -> None:
    with pytest.raises(ValueError, match="Unknown operator"):
        _evaluate_operator("", 0, 0)

def test_evaluate_operator_division_by_zero() -> None:
    with pytest.raises(ValueError, match="Division by zero."):
        _evaluate_operator("/", 1, 0)

@pytest.mark.parametrize("tokens, expected_result", [
    (["3", "4", "+"], 7),
    (["3", "4", "2", "1", "-", "*", "+"], 7),
    (["6", "3", "/", "2", "1", "-", "+"], 3),
    (["3", "4", "2", "*", "1", "3", "-", "2", "3", "^", "^", "/", "+"], 3.03125)
])
def test_evaluate_rpn_expression(tokens: list[str], expected_result: float) -> None:
    assert _evaluate_rpn_expression(tokens) == expected_result