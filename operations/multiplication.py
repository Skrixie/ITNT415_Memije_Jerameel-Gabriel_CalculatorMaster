"""
multiplication.py - level 2 (now with input validation)
student: Memije | branch: multiplication_Memije
"""

from operations import register, CalculatorError


def check_number(value):
    # no strings allowed. in python "ab" * 3 actually WORKS and gives "ababab"
    # which is funny but not what a calculator should do, so we block it
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise CalculatorError(f"multiplication needs numbers but got '{value}'")


def multiply(a, b):
    """multiplies two numbers after making sure they are real numbers"""
    check_number(a)
    check_number(b)
    return a * b


register(name="Multiplication", symbol="*", func=multiply, order=3)
