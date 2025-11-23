import sys
from pathlib import Path

print("=== Python Environment Check ===")
print("Python executable:", sys.executable)
print("Python version:", sys.version.split()[0])
print("Current working directory:", Path().resolve())
print("Virtual env active:", hasattr(sys, "real_prefix") or sys.prefix != sys.base_prefix)

print("\nChecking key packages...")


def check_package(name):
    try:
        mod = __import__(name)
        version = getattr(mod, "__version__", "unknown")
        print(f" - {name}: OK (version {version})")
    except ImportError:
        print(f" - {name}: NOT INSTALLED")


for pkg in ["numpy", "pandas", "matplotlib", "jupyter"]:
    check_package(pkg)
