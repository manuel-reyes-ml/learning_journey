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
        print(f"{self.name} makes a sound")

# Dog inherits from Animal
# Dog gets everything from Animal has (like self.name)       
class Dog(Animal): 
    def speak(self): # OVERRIDE the parent method
        print(f"{self.name} says: Woof!")
        
class Cat(Animal): # Cat inherits from Animal
    def speak(self): # OVERRIDE the parent method
        print(f"{self.name} says: Meow!")
        
# Create objects
generic = Animal("Generic")
buddy = Dog("Buddy")
whiskers = Cat("Whiskers")

generic.speak()
buddy.speak()
whiskers.speak()



