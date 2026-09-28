"""
addition.py - level 1 (basic version)
student: Memije | branch: addition_Memije
"""

from operations import register


def add(a, b):
    # ok so this just adds the two numbers. literally the easiest one lol
    return a + b


# this line is how the calculator finds me. it says "hey put me in the menu"
# order=1 means i show up first in the list
register(name="Addition", symbol="+", func=add, order=1)
