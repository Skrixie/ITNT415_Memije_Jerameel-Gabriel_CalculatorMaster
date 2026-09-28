# CalcuMator
Pinagpuyatan By: Memije, Jerameel Gabriel P.
Grade and Section: BIT42

## Branch Structure
- `main` - hybrid skeleton first, then the final integrated calculator after all four Pull Requests were merged
- `addition_Memije` - adds `operations/addition.py`
- `subtraction_Memije` - adds `operations/subtraction.py`
- `multiplication_Memije` - adds `operations/multiplication.py`
- `division_Memije` - adds `operations/division.py`

All four branches were created from the skeleton, developed separately, and
merged into `main` at the end through approved Pull Requests.

Each branch has 3 commits, one per level of improvement:

| Level | What changed |
|-------|--------------|
| 1 | basic working function (division also has its zero check) |
| 2 | input validation (rejects strings, True/False, None) |
| 3 | float cleanup (0.1 + 0.2 = 0.3), overflow guard, and smarter error messages |

## Program Features
- Menu-driven interface that builds itself from the operations that are loaded
- Optional GUI: `python3 calculator.py --gui`
- Addition, subtraction, multiplication, division
- Input validation (rejects letters, `nan`, `inf`, bad menu choices)
- Division-by-zero handling (and a separate message for 0 / 0)
- Overflow handling (huge answers show a message instead of `inf`)
- Keeps running until the user picks Exit
- Proper function definitions, one file per operation

## How to Run
```bash
python3 calculator.py          # terminal menu
python3 calculator.py --gui    # window version
```

## Design Notes
- I used a plugin style folder so each branch only adds a new file. That is why merging all four at the end has no conflicts.
- Tradeoff: rounding to 10 decimal places means answers smaller than 1e-10 show up as 0.
- Built and tested inside the Cisco DEVASC VM (Ubuntu, Python 3).
