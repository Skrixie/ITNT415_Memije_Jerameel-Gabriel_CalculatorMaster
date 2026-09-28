"""
division.py - level 3 (validation + smarter errors + float cleanup)
student: Memije | branch: division_Memije
"""

import math

from operations import register, CalculatorError


def check_number(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise CalculatorError(f"division needs numbers but got '{value}'")


def divide(a, b):
    """first number divided by the second, with the full set of safety checks"""
    check_number(a)
    check_number(b)

    # 0 / 0 is its own special case (undefined), so it gets its own message
    if a == 0 and b == 0:
        raise CalculatorError("0 divided by 0 is undefined, math has no answer for that")

    if b == 0:
        raise CalculatorError("you cant divide by zero, it breaks math")

    result = a / b

    # dividing by a super tiny number (like 1e-308) can blow up to inf
    if math.isinf(result):
        raise CalculatorError("that answer is too big for me to handle")

    # 1 / 3 goes on forever (0.3333333333333333), so we cut it at 10 places
    return round(result, 10)


register(name="Division", symbol="/", func=divide, order=4)
