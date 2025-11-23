# Py4E – Week 1 Notes

- `input()` always returns a string.
- Use `float()` or `int()` to convert to numbers.
- Use `str()` to convert to string.
- `print()` can take multiple arguments separated by commas.

- Here are the most common ones you’ll see as a beginner:

    Input / type / value related
    ValueError       # wrong value, e.g. float("abc")
    TypeError        # wrong type, e.g. len(5)
    NameError        # using a variable that doesn't exist

    Collections & indexing
    IndexError       # list index out of range
    KeyError         # dict key not found

    Math
    ZeroDivisionError  # division by zero
    OverflowError      # number too large (less common)

    Files & OS stuff
    FileNotFoundError  # opening a file that doesn't exist
    PermissionError    # no permission to read/write
    OSError            # generic OS-related error (parents of many file/network errors)

    Import / modules
    ImportError        # problem importing a module
    ModuleNotFoundError  # specific import not found

    Special ones (usually don’t catch these unless you know why)
    KeyboardInterrupt  # user pressed Ctrl + C
    SystemExit         # program is exiting (e.g. sys.exit())

## Catch a specific exception and keep the error object

Useful for debugging or printing the message:

try:
    x = float(user_input)
except ValueError as e:
    print("Conversion error:", e)

## Catch multiple specific exceptions

Use a tuple:

try:
    value = my_dict[key] / number
except (KeyError, ZeroDivisionError) as e:
    print("Problem accessing value or dividing:", e)