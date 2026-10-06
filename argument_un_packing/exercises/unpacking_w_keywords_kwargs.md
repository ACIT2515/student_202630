# `**kwargs` Exercise

Create a function that builds a user profile dictionary from keyword arguments.

Requirements:
1. Accept any number of keyword arguments using `**kwargs`
2. Required fields: `name` and `email` - raise `ValueError` if missing
3. Optional fields with defaults:
   - `role` (default: "user")
   - `active` (default: True)
4. Store any additional fields passed in `**kwargs`
5. Return a dictionary with all the profile information

```python
def create_user_profile(**kwargs):
    # Your code here
    pass

# Test cases:
print(create_user_profile(name="Alice", email="alice@example.com"))
# Should return: {'name': 'Alice', 'email': 'alice@example.com', 'role': 'user', 'active': True}

print(create_user_profile(name="Bob", email="bob@example.com", role="admin"))
# Should return: {'name': 'Bob', 'email': 'bob@example.com', 'role': 'admin', 'active': True}

print(create_user_profile(name="Charlie", email="charlie@example.com", age=30, city="Vancouver"))
# Should return: {'name': 'Charlie', 'email': 'charlie@example.com', 'role': 'user', 'active': True, 'age': 30, 'city': 'Vancouver'}

# This should raise ValueError:
# create_user_profile(name="Dave")  # Missing email
```

<details><summary>

## Solution</summary>

```python
def create_user_profile(**kwargs):
    """Create a user profile from keyword arguments"""
    # Check for required fields
    if "name" not in kwargs:
        raise ValueError("Missing required field: name")
    if "email" not in kwargs:
        raise ValueError("Missing required field: email")
    
    # Create profile with required fields
    profile = {
        "name": kwargs["name"],
        "email": kwargs["email"],
    }
    
    # Add optional fields with defaults
    profile["role"] = kwargs.get("role", "user")
    profile["active"] = kwargs.get("active", True)
    
    # Add any additional fields
    for key, value in kwargs.items():
        if key not in ["name", "email", "role", "active"]:
            profile[key] = value
    
    return profile

# Test
print(create_user_profile(name="Alice", email="alice@example.com"))
# {'name': 'Alice', 'email': 'alice@example.com', 'role': 'user', 'active': True}

print(create_user_profile(name="Bob", email="bob@example.com", role="admin"))
# {'name': 'Bob', 'email': 'bob@example.com', 'role': 'admin', 'active': True}

print(create_user_profile(name="Charlie", email="charlie@example.com", age=30, city="Vancouver"))
# {'name': 'Charlie', 'email': 'charlie@example.com', 'role': 'user', 'active': True, 'age': 30, 'city': 'Vancouver'}

try:
    create_user_profile(name="Dave")  # Missing email
except ValueError as e:
    print(f"Error: {e}")  # Error: Missing required field: email
```

</details>
