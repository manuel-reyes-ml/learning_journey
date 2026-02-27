from enum import IntEnum
from dataclasses import dataclass
from typing import Final


# =============================================================================
# OPTION 1: Module-level with Final
# =============================================================================
EXIT_SUCCESS: Final[int] = 0
EXIT_FAILURE: Final[int] = 1

# Static: mypy warns on reassignment ✓
# Runtime: NO protection! ✗
EXIT_SUCCESS = 99  # Works at runtime! No error!


# =============================================================================
# OPTION 2: Simple Class
# =============================================================================
class ExitCodesClass:
    SUCCESS: Final[int] = 0
    FAILURE: Final[int] = 1

# Static: mypy warns on reassignment ✓
# Runtime: NO protection! ✗
ExitCodesClass.SUCCESS = 99  # Works at runtime! No error!


# =============================================================================
# OPTION 3: Frozen Dataclass (Instance)
# =============================================================================
@dataclass(frozen=True)
class ExitCodesDataclass:
    SUCCESS: int = 0
    FAILURE: int = 1

CODES = ExitCodesDataclass()

# Static: mypy warns on reassignment ✓
# Runtime: Instance protected, class NOT protected
CODES.SUCCESS = 99              # ❌ FrozenInstanceError ✓
ExitCodesDataclass.SUCCESS = 99  # ⚠️ Works! Class not protected!


# =============================================================================
# OPTION 4: IntEnum ⭐ BEST
# =============================================================================
class ExitCode(IntEnum):
    SUCCESS = 0
    FAILURE = 1

# Static: mypy warns on reassignment ✓
# Runtime: FULLY protected! ✓
ExitCode.SUCCESS = 99  # ❌ AttributeError: cannot reassign member
ExitCode.NEW = 5       # ❌ AttributeError: cannot extend enumeration
del ExitCode.SUCCESS   # ❌ AttributeError: cannot delete member