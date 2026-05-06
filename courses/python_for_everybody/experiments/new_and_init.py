from __future__ import annotations

# Every class secretly inherits from object
# Python silently treats it as: class Dog(object):
# object is the universal root of every class hierarchy in Python.
# There is no class — anywhere, ever — that doesn't ultimately descend
# from object. This is true since Python 3.0 (in Python 2, you had to write
# class Dog(object): explicitly to get this; in Python 3, it's automatic).
class Dog:
    # __new__ runs first and produces and empty object (instance of this class).
    # cls is the class (in __new__, the instance doesn't exist yet)
    # Why must __new__ return something?
    # If it doesn't return an instance, there's nothing for __init__ to fill
    # — and your call to Dog("Rex") would just give back None.
    def __new__(cls, name: str) -> Dog:
        print("1. __new__ called - making an empty object (Dog instance)")
        # __mro__ is the Method Resolution Order — Python's ordered list of
        # where to look for methods. Even with no explicit parent, object
        # is right there.
        # When you write super().__new__(cls) inside Dog.__new__, Python walks
        # the MRO and finds the next class after Dog. That's object.
        #   super().__new__(cls)
        #   is equivalent to:
        #   object.__new__(cls)
        new_dog = super().__new__(cls)
        print(f"    returning a blank Dog instance: {new_dog}")  # ← no f-string with new_dog
        return new_dog
    
    # __init__ runs second and decorates it (with Data).
    # self is the instance (in __init__, it now exists)
    def __init__(self, name: str) -> None:
        print("2. __init__ called - setting up the object")
        self.name = name
        print(f"    done - name is now {self.name}")

    # make __str__ and __repr__ defensive. Use getattr with a fallback,
    # so it works whether the dog has a name yet or not.
    def __str__(self) -> str:
        name = getattr(self, "name", "<uninit>")
        return f"Dog(name={name})"
    
    def __repr__(self) -> str:
        name = getattr(self, "name", "<uninit>")
        return f"Dog(name={self.name!r})"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Dog):
            return NotImplemented
        return self.name == other.name
    
d = Dog("Rex")

print(d)
print(repr(d))
print(d is Dog("Rex"))
print(d == Dog("Rex"))
print(d != Dog("Rex"))
print(d != Dog("Buddy"))


# Visualizing the MRO walk
# Dog.__mro__ = (Dog, Animal, object)

#   super() inside Dog.__new__   →  finds Animal
#                                   →  calls Animal.__new__(cls)
#                                   →  inside Animal.__new__:
#                                        super() finds object
#                                        calls object.__new__(cls)
#                                   →  returns a blank Dog instance

# The key insight: super() doesn't mean "my parent." It means "the
# next class in the MRO." For single inheritance they're the same;
# for multiple inheritance they're not, and that's where super()'s
# real power shows up.