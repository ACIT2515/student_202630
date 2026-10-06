# Understanding \*args and \*\*kwargs

## Introduction

In Python, `*args` and `**kwargs` are special syntax that allow functions to
accept a variable number of arguments. They're essential for writing flexible
functions

- `*args` - collects positional arguments into a tuple
- `**kwargs` - collects keyword arguments into a dictionary

## Part 1: The Unpacking Operators

### The `*` Operator (Unpacking)

The `*` operator can **unpack** iterables (lists, tuples, etc.) into individual
elements.

```python
# Unpacking a list into function arguments
def add_three_numbers(a, b, c):
    return a + b + c

numbers = [1, 2, 3]
result = add_three_numbers(*numbers)  # Same as add_three_numbers(1, 2, 3)
print(result)  # 6

# Unpacking in list creation
first_list = [1, 2, 3]
second_list = [4, 5, 6]
combined = [*first_list, *second_list]  # [1, 2, 3, 4, 5, 6]
print(combined)
```

### The `**` Operator (Unpacking Dictionaries)

The `**` operator can **unpack** dictionaries into keyword arguments.

```python
# Unpacking a dictionary into keyword arguments
def greet(name, age, city):
    return f"{name} is {age} years old and lives in {city}"

person = {"name": "Alice", "age": 30, "city": "Vancouver"}
message = greet(**person)  # Same as greet(name="Alice", age=30, city="Vancouver")
print(message)

# Unpacking in dictionary creation
defaults = {"color": "blue", "size": "medium"}
custom = {"size": "large", "style": "modern"}
merged = {**defaults, **custom}  # {"color": "blue", "size": "large", "style": "modern"}
print(merged)  # Note: custom["size"] overwrites defaults["size"]
```

## Part 2: \*args (Arbitrary Positional Arguments)

### What is \*args?

`*args` allows a function to accept any number of positional arguments, which
are collected into a **tuple**.

```python
def sum_all(*args):
    """Sum any number of arguments"""
    total = 0
    for num in args:
        total += num
    return total

print(sum_all(1, 2, 3))           # 6
print(sum_all(10, 20, 30, 40))    # 100
print(sum_all(5))                  # 5
print(sum_all())                   # 0

# Inside the function, args is a tuple
def show_args(*args):
    print(f"Type: {type(args)}")   # Type: <class 'tuple'>
    print(f"Values: {args}")

show_args(1, 2, 3)  # Values: (1, 2, 3)
```

### Combining Regular Parameters with \*args

Regular parameters must come **before** `*args`.

```python
def greet_multiple(greeting, *names):
    """Greet multiple people with the same greeting"""
    for name in names:
        print(f"{greeting}, {name}!")

greet_multiple("Hello", "Alice", "Bob", "Charlie")
# Output:
# Hello, Alice!
# Hello, Bob!
# Hello, Charlie!

# greeting = "Hello"
# names = ("Alice", "Bob", "Charlie")
```

### Common Use Case: Forwarding Arguments

```python
def logger(func):
    """Decorator that logs function calls"""
    def wrapper(*args):  # Accept any positional arguments
        print(f"Calling {func.__name__} with args: {args}")
        result = func(*args)  # Pass them along to the original function
        return result
    return wrapper

@logger
def multiply(a, b, c):
    return a * b * c

multiply(2, 3, 4)
# Output: Calling multiply with args: (2, 3, 4)
```

## Part 3: \*\*kwargs (Arbitrary Keyword Arguments)

### What is \*\*kwargs?

`**kwargs` allows a function to accept any number of keyword arguments, which
are collected into a **dictionary**.

```python
def print_info(**kwargs):
    """Print key-value pairs"""
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_info(name="Alice", age=30, city="Vancouver")
# Output:
# name: Alice
# age: 30
# city: Vancouver

# Inside the function, kwargs is a dictionary
def show_kwargs(**kwargs):
    print(f"Type: {type(kwargs)}")   # Type: <class 'dict'>
    print(f"Values: {kwargs}")

show_kwargs(a=1, b=2, c=3)  # Values: {'a': 1, 'b': 2, 'c': 3}
```

### Combining Parameters with \*\*kwargs

Regular parameters and `*args` must come **before** `**kwargs`.

```python
def create_profile(name, *hobbies, **details):
    """Create a user profile"""
    print(f"Name: {name}")

    if hobbies:
        print(f"Hobbies: {', '.join(hobbies)}")

    for key, value in details.items():
        print(f"{key}: {value}")

create_profile(
    "Alice",                    # name (regular parameter)
    "reading", "hiking",        # hobbies (*args)
    age=30,                     # details (**kwargs)
    city="Vancouver",
    occupation="Developer"
)
# Output:
# Name: Alice
# Hobbies: reading, hiking
# age: 30
# city: Vancouver
# occupation: Developer
```

### Common Use Case: Configuration Functions

