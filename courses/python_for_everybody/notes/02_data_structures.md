**Course 2: Python Data Structures**
- Chapter 6: Strings
- Chapter 7: Files
- Chapter 8: Lists
- Chapter 9: Dictionaries
- Chapter 10: Tuples



# Py4E – Week 2 Notes

## Loops and conditionals

List comprehension: Build a list using a for loop (and conditional (if) optional)

Instead of:
    for x in range(1, 51):
    if x > 12:
       big_nums.append(x)

We can use:
    big_nums = [x for x in range(1, 51) if x > 12]