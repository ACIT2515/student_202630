
# Python basics - ACIT 2515

# General 

* Python is **strongly** but **dynamically** typed language
* The correct type of a variable **can only be known** at runtime
* **RUN THE CODE** it is better than looking at your editor colors or text decorations to debug your code
* Types can be defined with annotations and checked with a type checker and 
* Run your code with `python ...` in the terminal, or via your editor.
 
# Variables

* are symbolic names pointing to objects or values in memory.
* variables are defined by assigning them a value using the assignment operator.
* In Python variables are dynamically typed, allowing type changes through reassignment.

Python variable names can include letters, digits, and underscores but can’t start with a digit. You should use snake case for multi-word names to improve readability.
* Variables exist in different scopes (global, local, non-local, or built-in), which affects how you can access them.
You can have an unlimited number of variables in Python, limited only by computer memory.
* Declare, assign, set a variable (save a value): `my_variable = "something"`
* Use meaningful names for variables. Your variable names should have at least 4 letters.
* Python variables should follow the **snakecase** convention (`my_great_variable`, not `myGreatVariable`)
* Constants should be uppercase: `NUMBER_OF_ATTEMPTS = 2`
* All variables have a type: `type(my_variable)`

<div style="page-break-after: always;"></div>

## Python built-in data types

* **Numeric Types** (Immutable) — Represent numbers for arithmetic and math.
  * `int` — Whole numbers, unlimited precision (e.g., 42, -7).
  * `float` — Decimal numbers, double precision (e.g., 3.14, -0.001).
  * `complex` — Numbers with real and imaginary parts (e.g., 2+3j).
* **Boolean Type** (Immutable) — Logical truth values.
  * `bool` — True or False (subclass of int).
* **None Type** (Immutable) — Represents the absence of a value.
  * `NoneType` — Only one instance: `None`.
* **Sequence Types** — Ordered collections of items.
  * Immutable
    * `str` — Text data, sequence of Unicode characters.
    * `tuple` — Ordered, fixed-size collection of items.
    * `range` — Sequence of numbers, often used in loops.
  * Mutable
    * `list` — Ordered, resizable collection of items.
* **Mapping Types** — Key-value pairs.
  * Mutable
    * `dict` — Unordered collection mapping keys to values.
* **Set Types** — Unordered collections of unique elements.
  * Mutable
    * `set` — Mutable set of unique items.
  * Immutable
    * `frozenset` — Immutable set of unique items.
* **Binary Types** — Store sequences of bytes.
  * Immutable
    * `bytes` — Immutable sequence of bytes.
  * Mutable
    * `bytearray` — Mutable sequence of bytes.

<div style="page-break-after: always;"></div>

## [Numeric types](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)

"Numbers". Transform (= *cast*) one type to the other:

```python
round_number = 20
float_number = 42.4
string_number = "100"

int(float_number)             # 42
int(string_number)            # 100 (not '100' !)
float(round_number)           # 20.0
```

Because of the binary representation of floating point numbers, rouding errors can happen:
```python
0.1 + 0.1 + 0.1 != 0.3
```

* Types: `int`, `float`, `complex`
* Can do arithmetics: `a + b`, `a - b`, `a * b`, `a / b`
* Integer division and modulo: `14 // 3 == 4`, `14 % 3 == 2` (14 = 4 * 3 + 2)
* Complex math are done with `import math`
* `math.sqrt`, `math.pow`, `math.log`

<div style="page-break-after: always;"></div>

## Booleans: `bool`

