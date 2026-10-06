# Higher Order Functions and Decorators

## Introduction

**Higher order functions** are functions that either:

- Take one or more functions as arguments, OR
- Return a function as their result

**Decorators** are a special application of higher order functions that modify
or enhance the behavior of other functions

## Part 1: Higher Order Functions

### What Problems Do They Solve?

Higher order functions help solve problems involving:

- Code reuse and avoiding repetition
- Separating concerns (what to do vs. how to do it)
- Adding behavior to existing functions without modifying them
- Creating configurable behavior

### Functions as Arguments

```python
def hello(name):
    return f"Hello, {name}!"

def shout(name):
    return f"HEY {name.upper()}!"

def greeter(names, greet_func):
    """Process a list of names using any greeting function"""
    return [greet_func(name) for name in names]

# Use it
names = ["Alice", "Bob", "Charlie"]
print(greeter(names, hello))   # ['Hello, Alice!', 'Hello, Bob!', 'Hello, Charlie!']
print(greeter(names, shout))   # ['HEY ALICE!', 'HEY BOB!', 'HEY CHARLIE!']
```

**Note**: `greeter` doesn't care HOW to format names, it just knows to apply
whatever function we give it.

### Functions That Return Functions

```python
def create_multipler(n):
    """Returns a function that multiplies by n"""
    def multiplier(x):
        return x * n
    return multiplier

# Create specialized functions
doubler = create_multiplier(2)
tripler = create_multiplier(3)

print(doubler(5))  # 10
print(tripler(5))  # 15
```

**Use case**: Creating customized functions on-the-fly without writing separate
function definitions.

### Closures

A **closure** occurs when a nested function "remembers" variables from its
enclosing scope, even after the outer function has finished executing.

```python
def create_counter():
    """Returns a function that counts up from 0"""
    count = 0  # This variable is "captured" by the closure
    
    def increment():
        nonlocal count  # Access the enclosing scope's variable
        count += 1
        return count
    
    return increment

# Each counter has its own independent 'count' variable
counter1 = create_counter()
counter2 = create_counter()

print(counter1())  # 1
print(counter1())  # 2
print(counter2())  # 1 (independent from counter1)
print(counter1())  # 3
```

**Key points:**
- The inner function (`increment`) captures `count` from the enclosing scope
- The `count` variable persists between function calls
- Each closure has its own independent copy of the captured variables
- Use `nonlocal` keyword to modify variables from the enclosing scope

**Why variables from the enclosing scope aren't lost:**

When a nested function references a variable from its enclosing scope, Python
creates a closure by storing a reference to that variable (not just its value).
The returned function object maintains these references in a special attribute
called `__closure__`. As long as the returned function exists, Python keeps the
captured variables alive in memory, even though the outer function has finished
executing. This is why `count` persists across multiple calls to `counter1()` -
it's not a global variable, but rather a variable that's "kept alive" by the
closure mechanism.

**Why closures matter:** Decorators rely heavily on closures to maintain state
and access the original function being decorated.

### Practical Example: Validation

```python
def create_validator(min_val, max_val):
    """Returns a validation function with specific bounds"""
    def validate(value):
        return min_val <= value <= max_val

    return validate

# Create different validators
age_validator = create_validator(0, 120)
percentage_validator = create_validator(0, 100)

print(age_validator(25))    # True
print(age_validator(150))   # False
print(percentage_validator(50))  # True
```

## Part 2: Decorators

### What Are Decorators?

Decorators are a feature of Python ("syntactic sugar") for applying higher order
functions. They "wrap" a function to modify its behavior being invoked before
and completing after the function that they wrap.

### Simple Decorator Example

```python
def uppercase_decorator(func):
    """Decorator that converts function output to uppercase"""
    def wrapper():
        result = func()
        return result.upper()
    return wrapper

# Create greet without @ decorator syntax
def greet():
    return "hello, world"

# "Manually" re-assign greet to uppercase_decorator with itself as parameter
# note: the "inner" greet isn't being invoked
greet = uppercase_decorator(greet)

# Calling the "wrapped" version of greet
print(greet())  # "HELLO, WORLD"

# Using @ syntax - the outcome is the same as with greet but cleaner
@uppercase_decorator
def greet2():
    return "hello, world"

# Invoke the "wrapped" greet2
print(greet2())  # "HELLO, WORLD"
```

**What happened?** The decorator replaced our original function with a wrapped
version.

### Decorator with Arguments

```python
def repeat(times):
    """Decorator factory that repeats function output"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return result * times
        return wrapper
    return decorator

@repeat(3)
def say_hi(name):
    return f"Hi {name}! "

print(say_hi("Alice"))  # "Hi Alice! Hi Alice! Hi Alice! "
```

