# Scopes, Closures, and Decorators Exploration Activity - SOLUTION

---

## Question 1: Decorator Application
**How many times does the `log_globals()` function get called when the module is first imported/executed? Where in the code does this happen?**

**Answer:** 
`log_globals()` is called **3 times** when the module is first imported - once for each decorated function. This happens at:
- Line 113: `@log_globals` decorating `modify_global()`
- Line 132: `@log_globals` decorating `modify_local()`
- Line 151: `@log_globals` decorating `use_global()`

The decorator is applied at function definition time, not when the functions are called.

---

## Question 2: Decorator Syntax Alternative
**The code uses `@log_globals` decorator syntax. How would you apply the logging wrapper to `modify_global()` WITHOUT using the `@` decorator syntax? Write the equivalent code.**

**Answer:**
```python
def modify_global(suffix):
    global module_global
    global exported_global
    module_global = f"assigned in modify_global {suffix}"
    exported_global = f"assigned in modify_global {suffix}"
    print_variables()

# Apply the decorator manually
modify_global = log_globals(modify_global)
```

The `@log_globals` syntax is syntactic sugar that is equivalent to reassigning the function to the result of passing it through the decorator.

---

## Question 3: LEGB Resolution
**In the `log_tracked_vars()` function, when the code accesses the `tracked_vars` variable, which scope level (L, E, G, or B) is Python using according to LEGB resolution? Explain why.**

**Answer:**
Python is using the **E (Enclosing)** scope. 

`tracked_vars` is not defined locally in `log_tracked_vars()` (L), so Python looks in the enclosing scope. `tracked_vars` is defined in the enclosing function `log_globals()`, so it's found at the Enclosing level. Python doesn't need to look further to Global (G) or Built-in (B) scopes.

---

## Question 4: Closure Variable Capture
**Each decorated function has its own `call_count`. Set a breakpoint in `logging_wrapper()` and observe the value of `call_count` across multiple function calls. After running `modify_global("call_1")` and then `modify_global("call_2")`, what is the value of `call_count` for the `modify_global` wrapper?**

**Answer:**
The value of `call_count` is **2**.

Each call to `modify_global()` increments its own `call_count`:
- First call: `call_count` becomes 1
- Second call: `call_count` becomes 2

The closure preserves the state of `call_count` between calls to the same decorated function.

---

## Question 5: Global vs Local Scope
**In `modify_local()`, variables named `outside_global` and `exported_global` are assigned values. Are these the same variables as the global ones, or are they different? Step through with the debugger and check the global namespace to confirm your answer.**

**Answer:**
They are **different variables**. The variables in `modify_local()` are **local** variables that shadow the global ones.

Because `modify_local()` does NOT use the `global` keyword, the assignments create new local variables instead of modifying the global variables. You can verify this in the debugger by checking `globals()` before and after calling `modify_local()` - the global variables remain unchanged.

---

## Question 6: Closure Persistence
**After `log_globals()` returns the `logging_wrapper` function, does the `tracked_vars` list still exist? Use the debugger to inspect the closure variables of `logging_wrapper`. What mechanism allows this?**

**Answer:**
Yes, `tracked_vars` still exists. 

The mechanism is **closure**. When `logging_wrapper` is returned, it maintains references to variables from its enclosing scope (`tracked_vars`, `call_count`, `func`). Python keeps these variables alive in memory as part of the closure, even after `log_globals()` has finished executing. You can inspect these using `function.__closure__` or by viewing closure variables in the debugger.

---

## Question 7: Built-in Scope
**In `log_tracked_vars()`, the code calls `globals()`. Which scope level (L, E, G, or B) does `globals` come from in the LEGB resolution order?**

**Answer:**
The **B (Built-in)** scope.

`globals` is a built-in Python function, part of Python's built-in namespace. It's not defined locally (L), in an enclosing function (E), or at the global/module level (G), so Python finds it in the Built-in scope.

---

## Question 8: Nonlocal Keyword
**Why does `logging_wrapper()` use `nonlocal call_count` instead of just `call_count += 1`? What would happen if you removed the `nonlocal` keyword?**

**Answer:**
The `nonlocal` keyword is required because `call_count += 1` is an assignment operation, not just a read.

Without `nonlocal`, Python would assume you're trying to create a **new local variable** named `call_count` in `logging_wrapper()`. This would cause an `UnboundLocalError` because Python would try to read `call_count` (for the `+= 1` part) before it's been assigned locally.

The `nonlocal` keyword tells Python to use the `call_count` from the enclosing scope instead of creating a new local variable.

---

## Question 9: Reading vs Writing Globals
**In `use_global()`, the function reads `module_global` and `exported_global` without using the `global` keyword. In `modify_global()`, the function must use the `global` keyword. Explain why reading doesn't require `global` but writing does.**

**Answer:**
Python allows **reading** global variables without the `global` keyword because there's no ambiguity - Python follows LEGB and finds the variable in the global scope.

However, **writing** (assignment) to a variable creates a new local variable by default. To tell Python you want to modify the global variable instead of creating a local one, you must explicitly declare `global variable_name`.

This design prevents accidental modification of global variables.

---

## Question 10: Decorator Call Count Independence
**After running all the function calls in `__main__`, what is the total call count for `modify_global`, `modify_local`, and `use_global` respectively? Are they sharing the same counter or do they each have independent counters? Verify this with the debugger.**

**Answer:**
The call counts are:
- `modify_global`: 2 (called twice with "call_1" and "call_2")
- `modify_local`: 2 (called twice with "call_1" and "call_2")
- `use_global`: 2 (called once before modify_global, once after modify_local)

They have **independent counters**. Each time `@log_globals` decorates a function, it creates a **new closure** with its own `call_count` variable. The three decorated functions do NOT share the same counter - each maintains its own separate state.

This can be verified by setting breakpoints in `logging_wrapper()` and inspecting the `call_count` closure variable for each function call.
