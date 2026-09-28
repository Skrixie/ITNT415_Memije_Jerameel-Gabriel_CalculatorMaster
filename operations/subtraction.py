"""
subtraction.py - level 1 (basic version)
student: Memije | branch: subtraction_Memije
"""

from operations import register


def subtract(a, b):
    # first number minus the second number
    # order matters here (5 - 3 is NOT the same as 3 - 5, unlike addition)
    return a - b


# tells the calculator to put me in the menu, order=2 so im second
register(name="Subtraction", symbol="-", func=subtract, order=2)
