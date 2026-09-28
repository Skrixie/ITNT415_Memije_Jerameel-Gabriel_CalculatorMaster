"""
addition.py - level 2 (now with input validation)
student: Memije | branch: addition_Memije
"""

from operations import register, CalculatorError


def check_number(value):
    # the main calculator already checks stuff, but my teacher says never trust
    # inputs, so addition double checks on its own
    # (True and False count as numbers in python which is so weird, so we block them)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise CalculatorError(f"addition needs numbers but got '{value}'")


def add(a, b):
    """adds two numbers after making sure they are actually numbers"""
    check_number(a)
    check_number(b)
    return a + b


register(name="Addition", symbol="+", func=add, order=1)
