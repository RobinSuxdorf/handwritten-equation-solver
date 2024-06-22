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

def is_number(token: str) -> bool:
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


def tokenize(expression: str) -> list[str]:
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

def should_pop_operator_stack(operator_stack: list[str], token: str) -> bool:
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

def shunting_yard(expression: str) -> list[str]:
    """
    Takes a mathematical expression in infix notation and transforms it to reverse polish notation.

    Args:
        expression (str): The mathematil expression.

    Returns:
        list[str]: The reverse polish notation of the expression saved as list.
    """
    output: list[str] = []
    operator_stack: list[str] = []

    tokens = tokenize(expression)

    for token in tokens:
        if is_number(token):
            output.append(token)
        elif token in operators:
            while should_pop_operator_stack(operator_stack, token):
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