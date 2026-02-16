# =============================================================================
# EMPTY CLASS
# =============================================================================

class Dog1:
    pass  # Empty class for now

# Create two "instances" (objects) from the class
buddy = Dog1()
max = Dog1()

print(type(buddy))
print(type(max))
print(buddy == max) # Are they the same object?

print("\n")

# =============================================================================
# CONSTRUCTOR(__init__), DATA, METHODS IN CLASS
# =============================================================================

# Class name must be unique inside the script
class Dog2:
    # The __init__ method runs automatically when you create an object (Constructor)
    def __init__(self, name, age, breed):
        self.name = name   # Store data ON this object
        self.age = age
        self.breed = breed
    
    # Classes can also have functions (called "methods") that work with the data    
    def bark(self):
        print(f"{self.name} says: Woof!") # Access THIS object's data
        
    def describe(self):
        print(f"{self.name} is a {self.age}-year-old {self.breed}")
    
# Create objects of Dog2 with their data
buddy = Dog2("Buddy", 3, "Labrador")
max = Dog2("Max", 5, "Beagle")

# When you write:
#buddy = Dog2("Buddy", 3, "Labrador")

# Python does this internally:
# 1. Creates empty Dog object
# 2. Calls __init__(self=buddy, name="Buddy", age=3, breed="Labrador")
# 3. self.name = "Buddy" → buddy.name = "Buddy"
# 4. Returns the object

print(f"{buddy.name} is {buddy.age} years old")
print(f"{max.name} is {max.age} years old")

print("\n")

# Call methods on each dog (with their data)
buddy.bark()
max.bark()
buddy.describe()
max.describe()

print("\n")

# =============================================================================
# INHERITANCE (BUILDING ON ANOTHER CLASS)
# =============================================================================

class Animal: # Parent (base) class
    def __init__(self, name):
        self.name = name
    
    def speak(self):
        return f"{self.name} makes a sound"
        
    def speak1(self):
        print(f"{self.name} makes a sound")

# Dog inherits from Animal
# Dog gets everything from Animal has (like self.name)
# super().method() -> Do what my parent does       
class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name) # Call Animal's __init__ first! to set up self.name
        self.breed = breed          # Then add Dog-specific data
    
    def speak(self):
        parent_message = super().speak() # Get Animal's version
        return f"{parent_message}... Woof! (I'm a {self.breed})"
    
    def speak1(self): # OVERRIDE the parent method
        print(f"{self.name} says: Woof!")
        
class Cat(Animal): # Cat inherits from Animal
    def speak1(self): # OVERRIDE the parent method
        print(f"{self.name} says: Meow!")
        
# Create objects
generic = Animal("Generic")
buddy = Dog("Buddy", "Labrador")
whiskers = Cat("Whiskers")

generic.speak1()
buddy.speak1()
whiskers.speak1()

print("\n")

print(buddy.speak())

print("\n")

class BasicFormatter:
    """Pretend this is logging.Formatter"""
    def format(self, record):
        return f"[LOG] {record}"

class ColoredFormatter(BasicFormatter):
    """Our custom formatter that adds color"""
    
    def format(self, record):
        # Step 1: Get the parent´s formatted message
        original = super().format(record)
        
        # Step 2: Wrap it with color
        return f"\033[92m{original}\033[0m"

# Test both
basic = BasicFormatter()
colored = ColoredFormatter()

print(basic.format("Hello World"))
print(colored.format("Hello Workd"))

# =============================================================================
# PYTHON CLASSES QUICK REFERENCE
# =============================================================================
#
# BASIC CLASS
# -----------
# class ClassName:
#     def __init__(self, param1, param2):    # Constructor
#         self.attribute1 = param1           # Instance attribute
#         self.attribute2 = param2
#
#     def method(self):                      # Instance method
#         return self.attribute1
#
# INHERITANCE
# -----------
# class Child(Parent):                       # Child inherits from Parent
#     def __init__(self, param1, new_param):
#         super().__init__(param1)           # Call parent's __init__
#         self.new_attr = new_param          # Add child-specific data
#
#     def method(self):                      # Override parent method
#         parent_result = super().method()   # Optionally use parent's version
#         return f"Modified: {parent_result}"
#
# KEY TERMS
# ---------
# | Term        | Meaning                                    |
# |-------------|-------------------------------------------|
# | class       | Blueprint for creating objects             |
# | object      | Instance created from a class              |
# | self        | Reference to the current instance          |
# | __init__    | Constructor, runs when object is created   |
# | method      | Function defined inside a class            |
# | attribute   | Variable stored on an object (self.x)      |
# | inheritance | Child class gets parent's attributes/methods|
# | super()     | Access parent class's methods              |
# | override    | Child replaces parent's method             |
#
# =============================================================================