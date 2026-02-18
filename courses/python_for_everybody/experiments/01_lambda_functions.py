import time

#Testig Lambda expressions for 1 line custom functions

""" Simple version - tested
greet = lambda name: "Welcome, " + name
print(greet("Manuel"))
"""

#lambda taking two arguments + testing "else:" in try/except block
"""
width = input("Enter width: ").strip()
height = input("Enter height "). strip()

try:
    width = round(float(width), 2)
    height = round(float(height), 2)

except ValueError as e:
    print(f"Wrong value entered: {e}")

else:
    measure = lambda width, height: width * height
    print(f"Total is {measure(width, height)}")

#print("\nAfter try/except block...")
"""

#Using map() and filter() functions with lambda expressions + testing "else:" and "finally:" in try/block

#get names from user
names_input = input("\nEnter a list of names separated by commas(,): ").strip()
names = names_input.split(",")
print(f"\nOriginal list: {names}")

#convert raw data to list
name_lst = [name.strip() for name in names]
print(f"Stripped list: {name_lst}")
try:
    cap_lst = [name.capitalize() for name in name_lst]
except TypeError as e:
    print(f"Program Error: {e}")
else:
    print(f"Capitalized list: {cap_lst}")

time.sleep(2)

otherf = input("\nContinue to checkout map function()? Y/N: ").upper().strip()

if otherf == "Y":
    print("\nUsing same list as before, retrieving...")
    time.sleep(1)
    print(f"Retrieved list: {names}\n\nProcessing now...\n")

    def cap(name):
        return name.capitalize()
    
    #capitalized = map(cap, name_lst) #we use map() instead of "for loop"
    #capitalized = list(capitalized) #convert from map() object to list
    
    capitalized = list(map(lambda name: name.title(), names))

    print(f"Names list processed using map() function:\n {capitalized}\n")

else:
    print("\nExiting program now...")
    quit()

# =============================================================================
# LAMBDA QUICK REFERENCE
# =============================================================================
#
# Signature:
#     lambda parameters: expression
#
# | Parameters     | Example                          | Result          |
# |----------------|----------------------------------|-----------------|
# | None           | lambda: 42                       | 42              |
# | One            | lambda x: x * 2                  | 10 (if x=5)     |
# | Two            | lambda a, b: a + b               | 7 (if a=3, b=4) |
# | Multiple       | lambda a, b, c: a + b + c        | 6 (1+2+3)       |
# | With default   | lambda x, y=10: x + y            | 15 (if x=5)     |
# | With *args     | lambda *args: sum(args)          | 10 (1,2,3,4)    |
#
# Ternary in lambda:
#     lambda x: "yes" if x > 0 else "no"
#
# Common pairings:
#     sorted(items, key=lambda x: ...)
#     map(lambda x: ..., items)
#     filter(lambda x: ..., items)
#     max(items, key=lambda x: ...)
#     min(items, key=lambda x: ...)
#
# When to use lambda:
#     ✅ Simple, one-time-use functions
#     ✅ As arguments to higher-order functions (sorted, map, filter)
#
# When NOT to use lambda:
#     ❌ Complex logic (use regular def)
#     ❌ Reusable functions (give it a name with def)
#     ❌ When it hurts readability
#
# =============================================================================