### Function Metadata

Every Python function has built-in attributes (metadata) that describe it. These
attributes help with debugging, documentation, and introspection.

#### Common Function Attributes

```python
def greet(name):
    """Say hello to someone"""
    return f"Hello, {name}!"

# Access function metadata
print(greet.__name__)      # 'greet'
print(greet.__doc__)       # 'Say hello to someone'
print(greet.__module__)    # '__main__'
```

### Example 1: Using `__doc__` for Help Text

```python
def add(a, b):
    """Add two numbers together"""
    return a + b

def subtract(a, b):
    """Subtract b from a"""
    return a - b

# Show function documentation
print(f"{add.__name__}: {add.__doc__}")
# Output: add: Add two numbers together

print(f"{subtract.__name__}: {subtract.__doc__}")
# Output: subtract: Subtract b from a

# Built-in help() also uses __doc__
help(add)  # Displays the docstring
```

#### Example 2: Using `__name__` for Logging

```python
def log_function_call(func):
    """Decorator that logs function calls using function name"""
    def wrapper(*args, **kwargs):
        # Use func.__name__ to show which function was called
        print(f"[LOG] Calling {func.__name__}()")
        return func(*args, **kwargs)
    return wrapper

@log_function_call
def process_data():
    return "Data processed"

process_data()  # Output: [LOG] Calling process_data()

# But note that by decorating process_data we have hidden its metadata
print(f"process_data thinks its name is: {process_data.__name__})
# Output: process_data thinks its name is: wrapper 
```


**Key Point**: Decorators lose this metadata unless you add it back, i.e. use

### `functools.wraps()`

#### The Role of functools.wraps

When you use a decorator without special handling, the decorated function loses
its original metadata (like its name, docstring, and argument list), taking on
the metadata of the inner wrapper function instead. This can make debugging and
documentation difficult.

Using the `@functools.wraps(func)` decorator on your wrapper function solves this
issue: It preserves key attributes of the original function
(`__name__`,` __doc__`, etc.), making the decorated function look and behave
more like the original.

It improves debugging by ensuring stack traces and logs show the correct
function names.

It ensures documentation tools (like `help()`) extract the correct information.

```python
from functools import wraps

def my_decorator(func):

    @wraps(func)  # Preserves original function's metadata
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def important_function():
    """This docstring is preserved"""
    pass

print(important_function.__doc__)  # 'This docstring is preserved'
```

### Common Decorator Use Cases

#### 1. Logging

```python
from functools import wraps

def log_calls(func):
    """Log when a function is called"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with {args}, {kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result
    return wrapper

@log_calls
def add(a, b):
    return a + b

add(3, 5)
# Output:
# Calling add with (3, 5), {}
# add returned 8
```

#### 2. Timing Function Execution

```python
from functools import wraps
import time 

def timer(func):
    """Measure how long a function takes to run"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(1)
    return "Done!"

slow_function()  # slow_function took 1.0012 seconds
```

#### 3. Input Validation

```python
from functools import wraps

def validate_positive(func):
    """Ensure all numeric arguments are positive"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        for arg in args:
            if isinstance(arg, (int, float)) and arg < 0:
                raise ValueError(f"Negative value not allowed: {arg}")
        return func(*args, **kwargs)
    return wrapper

@validate_positive
def calculate_area(width, height):
    return width * height

print(calculate_area(5, 10))  # 50
# calculate_area(-5, 10)  # Raises ValueError
```

#### 4. Caching/Memoization

```python
from functools import wraps

def memoize(func):
    """Cache function results to avoid recomputation"""
    cache = {}

    @wraps(func)
    def wrapper(*args):
        if args in cache:
            print(f"Returning cached result for {args}")
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result
    return wrapper

@memoize
def factorial(n):
    """Calculate factorial with memoization"""
    if n <= 1:
        return 1
    return n * factorial(n - 1)

print(factorial(5))   # Computes: 120
print(factorial(6))   # Only computes 6! using cached 5!
print(factorial(5))   # Returns cached result

```

**Why memoization is useful:**

- Avoids expensive recalculations
- Speeds up recursive functions dramatically
- Perfect for pure functions (same input = same output)
- Common for API calls, database queries, complex calculations

## Key Takeaways

1. **Higher order functions** treat functions as data - they can be passed
   around and returned
2. **Decorators** are a special syntax for wrapping functions to add behavior
3. Both promote **code reuse** and **separation of concerns**
4. Common patterns: logging, timing, validation, caching, authentication
5. Use `*args, **kwargs` in wrappers to handle any function signature

