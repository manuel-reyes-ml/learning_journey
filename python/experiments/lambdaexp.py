#Testig Lambda expressions for 1 line custom functions

""" Simple version - tested
greet = lambda name: "Welcome, " + name
print(greet("Manuel"))
"""

width = input("Enter width: ").strip()
height = input("Enter height "). strip()

try:
    width = round(float(width), 2)
    height = round(float(height), 2)

except ValueError as e:
    print(f"Wrong value entered, {e}")

else:
    measure = lambda width, height: width * height
    print(f"Total is {measure(width, height)}")

print("\nAfter try/except block...")