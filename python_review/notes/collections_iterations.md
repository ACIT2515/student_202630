# Python Collections and Iteration

Collections store multiple values in one variable. Choose a collection based on
how the data must be organized: by position, by name, by uniqueness, or by a
numeric sequence.

## Choosing a Collection

| Type | Solves this problem | Ordered | Mutable | Indexed | Allows duplicates |
| --- | --- | --- | --- | --- | --- |
| `list` | A changeable sequence of values | Yes | Yes | Yes | Yes |
| `tuple` | A fixed sequence of related values | Yes | No | Yes | Yes |
| `set` | A group of unique values | No | Yes | No | No |
| `dict` | Values identified by unique keys | Yes* | Yes | By key | Keys: no; values: yes |
| `range` | A calculated sequence of integers | Yes | No | Yes | No** |

\* Dictionaries preserve insertion order in modern Python. This does not make
them positional sequences; access is by key.

\*\* A `range` can describe repeated numbers when its step causes repetition in
the requested direction, but normal positive-step ranges contain no duplicates.

## Lists

### Why and when

A list solves the problem of storing an ordered group that may grow, shrink, or
have individual values replaced. Use it for services to check, log entries, or
other data where order matters and duplicates are meaningful.

### Characteristics

- Ordered sequence; positions start at `0`.
- Mutable: items can be added, removed, or replaced.
- Allows duplicates and values of different types.
- Supports indexing, slicing, iteration, `len()`, and membership testing.

```python
services = ["Spooler", "W32Time", "WinRM"]

print(services[0])
services.append("Dhcp")
services[1] = "TimeBrokerSvc"
print(services)
```

Common list operations:

- `items.append(value)`: add one value to the end
- `items.extend(values)`: add several values
- `items.insert(index, value)`: insert at a position
- `items.remove(value)`: remove a value
- `items.pop()`: remove and return the last value
- `items.sort()`: sort the list in place
- `items.reverse()`: reverse the list in place
- `items.count(value)`: count matching values
- `items.index(value)`: find the first matching position
- `len(items)`: count the values
- `value in items`: check whether a value exists

Useful list attributes and syntax include `items[0]`, `items[start:stop]`, and
`items` itself. Lists have no special data attributes that replace these
operations; their behavior is provided mainly through methods.

## Tuples

### Why and when

A tuple solves the problem of grouping related values that should be treated as
one fixed record. Use it for coordinates, configuration pairs, or values
returned together from a function when callers should not modify the structure.

### Characteristics

- Ordered, immutable sequence.
- Supports indexing, slicing, iteration, `len()`, and membership testing.
- Allows duplicates and values of different types.
- Can be used as a dictionary key when all its contents are hashable.

```python
server_location = ("server01", "Vancouver", "rack-3")

print(server_location[0])
# server_location[0] = "server02"  # TypeError: tuples cannot be changed
```

Common tuple operations:

- `values.count(value)`: count matching values
- `values.index(value)`: find the first matching position
- `len(values)`: count the values
- `value in values`: check whether a value exists

A tuple with one item needs a trailing comma: `port = (443,)`. Tuple methods
cannot add, remove, or replace items because tuples are immutable.

## Sets

### Why and when

A set solves the problem of tracking unique values and comparing groups of
values. Use it when duplicates must be ignored, such as recording the distinct
ports found while inspecting a host.

### Characteristics

- Unordered collection with no positional indexes.
- Mutable: values can be added or removed.
- Every element must be hashable; lists and dictionaries cannot be elements.
- Supports fast membership testing and set algebra.

```python
open_ports = {80, 443, 443}
open_ports.add(22)

print(open_ports)  # Contains 80, 443, and 22 once each
print(443 in open_ports)
```

Common set operations:

- `values.add(value)`: add one value
- `values.update(other_values)`: add several values
- `values.remove(value)`: remove a value; raises `KeyError` if absent
- `values.discard(value)`: remove a value if present
- `values.union(other)`: values in either set
- `values.intersection(other)`: values in both sets
- `values.difference(other)`: values only in the first set
- `len(values)`: count the unique values

Sets do not support indexing or slicing. Use `set()` for an empty set; `{}` is
an empty dictionary.

## Dictionaries

### Why and when

A dictionary solves the problem of looking up values by meaningful keys instead
of numeric positions. Use it for records and mappings such as a hostname to IP
address, a service name to status, or a username to permissions.

### Characteristics

- Mapping of unique, hashable keys to values.
- Mutable: entries can be added, replaced, or removed.
- Preserves insertion order, but access is by key rather than position.
- Values may be duplicated and may have any type.
- Missing keys raise `KeyError` when accessed with square brackets.

```python
host = {
    "hostname": "server01",
    "ip_address": "192.168.1.10",
    "is_online": True,
}

print(host["hostname"])
host["port"] = 443
```

Accessing a missing key with `host["missing"]` raises a `KeyError`. Use `get()`
when a key may be absent:

```python
owner = host.get("owner", "not assigned")
print(owner)
```

Common dictionary operations and attributes:

