"""
subtraction.py - level 2 (now with input validation)
student: Memije | branch: subtraction_Memije
"""

from operations import register, CalculatorError


def check_number(value):
    # making sure both inputs are real numbers before we do any math
    # bool is secretly a number in python (True = 1) so it gets blocked too
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise CalculatorError(f"subtraction needs numbers but got '{value}'")


def subtract(a, b):
    """first number minus the second, but only if both are real numbers"""
    check_number(a)
    check_number(b)
    return a - b


register(name="Subtraction", symbol="-", func=subtract, order=2)
