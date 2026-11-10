# A Gentle Introduction to Python Lambda Functions

## What Is a Lambda Function?

A lambda creates a small, unnamed function, also called an anonymous function.
Its body is a single expression:

```python
lambda parameters: expression
```

The parameters are the inputs. The expression after `:` is returned
automatically; do not write `return`.

For example, these two functions do the same thing:

```python
def add_one(number):
    """Return the number plus one."""
    return number + 1
```

```python
lambda number: number + 1
```

Both create a function; neither calls it.

### Calling a Lambda Immediately

Put parentheses around the lambda, then add parentheses with its arguments:

```python
result = (lambda number: number + 1)(5)
print(result)  # 6
```

The `(5)` calls the new function immediately with `5`. This is an immediately
invoked function expression. It is valid, although `5 + 1` is clearer here.

## Why Use a Lambda?

A lambda provides simple behaviour right where it is needed, without a
separate `def`. It is a convenience, not a requirement.

## When Should We Use One?

Use a lambda when the behaviour is short, simple, and needed in one place.
Common uses are collection callbacks and simple replacements in tests.

### Common Built-in Functions and Methods That Accept Callbacks

A callback is a function passed to other code for that code to call.
The functions below call our callback with each item in a collection.

Pass the function itself, not the result of calling it. A `def` function or an
existing function such as `len` also works.

#### `sorted()`: Order Items Using a Key

`sorted()` returns a new list. Its `key` callback supplies the value used to
order each item. Here, that value is the length of each server name:

```python
servers = ["database-01", "web-01", "dns"]
ordered_servers = sorted(servers, key=lambda name: len(name))
print(ordered_servers)  # ['dns', 'web-01', 'database-01']
```

The original list is unchanged. Add `reverse=True` for longest names first.
Since `len` already does this job, `key=len` is a simpler alternative here.

#### `list.sort()`: Change the Existing List

This list method accepts the same kind of key callback as `sorted()`:

```python
servers = ["database-01", "web-01", "dns"]
servers.sort(key=lambda name: len(name))
print(servers)  # ['dns', 'web-01', 'database-01']
```

It changes the existing list and returns `None`; do not assign that result
back to `servers`.

#### `min()` and `max()`: Select an Item Using a Key

These functions select the item with the smallest or largest key.
Here, each tuple contains a server name and its response time:

```python
servers = [("web-01", 80), ("db-01", 20), ("dns-01", 45)]
fastest = min(servers, key=lambda server: server[1])
slowest = max(servers, key=lambda server: server[1])
print(fastest)  # ('db-01', 20)
print(slowest)  # ('web-01', 80)
```

`server[1]` supplies the response time for comparison. The result is the
selected tuple, not just its response time.

#### `map()`: Transform Each Item

`map()` uses the callback to transform each item:

```python
servers = ["WEB-01", "DNS-01", "DB-01"]
lowercase_names = list(map(lambda name: name.lower(), servers))
print(lowercase_names)  # ['web-01', 'dns-01', 'db-01']
```

The lambda returns a lowercase name. `map()` returns an iterator (values
produced as requested); `list()` collects those values into a list.

#### `filter()`: Keep Items That Pass a Check

`filter()` keeps items for which the callback returns a truthy result.
Here, the comparison returns `True` for response times above 100 milliseconds:

```python
response_times = [25, 180, 40, 250]
slow_responses = list(filter(lambda milliseconds: milliseconds > 100, response_times))
print(slow_responses)  # [180, 250]
```

Unlike `map()`, this selects original items rather than transforming them.
It also returns an iterator, so we use `list()` to collect the results.

### Providing a Predictable Answer in a Test

The pytest `monkeypatch` fixture temporarily replaces a function.
This replacement accepts a prompt and always returns `"yes"`:

```python
def test_confirmation(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda prompt: "yes")

    answer = input("Restart the server? ")

    assert answer == "yes"
```

The lambda accepts `prompt` because this call to `input()` supplies one,
even though it ignores the value. Pass the lambda without calling it:
`input()` calls the replacement later. Pytest restores the original afterward.
This demonstrates a replacement, not a test of real keyboard input.

Match the arguments the calling code supplies: `lambda: 10` takes none;
`lambda used, total: used / total` takes two.

## When Is `def` Better?

Use `def` when a function needs several steps, a loop, error handling, a
docstring, or a descriptive name for reuse. Prefer clarity over saving lines.
