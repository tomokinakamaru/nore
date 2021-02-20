# Nore

## Overview

Nore is a library that caches function calls to speed up trials-and-errors in data-mining and machine-learning projects. The following lines illustrates the features of Nore:

```python
from nore import nore

@nore
def f(x, y):
    print(f'Running f({x}, {y})')
    return g(x, y) * 2

@nore
def g(x, y):
    return x + y

z = f(1, 2) # Prints "Running f(1, 2)"
            # The result (= 6) is saved to a file under `.cache`
print(f'f(1, 2) = {z}')

z = f(1, 2) # Returns the value restored from the cache file
            # Does not print "Running f(1, 2)"
print(f'f(1, 2) = {z}')

z = f(1, 3) # Prints "Running f(1, 3)" since the arguments are different
            # The result (= 8) is saved to another file under `.cache`
print(f'f(1, 3) = {z}')
```

Since Nore caches function calls into files, the script prints only lines like "f(...) = ..." after the second execution. No lines like "Running f(...)" are printed after the second execution.

### Code-change detection

Cache files created by Nore are linked with function code, so a function is re-invoked if you update the implementation of the function. Suppose that you update `f` as follows:

```python
@nore
def f(x, y):
    print(f'Running f({x}, {y})')
    return g(x, y) * 3  # Used to be "return g(x, y) * 2"
```

Nore detects the change of `f`, re-invokes `f`, and stores the results into another cache file.

### Dependency analysis

Nore remembers dependencies among function calls to smartly re-invoke functions. Suppose that you update `g` as follows:

```python
@nore
def g(x, y):
    return x - y  # Used to be "return x + y"
```

Nore detects the change of `g`. Since `f` uses `g`, Nore finds that `f` needs to be re-invoked due to the change of `g`.

## Installation

```
pip install git+https://github.com/tomokinakamaru/nore
```

## Contributing

Bug reports, feature requests, and pull requests are welcome on GitHub at https://github.com/tomokinakamaru/nore.
