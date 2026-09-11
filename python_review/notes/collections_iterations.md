# Python Collections and Iteration

Collections store multiple values in one variable. They are useful when a
program needs to work with services, users, ports, log entries, or other groups
of related values.

This reference covers lists, dictionaries, tuples, sets, and `for` loops.

## Choosing a Collection

| Collection | Use it when you need | Ordered | Mutable |
| --- | --- | --- | --- |
| `list` | A sequence that can change | Yes | Yes |
| `dict` | Values identified by meaningful keys | Yes | Yes |
| `tuple` | A fixed sequence that should not change | Yes | No |
| `set` | Unique values with no duplicates | No | Yes |

## Lists

A list is an ordered, changeable collection. List positions start at `0`.

```python
services = ["Spooler", "W32Time", "WinRM"]

print(services[0])
services.append("Dhcp")
services[1] = "TimeBrokerSvc"
print(services)
```

Common list operations:

- `items.append(value)`: add one value to the end
- `items.remove(value)`: remove a value
- `items.pop()`: remove and return the last value
- `len(items)`: count the values
- `value in items`: check whether a value exists

## Dictionaries

A dictionary maps unique keys to values. Use a dictionary when a value needs a
name, such as a hostname, port, or service status.

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

Common dictionary operations:

- `mapping[key]`: get the value for a key
- `mapping[key] = value`: add or replace a key-value pair
- `mapping.get(key, default)`: get a value or a fallback value
- `mapping.keys()`: view the keys
- `mapping.values()`: view the values
- `mapping.items()`: view key-value pairs

## Tuples

A tuple is an ordered collection that cannot change after creation. Use a tuple
for related values that should stay together and remain unchanged.

```python
server_location = ("server01", "Vancouver", "rack-3")

print(server_location[0])
# server_location[0] = "server02"  # TypeError: tuples cannot be changed
```

A tuple with one item needs a trailing comma: `port = (443,)`.

## Sets

A set stores unique values. Adding the same value more than once does not create
a duplicate. Sets do not use indexes, so `ports[0]` is not valid.

```python
open_ports = {80, 443, 443}
open_ports.add(22)

print(open_ports)  # Contains 80, 443, and 22 once each
print(443 in open_ports)
```

Use sets when uniqueness matters, such as recording the distinct ports found
while inspecting a host.

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

### Counting with `range()`

`range()` produces a sequence of numbers, which is useful when you need a fixed
number of attempts.

```python
for attempt in range(1, 4):
    print(f"Connection attempt {attempt}")
```

This code runs three times with `attempt` equal to `1`, `2`, and `3`.

## Iteration with `while`

A `while` loop repeats while a condition is `True`. Use it when the number of
repetitions is not known in advance, such as retrying a network connection.

```python
attempt = 1
is_connected = False

while not is_connected and attempt <= 3:
    print(f"Connection attempt {attempt}")
    attempt += 1
```

The condition is checked before each loop iteration. Ensure the code inside the
loop changes a value used in the condition; otherwise, the loop may never stop.

Use `break` to leave a loop as soon as the required result is found:

```python
attempt = 1

while attempt <= 3:
    if attempt == 2:
        print("Connection succeeded")
        break
    attempt += 1
```

## Collection and Iteration Guidelines

1. Use a list when order matters and the collection may change.
1. Use a dictionary when each value needs a meaningful key.
1. Use a tuple when related values should not change.
1. Use a set when duplicate values must be ignored.
1. Iterate directly over values with `for value in collection` rather than
   manually using indexes when the index is not needed.
1. Use a `while` loop when repetition should continue until a condition changes.

## References

1. [Python Data Structures](https://docs.python.org/3/tutorial/datastructures.html)
1. [Built-in Types](https://docs.python.org/3/library/stdtypes.html)
1. [The `for` Statement](https://docs.python.org/3/reference/compound_stmts.html#the-for-statement)
