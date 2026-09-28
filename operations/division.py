"""
division.py - level 1 (basic version + divide by zero check)
student: Memije | branch: division_Memije
"""

from operations import register, CalculatorError


def divide(a, b):
    # you cant divide by zero. python would crash if we just did a / b
    # so we check first and raise our own error (the calculator catches it)
    if b == 0:
        raise CalculatorError("cant divide by zero")
    return a / b


# order=4 so division is last in the menu
register(name="Division", symbol="/", func=divide, order=4)
