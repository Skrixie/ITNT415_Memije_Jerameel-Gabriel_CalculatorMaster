"""
subtraction.py - level 3 (validation + float cleanup + overflow guard)
student: Memije | branch: subtraction_Memije
"""

import math

from operations import register, CalculatorError


def check_number(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise CalculatorError(f"subtraction needs numbers but got '{value}'")


def subtract(a, b):
    """first number minus the second, with validation and a cleaned up answer"""
    check_number(a)
    check_number(b)
    result = a - b

    # subtracting a negative is the same as adding, so huge numbers can still
    # blow up (1e308 - -1e308). catch it before it prints "inf"
    if math.isinf(result):
        raise CalculatorError("that answer is too big for me to handle")

    # 0.3 - 0.1 gives 0.19999999999999998 which looks broken
    # rounding to 10 places fixes that so we get 0.2
    return round(result, 10)


register(name="Subtraction", symbol="-", func=subtract, order=2)
