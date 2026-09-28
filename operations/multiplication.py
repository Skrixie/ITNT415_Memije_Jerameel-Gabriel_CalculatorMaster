"""
multiplication.py - level 3 (validation + float cleanup + overflow guard)
student: Memije | branch: multiplication_Memije
"""

import math

from operations import register, CalculatorError


def check_number(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise CalculatorError(f"multiplication needs numbers but got '{value}'")


def multiply(a, b):
    """multiplies two numbers with validation and a cleaned up answer"""
    check_number(a)
    check_number(b)
    result = a * b

    # multiplying gets big FAST. 1e200 * 1e200 becomes inf
    # so we stop it and show a real message instead
    if math.isinf(result):
        raise CalculatorError("that answer is too big for me to handle")

    # 0.1 * 3 gives 0.30000000000000004 (floats being floats again)
    # so we round it to 10 places
    return round(result, 10)


register(name="Multiplication", symbol="*", func=multiply, order=3)
