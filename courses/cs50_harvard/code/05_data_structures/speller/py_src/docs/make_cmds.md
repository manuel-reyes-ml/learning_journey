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
