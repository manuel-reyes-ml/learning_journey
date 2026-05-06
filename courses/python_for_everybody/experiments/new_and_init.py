from __future__ import annotations

class Dog:
    # __new__ runs first and produces the object. __init__ runs second and decorates it.
    def __new__(cls, name: str) -> Dog:
        print("1. __new__ called - making an empty object (Dog instance)")
        new_dog = super().__new__(cls)
        print(f"    returning a blank Dog instance: {new_dog}")  # ← no f-string with new_dog
        return new_dog
    
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
