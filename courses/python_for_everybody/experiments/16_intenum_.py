# =============================================================================
# IntEnum QUICK REFERENCE
# =============================================================================

from enum import IntEnum, auto, unique

# BASIC DEFINITION
class Status(IntEnum):
    ACTIVE = 1
    INACTIVE = 2

# WITH auto()
class Priority(IntEnum):
    LOW = auto()     # 1
    MEDIUM = auto()  # 2
    HIGH = auto()    # 3

# PREVENT DUPLICATES
@unique
class UniqueStatus(IntEnum):
    OK = 1
    # ALSO_OK = 1  # Error!

# ACCESS
member = Status.ACTIVE
member.name          # "ACTIVE"
member.value         # 1
int(member)          # 1
str(member)          # "Status.ACTIVE"

# LOOKUP
Status["ACTIVE"]     # By name → Status.ACTIVE
Status(1)            # By value → Status.ACTIVE

# ITERATION
list(Status)         # [Status.ACTIVE, Status.INACTIVE]
[s.name for s in Status]   # ["ACTIVE", "INACTIVE"]
[s.value for s in Status]  # [1, 2]

# COMPARISON (works with int!)
Status.ACTIVE == 1   # True
Status.ACTIVE > 0    # True
Status.ACTIVE < Status.INACTIVE  # True

# OPERATIONS (it's an int!)
Status.ACTIVE + 10   # 11
Status.INACTIVE * 2  # 4

# WITH METHODS
class HttpStatus(IntEnum):
    OK = 200
    NOT_FOUND = 404
    
    def is_error(self) -> bool:
        return self >= 400

# KEY DIFFERENCES
# Enum:    member == int_value  → False
# IntEnum: member == int_value  → True

# =============================================================================