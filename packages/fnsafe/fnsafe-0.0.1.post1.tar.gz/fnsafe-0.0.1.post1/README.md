fnsafe
======

The `fnsafe` library provides a decorator to
make your functions not raising errors. Instead
you are forced to handle the error.

The design is inspired by rust's
[Option](https://doc.rust-lang.org/std/option/enum.Option.html) and
[Result](https://doc.rust-lang.org/std/result/enum.Result.html)
enums.

While the class's name is `Result`, it provides
most of the functionality from rust's `Option` enum
instead of rust's `Result` enum.

```bash
pip install fnsafe
```

```python
import fnsafe

@fnsafe.makesafe
def divide(a, b, /):
    return a / b

result = divide(10, 0)
# Normally, this would raise an error since we're
# dividing through zero. The decorator turns the
# return value into a `Result` object.

print(result.unwrap())
# If the calculation succeded, it will be printed,
# otherwise it will throw an exception. However we
# can provide a default value:

print(result.unwrap_or(42))
import time
print(result.unwrap_or_else(lambda: time.time_ns()))

# Checking if a function succeded can be done by
# calling one of the `is_*` methods:
print(f"{result.is_none() = }")
print(f"{result.is_some() = }")
print(f"{result.is_some_and(lambda x: x % 2 == 0) = }")

# ... and much more feautures ...
```
