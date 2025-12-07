# 01: Programming Basics

**Course:** Programming for Everybody (Getting Started with Python)  
**Platform:** Coursera  
**Instructor:** Dr. Charles Severance  
**Started:** Nov 2025  
**Status:** Completed

---

## 📚 Overview

Introduction to programming fundamentals using Python. Covers the basics of why we program, variables and expressions, conditional execution, functions, and loops. This course provides the foundation for all future Python development.

---

## ✅ Progress

- [x] Module 1: Why We Program
- [x] Module 2: Variables, Expressions, and Statements
- [x] Module 3: Conditional Execution
- [x] Module 4: Functions
- [x] Module 5: Loops and Iteration

---

## 🎯 Key Concepts

### Module 1: Why We Program

**What it is:**  
Understanding what programming is, how computers work, and why Python is a good first language.

**Why it matters:**  
Computers are tools that follow instructions. Programming lets us tell computers what to do to solve problems and automate tasks.

**Key points:**
- Computers are fast but need precise instructions
- Programming languages translate human logic into machine instructions
- Python is beginner-friendly with readable syntax
- Programs are sequences of instructions (algorithms)

---

### Module 2: Variables, Expressions, and Statements

**What it is:**  
The building blocks of programs - storing data, performing calculations, and executing commands.

**Why it matters:**  
Variables let programs remember and manipulate data. Expressions perform calculations. Statements make things happen.

**Key points:**
- **Variables:** Named storage locations (`x = 5`)
- **Types:** int, float, str (Python determines automatically)
- **Operators:** `+`, `-`, `*`, `/`, `//`, `%`, `**`
- **Order of operations:** PEMDAS applies
- **Input/output:** `input()` gets user data, `print()` displays results
- **Type conversion:** `int()`, `float()`, `str()`

---

### Module 3: Conditional Execution

**What it is:**  
Making decisions in code - executing different actions based on conditions.

**Why it matters:**  
Programs need to respond differently to different situations (like "if user is logged in, show dashboard").

**Key points:**
- **if statement:** Execute code only if condition is True
- **else:** Alternative when condition is False
- **elif:** Multiple conditions (else-if)
- **Comparison operators:** `==`, `!=`, `>`, `<`, `>=`, `<=`
- **Logical operators:** `and`, `or`, `not`
- **Boolean values:** True and False
- **Indentation matters!** Python uses indentation to define code blocks

---

### Module 4: Functions

**What it is:**  
Reusable blocks of code that perform specific tasks. Like mini-programs within your program.

**Why it matters:**  
Functions let you organize code, avoid repetition, and make programs easier to read and maintain.

