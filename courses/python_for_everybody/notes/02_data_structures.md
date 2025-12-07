# 02: Data Structures

**Course:** Python Data Structures  
**Platform:** Coursera  
**Instructor:** Dr. Charles Severance  
**Started:** Nov 2025  
**Status:** Completed

---

## 📚 Overview

Deep dive into Python's built-in data structures for organizing and manipulating collections of data. Covers strings, file handling, lists, dictionaries, and tuples. Essential skills for processing real-world data and building practical applications.

---

## ✅ Progress

- [x] Module 6: Strings
- [x] Module 7: Files
- [x] Module 8: Lists
- [x] Module 9: Dictionaries
- [x] Module 10: Tuples

---

## 🎯 Key Concepts

### Module 6: Strings

**What it is:**  
Sequences of characters used to store and manipulate text data. Strings are immutable (can't be changed after creation).

**Why it matters:**  
Text processing is everywhere - parsing emails, cleaning data, extracting information, building user interfaces.

**Key points:**
- **Indexing:** Access characters by position: `name[0]` (first character)
- **Slicing:** Extract substrings: `name[0:3]` (characters 0, 1, 2)
- **Immutable:** Can't modify in place, must create new string
- **len():** Get string length
- **in operator:** Check if substring exists: `"a" in "banana"`
- **String methods:** `.lower()`, `.upper()`, `.strip()`, `.replace()`, `.find()`, `.startswith()`
- **Concatenation:** Join strings with `+`
- **String formatting:** f-strings, `.format()`, `%` operator

---

### Module 7: Files

**What it is:**  
Reading data from files and writing data to files on disk. Essential for persistent storage and processing large datasets.

**Why it matters:**  
Real data comes from files (CSV, text, logs). Programs need to save results. File I/O is fundamental to data analysis.

**Key points:**
- **Opening files:** `open(filename, mode)` - modes: 'r' (read), 'w' (write), 'a' (append)
- **Reading:** `.read()` (entire file), `.readline()` (one line), `.readlines()` (list of lines)
- **Iteration:** Loop through file line by line with `for line in file:`
- **Writing:** `.write(string)` to write data
- **Closing:** Always `.close()` file or use `with` statement
- **with statement:** Automatically closes file: `with open(file) as f:`
- **File paths:** Absolute vs relative paths
- **Error handling:** Use try/except for file operations

---

### Module 8: Lists

**What it is:**  
Ordered, mutable collections that can hold any type of data. The workhorse data structure in Python.

**Why it matters:**  
Lists are everywhere - storing multiple values, processing sequences, building dynamic collections. Most versatile data structure.

**Key points:**
- **Creating lists:** `numbers = [1, 2, 3]` or `list()`
- **Mutable:** Can modify after creation
- **Indexing:** Access elements: `numbers[0]`
- **Slicing:** Extract sublists: `numbers[1:3]`
- **Methods:** `.append()`, `.extend()`, `.insert()`, `.remove()`, `.pop()`, `.sort()`, `.reverse()`
- **in operator:** Check membership: `5 in numbers`
- **len():** Get list length
- **Concatenation:** Join with `+`
- **Iteration:** Loop with `for item in list:`
- **List comprehensions:** Create lists efficiently: `[x*2 for x in numbers]`
- **split() and join():** Convert between strings and lists

---

### Module 9: Dictionaries

**What it is:**  
Collections of key-value pairs (like a real dictionary: word → definition). Unordered but fast lookup by key.

**Why it matters:**  
Perfect for counting, grouping, mapping relationships. Essential for JSON/API data. Extremely common in real applications.

**Key points:**
- **Creating:** `counts = {'a': 3, 'b': 5}` or `dict()`
- **Access by key:** `counts['a']` returns value
- **Add/update:** `counts['c'] = 7`
- **get() method:** Safe access: `counts.get('x', 0)` (returns 0 if key missing)
- **in operator:** Check key exists: `'a' in counts`
- **Methods:** `.keys()`, `.values()`, `.items()` (key-value pairs)
- **Iteration:** Loop through keys, values, or both
- **Common pattern:** Counting occurrences with dictionaries
- **No duplicate keys:** Each key appears once

---

### Module 10: Tuples

**What it is:**  
Immutable sequences - like lists but can't be modified. Often used for fixed collections.

**Why it matters:**  
More efficient than lists for data that won't change. Used in dictionary items, function returns, data integrity.

**Key points:**
- **Creating:** `point = (3, 5)` - parentheses
- **Immutable:** Can't change after creation
- **Indexing/slicing:** Same as lists
- **Unpacking:** `x, y = point` assigns values to variables
- **Comparable:** Can compare and sort tuples
- **Dictionary items:** `.items()` returns list of tuples
- **Multiple return values:** Functions can return tuples
- **Faster than lists:** Less memory, faster operations
- **Single element:** Need comma: `(5,)` not `(5)`

---

## 💻 Code Examples

### Strings - Indexing and Slicing
```python
# String indexing
name = "Manuel"
print(name[0])      # Output: M
print(name[-1])     # Output: l (last character)
print(len(name))    # Output: 6

# String slicing
fruit = "banana"
print(fruit[0:3])   # Output: ban (characters 0, 1, 2)
print(fruit[2:])    # Output: nana (from index 2 to end)
print(fruit[:3])    # Output: ban (from start to index 3)
print(fruit[2:4])   # Output: na
```

---

### Strings - Methods
```python
# Common string methods
text = "  Hello World  "

print(text.lower())         # Output: "  hello world  "
print(text.upper())         # Output: "  HELLO WORLD  "
print(text.strip())         # Output: "Hello World" (removes whitespace)
print(text.replace("World", "Python"))  # Output: "  Hello Python  "
print(text.find("World"))   # Output: 8 (index where "World" starts)
print(text.startswith("  Hello"))  # Output: True

# String formatting
name = "Manuel"
age = 25
print(f"My name is {name} and I'm {age}")  # f-string (best!)
print("My name is {} and I'm {}".format(name, age))  # .format()
```

---

### Files - Reading
```python
# Read entire file
with open('mbox-short.txt') as file:
    content = file.read()
    print(content[:100])  # First 100 characters

# Read line by line (memory efficient!)
with open('mbox-short.txt') as file:
    for line in file:
        line = line.strip()  # Remove whitespace
        if line.startswith('From:'):
            print(line)

# Count lines
count = 0
with open('mbox-short.txt') as file:
    for line in file:
        count += 1
print(f"Total lines: {count}")
```

**Why `with`:** Automatically closes file even if error occurs. Best practice!

---

### Files - Writing
```python
# Write to file (overwrites existing!)
with open('output.txt', 'w') as file:
    file.write("Hello World\n")
    file.write("Line 2\n")

# Append to file
with open('output.txt', 'a') as file:
    file.write("Line 3\n")

# Write list to file
lines = ['First\n', 'Second\n', 'Third\n']
with open('output.txt', 'w') as file:
    file.writelines(lines)
```

---

### Lists - Basic Operations
```python
# Creating and modifying lists
numbers = [1, 2, 3, 4, 5]
numbers.append(6)           # Add to end: [1, 2, 3, 4, 5, 6]
numbers.insert(0, 0)        # Insert at index 0: [0, 1, 2, 3, 4, 5, 6]
numbers.extend([7, 8])      # Add multiple: [0, 1, 2, 3, 4, 5, 6, 7, 8]
numbers.remove(0)           # Remove first 0: [1, 2, 3, 4, 5, 6, 7, 8]
last = numbers.pop()        # Remove and return last: 8
numbers.sort()              # Sort in place
numbers.reverse()           # Reverse in place

# Slicing
nums = [0, 1, 2, 3, 4, 5]
print(nums[2:5])     # Output: [2, 3, 4]
print(nums[:3])      # Output: [0, 1, 2]
print(nums[3:])      # Output: [3, 4, 5]
```

---

### Lists - Common Patterns
```python
# Sum and average
numbers = [3, 41, 12, 9, 74, 15]
total = sum(numbers)
count = len(numbers)
average = total / count
print(f"Average: {average}")  # Output: Average: 25.666...

# Find max/min
print(max(numbers))  # Output: 74
print(min(numbers))  # Output: 3

# Filter list
nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
evens = [x for x in nums if x % 2 == 0]  # List comprehension!
print(evens)  # Output: [2, 4, 6, 8, 10]

# Transform list
squares = [x**2 for x in range(1, 6)]
print(squares)  # Output: [1, 4, 9, 16, 25]
```

---

### Lists - Split and Join
```python
# Split string into list
text = "From: john@example.com"
words = text.split()        # Split on whitespace
print(words)                # Output: ['From:', 'john@example.com']

email = "user@example.com"
parts = email.split('@')    # Split on specific character
print(parts)                # Output: ['user', 'example.com']

# Join list into string
words = ['Hello', 'World', 'Python']
sentence = ' '.join(words)   # Join with space
print(sentence)              # Output: "Hello World Python"

csv = ','.join(['a', 'b', 'c'])  # Join with comma
print(csv)                       # Output: "a,b,c"
```

---

### Dictionaries - Basics
```python
# Creating dictionaries
counts = {}  # Empty dictionary
counts['a'] = 1
counts['b'] = 2
print(counts)  # Output: {'a': 1, 'b': 2}

# Or initialize with values
person = {'name': 'Manuel', 'age': 25, 'city': 'Greenville'}
print(person['name'])  # Output: Manuel

# Safe access with get()
print(person.get('email', 'Not found'))  # Output: Not found
print(person.get('name', 'Not found'))   # Output: Manuel

# Check if key exists
if 'age' in person:
    print(f"Age: {person['age']}")
```

---

### Dictionaries - Counting Pattern
```python
# Count word occurrences (THE most common dictionary pattern!)
text = "the quick brown fox jumps over the lazy dog"
words = text.split()

counts = {}
for word in words:
    counts[word] = counts.get(word, 0) + 1

print(counts)
# Output: {'the': 2, 'quick': 1, 'brown': 1, 'fox': 1, ...}

# Find most common word
max_count = 0
max_word = None
for word, count in counts.items():
    if count > max_count:
        max_count = count
        max_word = word

print(f"Most common: {max_word} ({max_count} times)")
```

---

### Dictionaries - Iteration
```python
counts = {'a': 3, 'b': 5, 'c': 2}

# Iterate over keys
for key in counts:
    print(key, counts[key])

# Iterate over values
for value in counts.values():
    print(value)

# Iterate over key-value pairs (BEST!)
for key, value in counts.items():
    print(f"{key}: {value}")
```

---

### Tuples - Basics
```python
# Creating tuples
point = (3, 5)
person = ('Manuel', 25, 'Greenville')

# Access like lists
print(point[0])   # Output: 3
print(person[1])  # Output: 25

# Unpacking
x, y = point
print(f"x={x}, y={y}")  # Output: x=3, y=5

# Can't modify (immutable!)
# point[0] = 10  # ERROR!

# Comparison
t1 = (0, 1, 2)
t2 = (0, 3, 4)
print(t1 < t2)   # Output: True (compares element by element)
```

---

### Tuples - With Dictionaries
```python
# Dictionary items() returns list of tuples
counts = {'a': 3, 'b': 5, 'c': 2}

# Get list of (key, value) tuples
items = list(counts.items())
print(items)  # Output: [('a', 3), ('b', 5), ('c', 2)]

# Sort by value
sorted_items = sorted(counts.items(), key=lambda x: x[1], reverse=True)
print(sorted_items)  # Output: [('b', 5), ('a', 3), ('c', 2)]

# Top 3 items
for key, value in sorted_items[:3]:
    print(f"{key}: {value}")
```

---

## 📖 Important Terms

| Term | Definition | Example |
|------|------------|---------|
| **String** | Immutable sequence of characters | `"Hello"` |
| **Index** | Position of element (starts at 0) | `text[0]` |
| **Slice** | Extract portion of sequence | `text[2:5]` |
| **Immutable** | Cannot be changed after creation | Strings, tuples |
| **Mutable** | Can be modified after creation | Lists, dictionaries |
| **List** | Ordered, mutable collection | `[1, 2, 3]` |
| **Dictionary** | Key-value pairs | `{'name': 'Manuel'}` |
| **Tuple** | Immutable sequence | `(1, 2, 3)` |
| **Key** | Lookup value in dictionary | In `{'a': 5}`, 'a' is key |
| **Value** | Data associated with key | In `{'a': 5}`, 5 is value |
| **Method** | Function attached to object | `.append()`, `.split()` |
| **File handle** | Connection to file on disk | `f = open('file.txt')` |

---

## 🔧 Practice Exercises

**Exercise 1: Email Parser**
- **Task:** Read file, extract email addresses from "From:" lines
- **Solution:** Use `.split()` to get second word from lines starting with "From:"
- **Learning:** File reading, string methods, filtering

**Exercise 2: Word Frequency**
- **Task:** Count how many times each word appears in text
- **Solution:** Use dictionary with `.get(word, 0) + 1` pattern
- **Learning:** Dictionary counting pattern (super important!)

**Exercise 3: Grade Statistics**
- **Task:** Read list of grades, calculate average, find highest/lowest
- **Solution:** Use `sum()`, `len()`, `max()`, `min()` on list
- **Learning:** List operations, basic statistics

**Exercise 4: Data Cleaning**
- **Task:** Clean messy text (strip whitespace, lowercase, remove punctuation)
- **Solution:** Use `.strip()`, `.lower()`, `.replace()`
- **Learning:** String manipulation, data preprocessing

**Exercise 5: Top N Items**
- **Task:** Given dictionary of counts, find top 10 most common
- **Solution:** Convert to list of tuples with `.items()`, sort, slice [:10]
- **Learning:** Tuples, sorting, dictionary operations

---

## 💡 Key Takeaways

1. **Strings are immutable** - Can't change them, must create new ones
2. **Lists are mutable** - Can modify, append, remove elements freely
3. **Dictionaries are for counting** - The counting pattern (`get(key, 0) + 1`) is everywhere
4. **Use `with` for files** - Automatically closes file, prevents errors
5. **Tuples for fixed data** - Use when data shouldn't change (coordinates, database rows)
6. **String split() and join()** - Essential for text processing and CSV data
7. **List comprehensions** - Concise way to create lists: `[x*2 for x in nums]`
8. **Dictionary items()** - Returns tuples, perfect for sorting by value

---

## 🔗 Resources

- [Python String Methods](https://docs.python.org/3/library/stdtypes.html#string-methods)
- [Python Lists Tutorial](https://docs.python.org/3/tutorial/datastructures.html)
- [Python Dictionaries](https://realpython.com/python-dicts/)
- [Working with Files in Python](https://realpython.com/read-write-files-python/)
- [Python for Everybody - Chapter 6-10](https://www.py4e.com/html3/)

---

## 📝 My Notes

**What clicked:**  
- Dictionaries are PERFECT for counting - `counts.get(key, 0) + 1` is genius
- The `with` statement makes file handling so much safer
- List comprehensions are incredibly powerful once you understand them
- String `.split()` and `.join()` are inverse operations

**Challenges:**  
- Remembering when to use `.append()` vs `.extend()`
- Dictionary vs list - when to use which?
- File modes ('r', 'w', 'a') - which one to use when
- Tuple syntax with single element needs comma: `(5,)`

**Aha moments:**  
- Files are iterable! Can loop line-by-line without `.readlines()`
- Dictionary `.items()` returns tuples - perfect for sorting
- List slicing with negative indices: `nums[-3:]` = last 3 items
- F-strings are so much cleaner than old formatting

**To review:**  
- List comprehensions with conditions
- Nested dictionaries (dictionary of dictionaries)
- Sorting with custom keys
- File error handling (try/except)

**Real-world applications:**
- Used dictionary counting to analyze email frequency
- File reading essential for loading datasets
- String methods crucial for data cleaning
- Lists for storing and processing collections

---

## ➡️ Next Steps

**Next course:** 03_web_data.md (Regular Expressions, Network Programming, Web Services)  
**To practice:**  
- Build word frequency analyzer for any text file
- Create CSV parser using split() and dictionaries
- Practice file I/O with different data formats
- Write programs that combine all data structures

# Py4E – Week 2 Notes

## Loops and conditionals

List comprehension: Build a list using a for loop (and conditional (if) optional)

Instead of:
    for x in range(1, 51):
    if x > 12:
       big_nums.append(x)

We can use:
    big_nums = [x for x in range(1, 51) if x > 12]