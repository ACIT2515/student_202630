# Scopes, Closures, and Decorators Exploration Activity

## Overview
In this activity, you will step through `scopes_w_decorators.py` using a debugger to understand Python variable scopes (LEGB), closures, and decorators.

## Instructions
1. Open `scopes_w_decorators.py` in your debugger
2. Set breakpoints at key locations as you work through the questions
3. Step through the code execution to find answers
4. Answer all questions based on what you observe

---

## Questions

### Question 1: Decorator Application
How many times does the `log_globals()` function get called when the module is first imported/executed? Where in the code does this happen?

### Question 2: Decorator Syntax Alternative
The code uses `@log_globals` decorator syntax. How would you apply the logging wrapper to `modify_global()` WITHOUT using the `@` decorator syntax? Write the equivalent code.

### Question 3: LEGB Resolution
In the `log_tracked_vars()` function, when the code accesses the `tracked_vars` variable, which scope level (L, E, G, or B) is Python using according to LEGB resolution? Explain why.

### Question 4: Closure Variable Capture
Each decorated function has its own `call_count`. Set a breakpoint in `logging_wrapper()` and observe the value of `call_count` across multiple function calls. After running `modify_global("call_1")` and then `modify_global("call_2")`, what is the value of `call_count` for the `modify_global` wrapper?

### Question 5: Global vs Local Scope
In `modify_local()`, variables named `outside_global` and `exported_global` are assigned values. Are these the same variables as the global ones, or are they different? Step through with the debugger and check the global namespace to confirm your answer.

### Question 6: Closure Persistence
After `log_globals()` returns the `logging_wrapper` function, does the `tracked_vars` list still exist? Use the debugger to inspect the closure variables of `logging_wrapper`. What mechanism allows this?

### Question 7: Built-in Scope
In `log_tracked_vars()`, the code calls `globals()`. Which scope level (L, E, G, or B) does `globals` come from in the LEGB resolution order?

### Question 8: Nonlocal Keyword
Why does `logging_wrapper()` use `nonlocal call_count` instead of just `call_count += 1`? What would happen if you removed the `nonlocal` keyword?

### Question 9: Reading vs Writing Globals
In `use_global()`, the function reads `module_global` and `exported_global` without using the `global` keyword. In `modify_global()`, the function must use the `global` keyword. Explain why reading doesn't require `global` but writing does.

### Question 10: Decorator Call Count Independence
After running all the function calls in `__main__`, what is the total call count for `modify_global`, `modify_local`, and `use_global` respectively? Are they sharing the same counter or do they each have independent counters? Verify this with the debugger.

---

## Debugging Tips
- Use "Step Into" to enter function calls
- Use "Step Over" to execute a line without entering functions
- Watch the Variables panel to see local, global, and closure variables
- Use the Call Stack panel to see the enclosing scopes
