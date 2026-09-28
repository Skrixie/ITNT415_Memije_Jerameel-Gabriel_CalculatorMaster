"""
multiplication.py - level 1 (basic version)
student: Memije | branch: multiplication_Memije
"""

from operations import register


def multiply(a, b):
    # times tables vibes. the star (*) is how python does multiplying
    return a * b


# order=3 so multiplication shows up third in the menu
register(name="Multiplication", symbol="*", func=multiply, order=3)