**Key points:**
- **Define function:** `def function_name():`
- **Parameters:** Input values passed to function
- **Return values:** Output from function using `return`
- **Built-in functions:** `print()`, `len()`, `max()`, `min()`, `type()`
- **Function calls:** Execute function by name: `function_name()`
- **Scope:** Variables inside functions are local (don't exist outside)

---

### Module 5: Loops and Iteration

**What it is:**  
Repeating actions - running the same code multiple times without copy-pasting.

**Why it matters:**  
Computers excel at repetition. Loops let you process lists, repeat calculations, and automate repetitive tasks.

**Key points:**
- **while loop:** Repeats while condition is True
- **for loop:** Iterates over a sequence (list, string, range)
- **break:** Exit loop immediately
- **continue:** Skip to next iteration
- **Infinite loops:** Dangerous! Always have exit condition
- **Loop patterns:** Counting, searching, accumulating
- **range():** Generate number sequences

---

## 💻 Code Examples

### Variables and Types
```python
# Variables and assignment
name = "Manuel"
age = 25
height = 5.9
is_student = True

# Type conversion
user_input = input("Enter a number: ")  # Returns string
number = int(user_input)  # Convert to integer
result = number * 2
print(f"Double is: {result}")
```

**Output:**
```
Enter a number: 5
Double is: 10
```

---

### Conditional Execution
```python
# Simple if-else
hours = float(input("Enter hours: "))
rate = float(input("Enter rate: "))

if hours > 40:
    # Overtime pay
    regular = 40 * rate
    overtime = (hours - 40) * rate * 1.5
    pay = regular + overtime
else:
    # Regular pay
    pay = hours * rate

print(f"Pay: ${pay}")
```

**Example run:**
```
Enter hours: 45
Enter rate: 10
Pay: $475.0
```

**Explanation:**  
Checks if hours exceed 40. If yes, calculates overtime (1.5x rate). Otherwise, simple multiplication.

---

### Multiple Conditions (elif)
```python
score = int(input("Enter score: "))

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print(f"Grade: {grade}")
```

---

### Functions
```python
# Define function with parameters
def calculate_pay(hours, rate):
    """Calculate pay with overtime."""
    if hours > 40:
        regular = 40 * rate
        overtime = (hours - 40) * rate * 1.5
        return regular + overtime
    else:
        return hours * rate

# Call function
pay = calculate_pay(45, 10)
print(f"Pay: ${pay}")  # Output: Pay: $475.0
```

**Why better:** Reusable! Can call `calculate_pay()` multiple times without rewriting logic.

---

### While Loops
```python
# Count to 5
n = 1
while n <= 5:
    print(n)
    n = n + 1  # Important! Update condition

# Output: 1 2 3 4 5 (each on new line)
```
```python
# User input loop
while True:
    line = input("> ")
    if line == "done":
        break
    print(line.upper())

print("Finished!")
```

---

### For Loops
```python
# Iterate over list
friends = ["Alice", "Bob", "Charlie"]
for friend in friends:
    print(f"Hello, {friend}!")

# Output:
# Hello, Alice!
# Hello, Bob!
# Hello, Charlie!
```
```python
# Using range()
for i in range(5):
    print(i)  # Output: 0 1 2 3 4

# Sum numbers 1-10
total = 0
for num in range(1, 11):
    total = total + num
print(total)  # Output: 55
```

---

### Loop Patterns
```python
# Finding largest value
largest = None
for value in [3, 41, 12, 9, 74, 15]:
    if largest is None or value > largest:
        largest = value
print(f"Largest: {largest}")  # Output: 74
```
```python
# Counting pattern
count = 0
for letter in "banana":
    if letter == "a":
        count = count + 1
print(f"'a' appears {count} times")  # Output: 3
```

---

## 📖 Important Terms

| Term | Definition | Example |
|------|------------|---------|
| **Variable** | Named storage for data | `x = 5` |
| **String** | Text data in quotes | `name = "Manuel"` |
| **Integer** | Whole number | `age = 25` |
| **Float** | Decimal number | `price = 19.99` |
| **Boolean** | True or False value | `is_valid = True` |
| **Function** | Reusable code block | `def greet(): print("Hi")` |
| **Parameter** | Input to function | `def add(x, y):` |
| **Return** | Output from function | `return x + y` |
| **Loop** | Repeat code | `for i in range(5):` |
| **Conditional** | Decision making | `if x > 0:` |
| **Iteration** | Going through items one by one | `for item in list:` |
| **Indentation** | Spaces defining code blocks | Required in Python! |

---

## 🔧 Practice Exercises

**Exercise 1: Pay Calculator**
- **Task:** Write program that asks for hours and rate, calculates pay with overtime (>40 hrs = 1.5x)
- **Solution:** Use if/else to check hours > 40, calculate accordingly
- **Learning:** Conditional logic, user input, calculations

**Exercise 2: Grade Calculator**
- **Task:** Convert numerical score to letter grade (A-F)
- **Solution:** Use elif chain for score ranges
- **Learning:** Multiple conditions, decision trees

**Exercise 3: Find Maximum**
- **Task:** Find largest number in list using loop
- **Solution:** Track largest value, update if current > largest
- **Learning:** Loop patterns, variable tracking

**Exercise 4: Count Vowels**
- **Task:** Count vowels in a string
- **Solution:** Loop through string, check if each character in "aeiou"
- **Learning:** String iteration, counting pattern

---

## 💡 Key Takeaways

1. **Variables store data** - Use descriptive names, understand types (int, float, str)
2. **Conditionals make decisions** - if/elif/else let programs respond to different situations
3. **Functions organize code** - Reusable, easier to read, avoid repetition
4. **Loops automate repetition** - while for unknown iterations, for for sequences
5. **Indentation is syntax** - Python uses spaces to define code structure (not optional!)
6. **Start simple, build up** - Write small working pieces, test, then combine
7. **Comments help future you** - Explain WHY not WHAT

---

## 🔗 Resources

- [Official Python Tutorial](https://docs.python.org/3/tutorial/)
- [Python for Everybody Textbook](https://www.py4e.com/book)
- [Automate the Boring Stuff](https://automatetheboringstuff.com/) - Similar beginner resource
- [Python Tutor](https://pythontutor.com/) - Visualize code execution
- [Real Python Basics](https://realpython.com/python-basics/)

---

## 📝 My Notes

**What clicked:**  
- Functions are like creating your own custom tools
- Loops save massive amounts of time vs manual repetition
- Indentation errors are frustrating but you get used to them

**Challenges:**  
- Remembering when to use `==` vs `=` (comparison vs assignment)
- Off-by-one errors in loops (forgetting range stops before end)
- Scope - variables inside functions don't exist outside

**Aha moments:**  
- `for` loops are better for "do this N times" or "for each item"
- `while` loops better for "keep going until condition changes"
- Functions can call other functions!

**To review:**  
- Loop patterns (counting, finding max/min, filtering)
- When to use return vs print in functions
- Nested conditionals (if inside if)

---

## ➡️ Next Steps

**Next course:** 02_data_structures.md (Strings, Lists, Dictionaries, Tuples)  
**To practice:**  
- Write more functions (get comfortable with parameters and return)
- Practice loop patterns (count, search, filter, accumulate)
- Build small programs combining all concepts (calculator, quiz game, etc.)



- Here are the most common ones you’ll see as a beginner:

    Input / type / value related
    ValueError       # wrong value, e.g. float("abc")
    TypeError        # wrong type, e.g. len(5)
    NameError        # using a variable that doesn't exist

    Syntax
    SyntaxError.     # wronf syntax (missing colon :)

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

## How does main() work in Python?

In Python we usually use this pattern:

def main():
    # main program logic
    ...

if __name__ == "__main__":
    main()

🔍 What is __name__?

Python sets a special variable called __name__ for every file.

If you run the file directly:

python overtime_pay.py


then inside that file:

__name__ == "__main__"


If you import the file from somewhere else:

import overtime_pay


then inside overtime_pay.py:

__name__ == "overtime_pay"


So:

if __name__ == "__main__":
    main()

means:

“Only run main() if this file is being executed directly, not when it’s imported.”