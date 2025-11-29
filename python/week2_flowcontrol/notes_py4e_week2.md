# Py4E – Week 2 Notes

## Loops and conditionals

List comprehension: Build a list using a for loop (and conditional (if) optional)

Instead of:
    for x in range(1, 51):
    if x > 12:
       big_nums.append(x)

We can use:
    big_nums = [x for x in range(1, 51) if x > 12]