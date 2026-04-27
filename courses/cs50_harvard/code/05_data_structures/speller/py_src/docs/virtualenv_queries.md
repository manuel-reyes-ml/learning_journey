# Speller Virtualenv Queries — `venv` Cookbook

We'll create a fresh, empty Python environment that has nothing installed, then install your
wheel into it. If the wheel is genuinely standalone, your speller will work in this empty
environment with no help from your source tree.

```bash
# Create a temporary venv somewhere outside your project
python3 -m venv /tmp/speller_test

# Activate it (commands differ by shell):
source /tmp/speller_test/bin/activate          # macOS / Linux (bash, zsh)
# /tmp/speller_test/Scripts/activate            # Windows
```