- `mapping[key]`: get the value for a key
- `mapping[key] = value`: add or replace a key-value pair
- `mapping.get(key, default)`: get a value or a fallback value
- `mapping.pop(key)`: remove and return a value
- `mapping.setdefault(key, default)`: get a value, adding a default if absent
- `mapping.keys()`: view the keys
- `mapping.values()`: view the values
- `mapping.items()`: view key-value pairs
- `mapping.update(other)`: add or replace several entries
- `mapping.clear()`: remove all entries
- `key in mapping`: check whether a key exists
- `len(mapping)`: count the key-value pairs

## `range`

### Why and when

`range` solves the problem of generating a predictable sequence of integers for
iteration without storing every integer in memory. Use it for repetition,
indexes, attempt numbers, or bounded numeric loops.

### Characteristics

- Ordered, immutable sequence of integers.
- Supports indexing, slicing, iteration, `len()`, and membership testing.
- Uses little memory because it stores `start`, `stop`, and `step` rather than
    every number.
- The stop value is exclusive: `range(1, 4)` produces `1`, `2`, and `3`.

```python
for attempt in range(1, 4):
    print(f"Connection attempt {attempt}")
```

Common range attributes and operations:

- `numbers.start`: first value
- `numbers.stop`: exclusive upper boundary
- `numbers.step`: difference between values
- `numbers.count(value)`: count occurrences, usually `0` or `1`
- `numbers.index(value)`: find a value's position
- `len(numbers)`: count the generated values
- `value in numbers`: test membership

`range()` accepts `range(stop)`, `range(start, stop)`, or
`range(start, stop, step)`. A step of `0` raises `ValueError`.

## Iteration with `for`

A `for` loop runs once for each value in a collection. Use a descriptive loop
variable that represents one item.

```python
services = ["Spooler", "W32Time", "WinRM"]

for service_name in services:
    print(f"Checking {service_name}")
```

### Iterating Over Dictionaries

Iterate over `items()` when you need both each key and its value:

```python
host = {
    "hostname": "server01",
    "ip_address": "192.168.1.10",
}

for field_name, field_value in host.items():
    print(f"{field_name}: {field_value}")
```

Iterate directly over a dictionary when you need only keys. Use `values()` when
you need only values.

```python
for field_name in host:
    print(field_name)

for field_value in host.values():
    print(field_value)
```

## Other Looping Constructs

### `while` loops

Use a `while` loop when repetition depends on a condition and the number of
iterations is not known in advance. Change the condition inside the loop so it
eventually becomes false.

```python
attempt = 1
connected = False

while attempt <= 3 and not connected:
    print(f"Connection attempt {attempt}")
    connected = check_connection()
    attempt += 1
```

Use a `for` loop when processing each item in a collection or a known numeric
sequence. Use a `while` loop when continuing until a condition changes.

### `break` and `continue`

- `break` exits the nearest loop immediately.
- `continue` skips the rest of the current iteration and starts the next one.

```python
for service_name in services:
    if service_name == "Spooler":
        print("Required service found")
        break
    if service_name == "DisabledService":
        continue
    print(f"Checking {service_name}")
```

Use these statements for a clear early exit or to skip known exceptions. Avoid
using them so often that the loop's normal path becomes difficult to follow.

### Loop `else`

The `else` block runs when a loop finishes normally. It does not run when
`break` exits the loop.

```python
for service_name in services:
    if service_name == "Spooler":
        print("Required service found")
        break
else:
    print("Required service was not found")
```

This pattern is useful for searches: `break` handles the found case, and
`else` handles the not-found case.

### Nested loops

A nested loop is a loop inside another loop. Use one when each item in one group
must be compared with or combined with every item in another group.

```python
hosts = ["server01", "server02"]
ports = [80, 443]

for hostname in hosts:
    for port in ports:
        print(f"Checking {hostname}:{port}")
```

Nested loops can perform many operations, so keep the inner work small and
consider whether a set, dictionary, or helper function gives a clearer design.

### `enumerate()` and `zip()`

Use `enumerate()` when a loop needs both the position and the value. Use `zip()`
when related sequences should be processed together.

```python
for position, service_name in enumerate(services, start=1):
    print(f"{position}. {service_name}")

statuses = ["running", "stopped", "running"]
for service_name, status in zip(services, statuses):
    print(f"{service_name}: {status}")
```

`zip()` stops when the shortest input is exhausted. Use `itertools.zip_longest()`
when unmatched values must also be processed.

## Collection and Iteration Guidelines

1. Use a list when order matters and the collection may change.
1. Use a tuple when related values should not change.
1. Use a set when duplicate values must be ignored.
1. Use a dictionary when each value needs a meaningful key and for repeated lookups.
1. Use `range` when a loop needs a calculated sequence of integers.
1. Iterate directly over values with `for value in collection` rather than
   manually using indexes when the index is not needed.
1. Use `enumerate()` instead of manually tracking a counter.
1. Use `zip()` to iterate through related sequences together.
1. Use `while` only when a condition controls when repetition ends.

## References

1. [Python Data Structures](https://docs.python.org/3/tutorial/datastructures.html)
1. [Built-in Types](https://docs.python.org/3/library/stdtypes.html)
1. [The `for` Statement](https://docs.python.org/3/reference/compound_stmts.html#the-for-statement)
