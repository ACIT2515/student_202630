#!/usr/bin/env python3
"""
Demonstrates python variable scoping and the use of closures and decorators.

SCOPE:

After walking through this script in the debugger you should be able to
understand the following Python Variable Scopes and the LEGB Resolution Rule:

    1. Local (L): Variables defined within a function
    2. Enclosing (E): Variables in the enclosing function (for nested functions)
    3. Global (G): Variables defined at module level
    4. Built-in (B): Python's built-in namespace (e.g., len, print, etc.)

CLOSURES:

A closure is created when a nested function references variables from its
enclosing scope. The nested function "closes over" these variables, preserving
them even after the outer function has finished executing. The creation and use
of closures is noted in the comments.

This script utilizes the inspect library to access the calling function and
the name of functions that are passed as variables
"""

import inspect  # Built-in scope: 'inspect' module from Python standard library
import logging  # Built-in scope: 'logging' module from Python standard library

# Global scope: These variables are accessible throughout the module
logging.basicConfig(
    level=logging.DEBUG,
    format="{funcName:<20} : {message}",
    style="{",
)  # Use new style string formatter

log = logging.getLogger(__name__).debug  # Global scope: log function


def print_variables():
    """
    Prints all local variables from calling function.

    Uses inspect to access the calling stack frame

    Returns:
        None

    """
    # Local scope: These variables only exist within print_variables()
    stack_frame = inspect.currentframe()  # Local variable
    calling_func = stack_frame.f_back  # Local variable
    log(f"{calling_func.f_code.co_name} Local Variables: {calling_func.f_locals}")


def log_globals(func):
    """
    This is the decorating function to log all register global variables before
    and after every function call.

    This function creates CLOSURES by returning nested functions that capture
    variables from the enclosing scope (func, tracked_vars, call_count).

    IMPORTANT: Each time @log_globals decorates a function, a NEW closure is created
    with its OWN independent call_count. This means:
    - modify_global has call_count starting at 0
    - modify_local has call_count starting at 0
    - use_global has call_count starting at 0

    They do NOT share the same counter!

    Args:
        func: function to be decorated (Enclosing scope for wrapper)

    Returns:
        wrapped function
        (a CLOSURE that captures 'func', 'tracked_vars', and 'call_count')
    """
    # Enclosing scope: These variables are accessible to nested functions:
    # wrapper, log_tracked_vars
    #
    # These will be CAPTURED by the closures created below
    tracked_vars = [
        "exported_global",
        "module_global",
    ]  # Enclosing variable - captured in closure
    call_count = 0  # counter for THIS specific decorated function

    def log_tracked_vars():
        """
        Utility function to print the global variables to be tracked

        CLOSURE: This function captures 'tracked_vars' from the enclosing scope.
        Even after log_globals() finishes, this function retains access to tracked_vars.

        Returns:
            None

        """
        # Local scope: Variables defined here only exist within log_tracked_vars()
        global_vars = (
            globals()
        )  # Local variable - result of built-in globals() function

        # Enclosing scope: tracked_vars is from the outer log_globals() function
        # This is CLOSURE in action - accessing variable from enclosing scope
        for var in tracked_vars:  # 'var' is local to this loop
            if var in global_vars:
                log(f"{var:20} = {global_vars[var]}")

    def logging_wrapper(*args, **kwargs):
        """
        The wrapper decorator function.

        CLOSURE: This function captures 'func', 'call_count', and 'log_tracked_vars'
        from the enclosing log_globals() scope. These variables remain accessible
        even after log_globals() has returned.

        Each decorated function has its OWN wrapper with its OWN call_count closure
        variable.

        It logs the value of the tracker variables before and after the
        execution of the decorated function.

        Args:
            *args: Positional arguments to pass to the decorated function
            **kwargs: Keyword arguments to pass to the decorated function

        Returns:
            Any results of the decorated function

        """
        nonlocal call_count
        # Increments THIS function's counter,
        # only persists across calls to a specific function
        call_count += 1

        log(f"=== {func.__name__} Logging Decorator Call #{call_count} ===")
        log_tracked_vars()  # Call nested function from enclosing scope (also a closure)
        log(
            f"Start {func.__name__}()"
        )  # 'func' is from enclosing scope (captured in closure)
        result = func(*args, **kwargs)  # Pass arguments to the decorated function
        log(f"End {func.__name__}()")
        log_tracked_vars()
        log(f"=== Total calls to {func.__name__}: {call_count} ===\n\n")
        return result  # Return local variable

    # CLOSURE CREATION: wrapper is returned with captured references to:
    #   - func (the decorated function)
    #   - call_count (maintains state across calls)
    #   - tracked_vars (configuration data)
    #   - log_tracked_vars (nested function, itself a closure)
    return logging_wrapper  # Return nested function (CLOSURE)


@log_globals
def modify_global(suffix):
    """
    Demonstrates modification and creation of global variables in a function
    through use of the global keyword.

    It assigns values to global variables (with suffix appended) and prints all local variables

    Args:
        suffix: String to append to the variable assignment
    """
    # Global scope access: Declare intent to modify global variables
    global module_global  # References global scope variable
    global exported_global  # References global scope variable (will be created)

    # These assignments modify global scope, not local scope
    module_global = f"assigned in modify_global {suffix}"
    exported_global = f"assigned in modify_global {suffix}"

    print_variables()  # Global scope: function defined at module level


@log_globals
def modify_local(suffix):
    """
    Demonstrates modification and creation of local variables in a function
    in the absence of the global keyword.

    It assigns values to local variables (with suffix appended) and prints them

    Args:
        suffix: String to append to the variable assignment
    """
    # Local scope: Without 'global' keyword, these create NEW local variables
    # that shadow any global variables with the same name

    # the global variables can't be accessed before being assigned as python
    # assumes you want to define it locally because its name exists inside the
    # function

    outside_global = (
        f"assigned in modify_local {suffix}"  # Local variable (shadows global)
    )
    exported_global = (
        f"assigned in modify_local {suffix}"  # Local variable (shadows global)
    )
    print_variables()  # Global scope function


@log_globals
def use_global():
    """
    Demonstrates the access of global variables in a function
    in the absence of the global keyword.

    It assigns the global variables values to local variables and prints them
    """
    # Local scope: temp1 and temp2 are local variables
    # Global scope: outside_global and inside_global are read from global scope
    # Reading global variables doesn't require 'global' keyword, only writing does

    # global variables be accessed immediately since they are never redefined
    if module_global in globals():
        temp1 = module_global  # Local var = Global var (read-only access)

    if module_global in globals():
        temp2 = exported_global  # Local var = Global var (read-only access)

    print_variables()  # global scope function


if __name__ == "__main__":
    # Print logging header
    print("=" * 80)
    print(f"{'Function':<20} : {'Message'}")
    print("=" * 80)

    # Global scope: This variable is created at module level
    # It's accessible to all functions in this module (unless shadowed by local vars)
    module_global = "assigned in global scope"

    use_global()  # Will read from global variables
    # Global scope: These are function calls using globally-defined functions
    modify_global(
        "call_1"
    )  # Will modify global 'outside_global' and create global 'inside_global'
    modify_global("call_2")  # Will modify global variables with different suffix
    modify_local("call_1")  # Will create local variables that shadow globals
    modify_local("call_2")  # Will create local variables with different suffix
    use_global()  # Will read from global variables
