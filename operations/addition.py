"""
addition.py - level 3 (validation + float cleanup + overflow guard)
student: Memije | branch: addition_Memije
"""

import math

from operations import register, CalculatorError


def check_number(value):
    # same check as level 2. bool sneaks in as a number so we block it
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise CalculatorError(f"addition needs numbers but got '{value}'")


def add(a, b):
    """adds two numbers, blocks bad input, and cleans up the answer"""
    check_number(a)
    check_number(b)
    result = a + b

    # 1e308 + 1e308 turns into inf which is basically python giving up
    if math.isinf(result):
        raise CalculatorError("that answer is too big for me to handle")

    # floats are weird. 0.1 + 0.2 gives 0.30000000000000004 (yes really)
    # rounding to 10 places makes it 0.3 like a normal human expects
    # (trade off: super tiny answers under 1e-10 turn into 0, i know, i know)
    return round(result, 10)


register(name="Addition", symbol="+", func=add, order=1)