* Use `==` to check if two values are equal, `!=` if they are different. **`=` assigns a value to a variable**! See also: [Comparisons](https://docs.python.org/3/library/stdtypes.html#comparisons).
* A boolean value can only be `True` or `False`. You can combine logic with `and`, `or`, and `not`. See [boolean operators](https://docs.python.org/3/library/stdtypes.html#boolean-operations-and-or-not).

```python
rich = True
beautiful = True
attractive = rich and beautiful
```

Remember that `not (A and B)` is `not A or not B`, and is not the same as `not A and not B`!

```python
not_attractive = not (rich and beautiful)
not_attractive = not rich or not beautiful
very_unattractive = not rich and not beautiful
```

Note: `None` is also a built-in value (it is neither `True` nor `False`).

<div style="page-break-after: always;"></div>



## Strings (text)

Strings are very much like "lists of characterers". In Python, **string are immutable** (you cannot change a string, only make a copy with changes).

* Type `str`, defined with single quotes `'text'`, double quotes `"text"`. or triple quotes `"""text"""`
* Useful: `split`, `join`, `upper`, `lower`, `isnumeric`
* Use f-strings: `my_string = f"Hello {name}, nice to meet you!"`
* `"abc de f".split()` => `["abc", "de", "f"]`
* `" ".join(["abc", "de", "f"])` => `"abc de f"`
* See also: [common string operations](https://docs.python.org/3/library/string.html)

### [String methods](https://docs.python.org/3/library/stdtypes.html#string-methods)

```python
my_string = "hello world"
my_string[0]                  # 'h'
my_string[0] = "H"            # ERROR! Strings are immutable
my_string.upper()             # 'HELLO WORLD'
my_string.split(' ')          # ['hello', 'world']
' '.join(['hello', 'world'])  # 'hello world'
'HELLO WORLD'.lower()         # 'hello world'
'world' in my_string          # True
```

# Iterate on strings like lists

```python
for letter in my_string:
    print(letter)
```

# Convert strings to numbers and vice-versa

```python
my_string = "12345"
int(my_string)          # 12345
another = "abc"
int(another)            # Raises an Exception!
```

### Careful... `123 != "123"`

<div style="page-break-after: always;"></div>

# Conditionals and Loops

## Conditions: `if`

```python
if condition:
    # runs if condition is True
elif another:
    # runs if condition is False and another is True
else:
    # runs if condition is False and another is False
```

There is also a short version (one-liner) for `if` statements.

```python
can_drink = True if age > 18 else False
```

<div style="page-break-after: always;"></div>

## Loops

* Loops repeat a block of code multiple times
* `for` loops iterate over a known collection (a `list`, `range`, `str`, ...)
* `while` loops repeat as long as a condition is `True`

```python
for value in [1, 2, 3]:
    print(value)          # Runs once per element: 1, 2, 3

for i in range(3):
    print(i)               # Runs once per number: 0, 1, 2

count = 0
while count < 3:
    print(count)           # Runs while the condition is True
    count += 1             # Don't forget to update the condition!
```

* `break` exits the loop immediately
* `continue` skips to the next iteration

<div style="page-break-after: always;"></div>

# Exploring Some Benefits of Functions

Why use functions? They provide:

* **Abstraction** - hide implementation details behind a simple, descriptive name
* **Encapsulation** - variables defined inside a function stay local to it (their own **namespace** / scope)
* **Modularity** - break a large program into smaller, focused pieces
* **Reusability** - write the logic once, call it from many places (the **DRY** principle: Don't Repeat Yourself)
* **Maintainability** - fix or improve behavior in a single place (the function definition)
* **Testability** - functions with clear inputs/outputs are easier to test in isolation

<div style="page-break-after: always;"></div>

# Functions in Python

* A function is a named, reusable block of code that performs a specific task
* Python has built-in functions (`len()`, `print()`, `id()`, ...), and you can also define your own (**user-defined functions**)
* Defining a function means choosing its name, its parameters (if any), and what it computes
* Calling a function runs its code, then returns control (and possibly a value) back to the caller
* A variable defined inside a function is only "known" within that function (**variable scoping**)
* Global variables are bad. Just don't - use functions, arguments and return values instead

See also: [functions](https://docs.python.org/3/library/functions.html).

<div style="page-break-after: always;"></div>

# Defining Functions in Python

```python
def function_name(parameter_1, parameter_2):
    # function body (must be indented)
    return parameter_1 + parameter_2
```

* `def` starts the definition, followed by the function name and a required pair of parentheses
* Parameters go inside the parentheses (optional - a function can take zero parameters)
* The `:` ends the header. The indented block below is the function's **body**
* A function body can't be empty - use `pass` as a placeholder (a **stub**) if needed

```python
def not_implemented_yet():
    pass   # valid, but does nothing
```

<div style="page-break-after: always;"></div>

# Calling Functions in Python

```python
function_name(argument_1, argument_2)
```

* Call a function using its name followed by `()`, even if it takes no arguments
* Forgetting the parentheses does **not** call the function - it just refers to the function object

### Positional arguments

```python
def calculate_cost(item, quantity, price):
    print(f"{quantity} {item} cost ${quantity * price:.2f}")

calculate_cost("bananas", 6, 0.74)   # arguments are matched by position / order
```

* Arguments are matched to parameters **in order**
* The number of arguments must match the number of parameters (unless defaults are used)

### Keyword arguments

```python
calculate_cost(item="bananas", quantity=6, price=0.74)
calculate_cost(price=0.74, quantity=6, item="bananas")   # order doesn't matter
calculate_cost("bananas", quantity=6, price=0.74)        # can mix positional + keyword
```

* Keyword arguments are matched **by name**, so their order doesn't matter
* Improves readability, especially for functions with many parameters
* All positional arguments must come before keyword arguments in a call

<div style="page-break-after: always;"></div>

# Returning From Functions

* Functions can affect the program in two (non-exclusive) ways:
  * Cause a **side effect** (e.g. modify a mutable argument, print something)
  * **Return a value** to the caller with `return`
* Prefer returning values over relying on side effects - it makes functions easier to test and reason about

```python
def double_bad(numbers):        # BAD: mutates the input (a side effect)
    for i, _ in enumerate(numbers):
        numbers[i] *= 2

def double(numbers):            # GOOD: returns a new list, no side effect
    return [number * 2 for number in numbers]
```

* `return` immediately exits the function and sends a value back to the caller
* If the `return` statement has no expression, or is omitted entirely, the function returns `None`
* `return` can also be used to exit a function early

```python
def find_user(username, user_list):
    for user in user_list:
        if user["username"] == username:
            return user   # exits early, as soon as a match is found
    return None            # explicit: "no user was found"
```

* Compare a possibly-`None` result with `is` / `is not`, not `==`

```python
if find_user("linda", users) is None:
    print("Linda isn't a registered user")
```

* A function can return **multiple values** - they are packed into a `tuple`

```python
def create_point(x, y):
    return x, y

create_point(2, 4)   # (2, 4)
```

<div style="page-break-after: always;"></div>

## Default argument values

```python
def greet(name="World"):
    print(f"Hello, {name}!")

greet()               # Hello, World!
greet("Pythonista")   # Hello, Pythonista!
```

* A default value makes a parameter optional
* :warning: never use a mutable object (`[]`, `{}`) as a default value - it's created **once** and shared across all calls. Use `None` as a sentinel instead:

```python
def append_to(item, target=None):
    if target is None:
        target = []
    target.append(item)
    return target
```


<div style="page-break-after: always;"></div>

# Debug your programs

* Use the debugger.
* You may also use `print`, it's better than nothing.
* Whatever tool you use, your brain does the debugging. The tools are here to help, but won't give you the answer.
* Read the error messages. 9 times out of 10, the solution to the problem is on the screen.
* Every time you make a change to your code, **RUN THE CODE**.
* Do not make multiple changes to the code. Fix one problem at a time.

<div style="page-break-after: always;"></div>

# Code structure

* Separate code into functions
* Separate functions into modules (Python files)
* Organize modules into packages (files in folders)
* Don't forget about `__init__.py` files for packages!
* Use `if __name__ == "__main":` in your modules, to debug and prevent unwanted code execution.
* Create a single entrypoint in your program, and then use modules / packages to organize the logic.

```
├── component_1
│   ├── __init__.py
│   └── sub_package
│       ├── __init__.py
│       ├── sub_module_1.py
│       └── sub_module_2.py
├── component_2
│   ├── __init__.py
│   └── [... files ...]
├── component_3
│   ├── __init__.py
│   └── [... files ...]
└── main.py
```

