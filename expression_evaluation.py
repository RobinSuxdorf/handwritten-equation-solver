class Operator:
    def __init__(self, precedence: int, associativity: str) -> None:
        self.precedence = precedence
        self.associativity = associativity

operators = {
    "^": Operator(3, "right"),
    "*": Operator(2, "left"),
    "/": Operator(2, "left"),
    "+": Operator(1, "left"),
    "-": Operator(1, "left")
}

def _is_number(token: str) -> bool:
    """
    Checks whether a token is a number or not.

    Args:
        token (str): The token to be checked.

    Returns:
        bool: True if the token is a number, otherwise False.
    """
    try:
        float(token)
        return True
    except ValueError:
        return False


def _tokenize(expression: str) -> list[str]:
    """
    Returns a tokenization of the input expression, e.g. each number and operator will be an entry on the result list.

    Args:
        expression (str): The expression to be tokenized.

    Returns:
        list[str]: A list containing the tokens from the expression.
    """
    tokens: list[str] = []

    expression = expression.replace(" ", "")

    current_number = ""

    for char in expression:
        if char.isdigit() or char == ".":
            current_number += char
        else:
            if current_number:
                tokens.append(current_number)
                current_number = ""
            tokens.append(char)
    
    if current_number:
        tokens.append(current_number)

    return tokens

def _should_pop_operator_stack(operator_stack: list[str], token: str) -> bool:
    """
    Determine if the operator stack should be popped based on precedence and associativity.

    Args:
        operator_stack (list[str]): Stack containg operators.
        token (str): Current token to be parsed.

    Returns:
        bool: True if operator stack should be stopped, otherwise False.
    """
    if not operator_stack or operator_stack[-1] == "(":
        return False

    top_operator = operators[operator_stack[-1]]
    current_operator = operators[token]

    return (
        current_operator.precedence < top_operator.precedence
        or (
            current_operator.precedence == top_operator.precedence
            and current_operator.associativity == "left"
        )
    )

def _shunting_yard(expression: str) -> list[str]:
    """
    Takes a mathematical expression in infix notation and transforms it to reverse Polish notation (RPN).

    Args:
        expression (str): The mathematil expression.

    Returns:
        list[str]: The reverse polish notation of the expression saved as list.
    """
    output: list[str] = []
    operator_stack: list[str] = []

    tokens = _tokenize(expression)

    for token in tokens:
        if _is_number(token):
            output.append(token)
        elif token in operators:
            while _should_pop_operator_stack(operator_stack, token):
                output.append(operator_stack.pop())
            operator_stack.append(token)
        elif token == ",":
            while operator_stack[-1] != "(":
                output.append(operator_stack.pop())
        elif token == "(":
            operator_stack.append(token)
        elif token == ")":
            while operator_stack[-1] != "(":
                output.append(operator_stack.pop())
            operator_stack.pop()

    while operator_stack:
        output.append(operator_stack.pop())

    return output

def _evaluate_operator(operator: str, x: float, y: float) -> float:
    """
    Evaluates a binary operation on two operands.

    Args:
        operator (str): The operator, one of "+", "-", "*", "/" or "^".
        operand1 (float): The first operand.
        operand2 (float): The second operand.

    Returns:
        float: The result of the operation.
    """
    if operator == "+":
        return x + y
    elif operator == "-":
        return x - y
    elif operator == "*":
        return x * y
    elif operator == "/":
        if y == 0:
            raise ValueError("Division by zero.")
        return x / y
    elif operator == "^":
        return pow(x, y)
    else:
        raise ValueError(f"Unknown operator: {operator}")

def _evaluate_rpn_expression(tokens: list[str]) -> float:
    """
    Evaluates an expression in reverse Polish notation (RPN).

    Args:
        tokens (list[str]): The expression in RPN as list of tokens.

    Returns:
        float: The result of the expression.
    """
    stack: list[float] = []

    for token in tokens:
        if _is_number(token):
            stack.append(float(token))
        else:
            try:
                operand2 = stack.pop()
                operand1 = stack.pop()
            except IndexError:
                raise ValueError("Invalid expression: insufficient values in the expression.")
            result = _evaluate_operator(token, operand1, operand2)
            stack.append(result)

    if len(stack) != 1:
        raise ValueError("Invalid expression: the stack should have exactly one element after evaluation.")


    return stack[0]

def evaluate_expression(expression: str) -> float:
    """
    Evaluates a mathematical expression in infix notation.

    Args:
        expression (str): The expression to be evaluated.

    Returns:
        float: The result of the evaluation.
    """
    tokens = _shunting_yard(expression)
    result = _evaluate_rpn_expression(tokens)
    return result