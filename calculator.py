"""
Calculator Master - main (PINAGPUYATAN EDITION)
student: Memije, Jerameel Gabriel P. | course: BIT

how to run:
    python3 calculator.py          -> menu in the terminal (default)
    python3 calculator.py --gui    -> little pop up window version

terminal shortcuts:
    H      show your history
    0      exit (q also works)
    b      go back to the menu while typing numbers
    ans    reuse your last answer as a number
"""

import math
import os
import sys

from operations import CalculatorError, load_operations

try:
    # this makes arrow keys and backspace work better when typing
    import readline
except ImportError:
    pass


# ---------------------------------------------------------------------------
# ui
# ---------------------------------------------------------------------------

# only use colors if we're in a real terminal (so screenshots and pipes dont get junk)
USE_COLOR = sys.stdout.isatty() and "NO_COLOR" not in os.environ

# only use the fancy box characters if the terminal can actually show them
FANCY = (sys.stdout.encoding or "").lower().replace("-", "").startswith("utf")

if FANCY:
    TL, TR, BL, BR, HL, VL, LT, RT = "╔", "╗", "╚", "╝", "═", "║", "╠", "╣"
    OK_MARK, BAD_MARK, DASH, ARROW = "✔", "✘", "──", "›"
else:
    TL = TR = BL = BR = LT = RT = "+"
    HL, VL = "-", "|"
    OK_MARK, BAD_MARK, DASH, ARROW = "OK", "X", "--", ">"

BOX_WIDTH = 40


def paint(text, code):
    # wraps text in a color code. code is stuff like "32;1" (bold green)
    if USE_COLOR:
        return f"\033[{code}m{text}\033[0m"
    return text


def print_box(title, rows):
    # rows is a list of (text, color_code). the box grows if a row is too long
    # (padding is worked out BEFORE coloring or the right side wouldnt line up)
    width = max(BOX_WIDTH, len(title) + 2, max((len(t) for t, _ in rows), default=0) + 2)
    edge = "36"  # cyan borders

    print(paint(TL + HL * width + TR, edge))
    print(paint(VL, edge) + paint(title.center(width), "1;36") + paint(VL, edge))
    print(paint(LT + HL * width + RT, edge))
    for text, code in rows:
        print(paint(VL, edge) + paint((" " + text).ljust(width), code) + paint(VL, edge))
    print(paint(BL + HL * width + BR, edge))


def ask(prompt):
    # the weird \001 and \002 tell readline "these characters are invisible"
    # so the cursor doesnt get confused by the color codes
    if USE_COLOR:
        prompt = "\001\033[36;1m\002" + prompt + "\001\033[0m\002"
    return input(prompt)


# ---------------------------------------------------------------------------
# shared
# ---------------------------------------------------------------------------

def format_number(value):
    # python prints 5.0 instead of 5 which looks kinda ugly
    # so if its a whole number we show it without the .0
    if not math.isfinite(value):
        return str(value)
    if value == int(value) and abs(value) < 1e15:
        return str(int(value))
    return str(value)


def is_good_number(value):
    # float("nan") and float("inf") technically work in python but theyre
    # not real numbers for a calculator, so we block them
    return math.isfinite(value)


def do_calculation(op, a, b):
    # this is the brain. the terminal and the window both call this, so the
    # error handling only has to be written one time (way less work)
    # it gives back (worked_or_not, text_to_show, the_actual_answer)
    try:
        result = op["func"](a, b)
    except CalculatorError as err:
        # errors the operation files raise on purpose
        return False, str(err), None
    except ArithmeticError as err:
        # safety net in case some math error sneaks through
        return False, f"math error: {err}", None

    message = f"{format_number(a)} {op['symbol']} {format_number(b)} = {format_number(result)}"
    return True, message, result


# ---------------------------------------------------------------------------
# terminal mode
# ---------------------------------------------------------------------------

class GoBack(Exception):
    # raised when the user types "b" so we can bail out to the menu
    pass


def show_menu(ops):
    rows = []
    if not ops:
        rows.append(("(no operations loaded yet)", "33"))

    # the menu builds itself from whatever operations got loaded
    for number, op in enumerate(ops, start=1):
        rows.append((f"[{number}] {op['name']:<16}( {op['symbol']} )", "0"))

    rows.append(("", "0"))  # empty row so its spaced out
    rows.append(("[H] History", "33"))
    rows.append(("[0] Exit", "31"))

    print()
    print_box("CALCULATOR MASTER", rows)


def show_history(history):
    if not history:
        rows = [("nothing yet, go do some math!", "33")]
    else:
        # only show the last 10 so it doesnt get huge
        recent = history[-10:]
        first_number = len(history) - len(recent) + 1
        rows = []
        for number, (worked, text) in enumerate(recent, start=first_number):
            mark = OK_MARK if worked else BAD_MARK
            rows.append((f"{number}. {mark} {text}", "32" if worked else "31"))

    print()
    print_box("HISTORY", rows)


