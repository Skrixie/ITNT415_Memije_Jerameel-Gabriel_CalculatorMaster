"""
Calculator Master - main skeleton (hybrid edition)
student: Memije | course: BIT

ok so this is the base of the whole project. it has NO math in it on purpose.
every operation lives in its own file inside operations/ and gets added by its
own git branch. once a branch is merged the calculator finds the new file by
itself, so this file never has to change.

how to run:
    python3 calculator.py          -> menu in the terminal (default)
    python3 calculator.py --gui    -> little pop up window version
"""

import math
import sys

from operations import CalculatorError, load_operations


# ---------------------------------------------------------------------------
# shared stuff (the terminal AND the window both use these)
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
    # it gives back (worked_or_not, text_to_show)
    try:
        result = op["func"](a, b)
    except CalculatorError as err:
        # errors the operation files raise on purpose
        return False, str(err)
    except ArithmeticError as err:
        # safety net in case some math error sneaks through
        return False, f"math error: {err}"

    return True, f"{format_number(a)} {op['symbol']} {format_number(b)} = {format_number(result)}"


# ---------------------------------------------------------------------------
# terminal mode (the menu driven part from the assignment)
# ---------------------------------------------------------------------------

def show_menu(ops):
    print("\n===== CALCULATOR MASTER =====")
    if not ops:
        print("(no operations loaded yet - merge a branch first)")
    # the menu builds itself from whatever operations got loaded
    for number, op in enumerate(ops, start=1):
        print(f"{number}. {op['name']}")
    print(f"{len(ops) + 1}. Exit")


def ask_for_number(prompt):
    # keeps asking until the user types a real number, no crashing allowed
    while True:
        text = input(prompt).strip()
        try:
            value = float(text)
        except ValueError:
            print("invalid input, numbers only pls (like 5 or 2.5)")
            continue

        if is_good_number(value):
            return value
        print("thats not a real number, try again")


def run_cli(ops):
    print("welcome to Calculator Master!")
    exit_number = len(ops) + 1

    # keeps looping until the user picks exit
    while True:
        show_menu(ops)
        choice = input(f"pick an option (1-{exit_number}): ").strip()

        try:
            number = int(choice)
        except ValueError:
            number = 0  # not even a number, so it fails the checks below

        if number == exit_number:
            print("thanks for using Calculator Master, bye!")
            break
        elif 1 <= number <= len(ops):
            op = ops[number - 1]
            a = ask_for_number("enter first number: ")
            b = ask_for_number("enter second number: ")
            worked, message = do_calculation(op, a, b)
            print(("result: " if worked else "error: ") + message)
        else:
            print(f"thats not a valid option, pick 1-{exit_number}")


# ---------------------------------------------------------------------------
# window mode (bonus). tkinter comes with python so nothing to install
# ---------------------------------------------------------------------------

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

        worked, message = do_calculation(op, a, b)
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
# start of the program
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
