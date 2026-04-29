# Speller Makefile commands — `make` Cookbook

```bash
# Morning — pull down changes, install fresh deps
make install-dev

# While coding — quick feedback loop
make format         # auto-fix style
make lint           # catch issues
make typecheck      # verify types
make test           # run tests

# All of the above at once
make all

# Before committing — verify packaging still works
make wheel-test

# After merging to main — tidy up
make clean
```

Trigger to remove all current artifacts in build/ and dist and then
build a new wheel and recreate build/ and dist/ files

```bash
# Build a wheel in dist/, and clean all current artifacts
make build
```