def ask_for_number(label, last_answer):
    # keeps asking until the user types a real number, no crashing allowed
    while True:
        text = ask(f"  {label} {ARROW} ").strip()
        lowered = text.lower()

        if lowered in ("b", "back"):
            raise GoBack

        if lowered == "ans":
            if last_answer is None:
                print(paint("  no previous answer yet, type a number instead", "33"))
                continue
            return last_answer

        try:
            value = float(text)
        except ValueError:
            print(paint("  invalid input, numbers only pls (like 5 or 2.5)", "31"))
            continue

        if is_good_number(value):
            return value
        print(paint("  thats not a real number, try again", "31"))


def run_cli(ops):
    history = []        # every calculation this session
    last_answer = None  # so "ans" works

    print()
    print(paint("  welcome to Calculator Master!", "1;32"))
    print(paint("  tip: run with --gui for the window version", "2"))

    try:
        # keeps looping until the user picks exit
        while True:
            show_menu(ops)
            choice = ask(f"  pick an option {ARROW} ").strip().lower()

            if choice in ("0", "q", "quit", "exit"):
                break

            if choice in ("h", "history"):
                show_history(history)
                continue

            try:
                number = int(choice)
            except ValueError:
                number = 0  # not even a number, so it fails the check below

            if not 1 <= number <= len(ops):
                print(paint("  thats not a valid option, check the menu and try again", "33"))
                continue

            op = ops[number - 1]
            print()
            print(paint(f"  {DASH} {op['name']} {DASH}", "1;35")
                  + paint("   (b = back, ans = last answer)", "2"))

            try:
                a = ask_for_number("first number ", last_answer)
                b = ask_for_number("second number", last_answer)
            except GoBack:
                print(paint("  ok, back to the menu", "2"))
                continue

            worked, message, result = do_calculation(op, a, b)

            if worked:
                last_answer = result
                history.append((True, message))
                print(paint(f"  {OK_MARK} {message}", "32;1"))
            else:
                history.append((False, f"{op['name']}: {message}"))
                print(paint(f"  {BAD_MARK} {message}", "31;1"))

    except (KeyboardInterrupt, EOFError):
        # ctrl+c or ctrl+d, just leave nicely instead of a scary traceback
        print()

    print(paint("\n  thanks for using Calculator Master, bye!\n", "1;32"))

def run_gui(ops):
    import tkinter as tk
    from tkinter import messagebox

    try:
        root = tk.Tk()
    except tk.TclError as err:
        print(f"couldnt open a window (is there a screen?): {err}")
        return

    root.title("Calculator Master")
    root.geometry("360x340")
    root.resizable(False, False)

    tk.Label(root, text="Calculator Master", font=("Arial", 14, "bold")).pack(pady=(12, 6))

    tk.Label(root, text="Number 1").pack()
    entry1 = tk.Entry(root, justify="center")
    entry1.pack()

    tk.Label(root, text="Number 2").pack(pady=(8, 0))
    entry2 = tk.Entry(root, justify="center")
    entry2.pack()

    result_label = tk.Label(root, text="Result: -", font=("Arial", 11, "bold"))
    result_label.pack(pady=12)

    def on_click(op):
        # same checks as the terminal, just with popups instead of prints
        try:
            a = float(entry1.get())
            b = float(entry2.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "numbers only pls")
            return

        if not (is_good_number(a) and is_good_number(b)):
            messagebox.showerror("Invalid Input", "thats not a real number")
            return

        worked, message, _ = do_calculation(op, a, b)
        if worked:
            result_label.config(text=message)
        else:
            messagebox.showerror("Calculator Error", message)

    button_frame = tk.Frame(root)
    button_frame.pack()

    if not ops:
        tk.Label(button_frame, text="(no operations loaded yet)").pack()

    # one button per loaded operation, 2 buttons per row
    for index, op in enumerate(ops):
        row, column = divmod(index, 2)
        tk.Button(
            button_frame,
            text=f"{op['symbol']}  {op['name']}",
            width=16,
            command=lambda chosen=op: on_click(chosen),
        ).grid(row=row, column=column, padx=4, pady=4)

    tk.Button(root, text="Exit", command=root.destroy).pack(pady=12)
    root.mainloop()


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main():
    ops = load_operations()

    if "--gui" in sys.argv:
        try:
            run_gui(ops)
        except ImportError:
            print("tkinter isnt installed. try: sudo apt install python3-tk")
    else:
        run_cli(ops)


if __name__ == "__main__":
    main()