```python
def connect_database(host, port=5432, **options):
    """Connect to a database with flexible options"""
    print(f"Connecting to {host}:{port}")

    # Handle additional options
    if "timeout" in options:
        print(f"Timeout: {options['timeout']} seconds")
    if "ssl" in options:
        print(f"SSL: {options['ssl']}")

    # Access all other options
    for key, value in options.items():
        if key not in ["timeout", "ssl"]:
            print(f"{key}: {value}")

connect_database(
    "localhost",
    port=3306,
    timeout=30,
    ssl=True,
    max_connections=100
)
```

## Part 4: Using \*args and \*\*kwargs Together

You can use both in the same function, but they must follow this order:

1. Regular parameters
2. `*args`
3. `**kwargs`

```python
def flexible_function(required, *args, **kwargs):
    """A function that accepts everything"""
    print(f"Required: {required}")
    print(f"Extra positional (*args): {args}")
    print(f"Extra keyword (**kwargs): {kwargs}")

flexible_function(
    "must have this",       # required
    1, 2, 3,                # args
    name="Alice",           # kwargs
    age=30
)
# Output:
# Required: must have this
# Extra positional (*args): (1, 2, 3)
# Extra keyword (**kwargs): {'name': 'Alice', 'age': 30}
```

### Practical Example: Wrapper Functions

This is the key pattern used in decorators!

```python
def log_function_call(func):
    """Decorator that logs any function call"""
    def wrapper(*args, **kwargs):
        # Accept any arguments
        print(f"Calling {func.__name__}")
        print(f"  Positional args: {args}")
        print(f"  Keyword args: {kwargs}")

        # Forward all arguments to the original function
        result = func(*args, **kwargs)

        print(f"  Result: {result}")
        return result
    return wrapper

@log_function_call
def calculate_total(price, quantity, tax=0.12, discount=0):
    """Calculate total with tax and discount"""
    subtotal = price * quantity
    total = subtotal * (1 + tax) * (1 - discount)
    return total

# This works with any combination of arguments!
calculate_total(10, 5)                          # price=10, quantity=5
calculate_total(10, 5, tax=0.15)                # with custom tax
calculate_total(10, 5, discount=0.1)            # with discount
calculate_total(10, 5, tax=0.15, discount=0.2)  # with both
```

## Common Patterns and Best Practices

### 1. Forwarding Arguments to Another Function

```python
def enhanced_print(*args, **kwargs):
    """Print with a timestamp"""
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}]", *args, **kwargs)

enhanced_print("Hello", "World", sep=", ")
# [2024-01-15 10:30:45] Hello, World
```

### 2. Default Values with \*\*kwargs

```python
def create_user(**kwargs):
    """Create user with defaults"""
    # Provide defaults using .get()
    name = kwargs.get("name", "Anonymous")
    age = kwargs.get("age", 0)
    active = kwargs.get("active", True)

    return {
        "name": name,
        "age": age,
        "active": active
    }

user1 = create_user(name="Alice", age=30)
user2 = create_user()  # Uses all defaults
```

### 3. Extracting Specific Arguments from \*\*kwargs

```python
def process_data(**kwargs):
    """Process data with specific and extra parameters"""
    # Extract specific parameters
    required_param = kwargs.pop("required")  # Remove and get value
    optional_param = kwargs.pop("optional", "default")

    # kwargs now contains only "extra" parameters
    print(f"Required: {required_param}")
    print(f"Optional: {optional_param}")
    print(f"Extra parameters: {kwargs}")

process_data(required="must have", optional="custom", extra1=1, extra2=2)
```

## Quick Reference

| Syntax     | Purpose                              | Collected As | Example                                        |
| ---------- | ------------------------------------ | ------------ | ---------------------------------------------- |
| `*args`    | Accept variable positional arguments | Tuple        | `func(1, 2, 3)` → `args = (1, 2, 3)`           |
| `**kwargs` | Accept variable keyword arguments    | Dictionary   | `func(a=1, b=2)` → `kwargs = {'a': 1, 'b': 2}` |
| `*list`    | Unpack list/tuple into arguments     | N/A          | `func(*[1, 2, 3])` → `func(1, 2, 3)`           |
| `**dict`   | Unpack dict into keyword arguments   | N/A          | `func(**{'a': 1})` → `func(a=1)`               |

## Common Mistakes to Avoid

```python
# WRONG: kwargs before args
# def wrong(*args, **kwargs, regular):  # SyntaxError!

# CORRECT: Regular parameters first, then *args, then **kwargs
def correct(regular, *args, **kwargs):
    pass

# WRONG: Multiple *args
# def wrong(*args1, *args2):  # SyntaxError!

# CORRECT: Only one *args
def correct(*args):
    pass

# WRONG: Multiple **kwargs
# def wrong(**kwargs1, **kwargs2):  # SyntaxError!

# CORRECT: Only one **kwargs
def correct(**kwargs):
    pass
```

## Key Takeaways

1. `*args` collects extra **positional** arguments into a **tuple**
2. `**kwargs` collects extra **keyword** arguments into a **dictionary**
3. Order matters: `func(regular, *args, **kwargs)`
4. Use `*` to **unpack** iterables, `**` to **unpack** dictionaries
