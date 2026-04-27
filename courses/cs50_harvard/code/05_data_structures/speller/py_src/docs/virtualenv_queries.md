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

# Verify no packages are installed in that venv (just pip)
pip list

# Install newly created packaged inside venv for testing
pip install dist/cs50_speller-0.2.0-py3-none-any.whl 
```

After tests are completed and need to re install a new version of the package
you may exit out the current environment and delete it to make sure we would start
clean. 

```bash
# Exit out current venv
deactivate

# Delete venv to remove all installed packages/dependencies
rm -rf /tmp/speller_test
```
