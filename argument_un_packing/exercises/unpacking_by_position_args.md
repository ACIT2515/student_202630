# `args`, `kwargs`, Unpack Exercise

Create a function that accepts any number of numbers and any keyword arguments,
then:

1. Sum all the numbers from `*args`
2. Multiply the sum by a `multiplier` from `**kwargs` (default to 1)
3. Add a `bonus` from `**kwargs` (default to 0)

```python
def calculate(*args, **kwargs):
    # Your code here
    pass

# Test cases:
print(calculate(1, 2, 3))                    # Should return 6
print(calculate(1, 2, 3, multiplier=2))      # Should return 12
print(calculate(1, 2, 3, bonus=10))          # Should return 16
print(calculate(1, 2, 3, multiplier=2, bonus=5))  # Should return 17
```

<details><summary>

## Solution</summary>

```python
def calculate(*args, **kwargs):
    """Sum numbers with optional multiplier and bonus"""
    # Sum all positional arguments
    total = sum(args)

    # Get optional parameters with defaults
    multiplier = kwargs.get("multiplier", 1)
    bonus = kwargs.get("bonus", 0)

    # Apply operations
    result = total * multiplier + bonus
    return result

# Test
print(calculate(1, 2, 3))                    # 6
print(calculate(1, 2, 3, multiplier=2))      # 12
print(calculate(1, 2, 3, bonus=10))          # 16
print(calculate(1, 2, 3, multiplier=2, bonus=5))  # 17
```

</details>

