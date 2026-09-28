"""
operations package - the plugin folder
student: Memije | course: BIT

ok so this folder is where every math operation lives. the main calculator
does NOT know what operations exist. it just loads whatever .py files are in
here. so when a branch gets merged and adds a new file, the calculator picks
it up automatically. no editing calculator.py, no merge conflicts, nice.

how an operation file works:
    1. import register (and CalculatorError if it needs to complain)
    2. write a function that takes two numbers and returns the answer
    3. call register(...) at the bottom so the calculator knows about it
"""

import importlib
import pkgutil


class CalculatorError(Exception):
    # our own error type. operations raise this when something is wrong
    # and the calculator shows the message instead of crashing
    pass


# every operation that gets registered lands in this list
OPERATIONS = []


def register(name, symbol, func, order=100):
    # name   = what shows up in the menu
    # symbol = the little sign used when printing the answer
    # func   = the function that does the math, func(a, b)
    # order  = smaller number shows up first in the menu
    OPERATIONS.append({"name": name, "symbol": symbol, "func": func, "order": order})


def load_operations():
    # look at every python file in this folder and import it
    # importing runs the register(...) line at the bottom of each file
    for module_info in pkgutil.iter_modules(__path__):
        try:
            importlib.import_module(f"{__name__}.{module_info.name}")
        except Exception as err:
            # one broken file shouldnt take the whole calculator down
            print(f"warning: skipped '{module_info.name}' because of: {err}")

    OPERATIONS.sort(key=lambda op: op["order"])
    return OPERATIONS
