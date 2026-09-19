# Recursion and Call Stacks

## What Is Recursion?

Recursion is a technique where a function solves a problem by calling itself
on a smaller or simpler version of the same problem. Each call works on less
of the problem than the call before it, until the problem is small enough to
answer directly.

Every recursive function needs two parts:

- A **base case**: a condition that answers the problem directly, without
  making another recursive call. This is what stops the recursion.
- A **recursive case**: the part that does some work, then calls the function
  again with an input that is closer to the base case.

If a function is missing a base case, or the recursive case never moves
closer to it, the function calls itself forever (until Python stops it with
an error).

## Base Cases and Recursive Cases: a Worked Example

[01_recursion_demo.py](../demo/intro/01_recursion_demo.py) counts down from a
number to zero:

```python
def countdown_recursive(count):
    if count <= 0:  # Base case
        print("Liftoff!")
        return
    print(f"  {count}...")
    countdown_recursive(count - 1)  # Recursive case
```

- The base case is `count <= 0`. Once reached, the function prints `"Liftoff!"`
  and returns, without calling itself again.
- The recursive case prints the current count, then calls
  `countdown_recursive` again with `count - 1`. Each call moves one step
  closer to the base case.

## Frame Execution and the Call Stack

Every function call, recursive or not, gets its own **stack frame**: a
region of memory holding that call's parameters, local variables, and the
point it should resume at when the call it made returns. The call stack is a
last-in-first-out (LIFO) structure: the most recent call is always the next
one to finish.

For a recursive function, calling itself pushes a new frame on top of the
stack. That new frame has its own copy of the parameters and local variables,
completely separate from the frame that called it. The paused (calling) frame
does no further work until the frame it started returns.

Tracing `countdown_recursive(3)`:

1. `countdown_recursive(3)` is called. Frame 1 (`count=3`) prints `3...` and
   calls `countdown_recursive(2)`. Frame 1 pauses.
2. `countdown_recursive(2)` is called. Frame 2 (`count=2`) prints `2...` and
   calls `countdown_recursive(1)`. Frame 2 pauses.
3. `countdown_recursive(1)` is called. Frame 3 (`count=1`) prints `1...` and
   calls `countdown_recursive(0)`. Frame 3 pauses.
4. `countdown_recursive(0)` is called. Frame 4 (`count=0`) hits the base case:
   it prints `"Liftoff!"` and returns immediately. No new frame is created.
5. Frame 4 finishes and is removed from the stack. Frame 3 resumes; it has
   nothing left to do, so it also returns and is removed.
6. Frame 2 resumes, then returns and is removed.
7. Frame 1 resumes, then returns and is removed. The stack is now empty.

At the deepest point, four frames existed on the stack at once (for
`count=3`, `2`, `1`, and `0`), even though only one function was ever
defined. This is true of every recursive call: the stack briefly holds one
frame per level of recursion still in progress.

[02_nested_list_sum_demo.py](../demo/intro/02_nested_list_sum_demo.py) shows
frame execution combining results, not just printing them:

```python
def sum_nested_recursive(data):
    if isinstance(data, (int, float)):  # Base case
        return data

    total = 0
    for item in data:
        total += sum_nested_recursive(item)  # Recursive case
    return total
```

Here, each frame's `total` depends on values returned by the frames it
started. A frame cannot finish computing its own `total` until every
recursive call it made has returned. This is different from
`countdown_recursive`, where each frame's work was already done before it
made its recursive call.

### Recursion Depth Limits

Python limits how many frames can be on the call stack at once (by default,
roughly 1000). A recursive function whose base case is never reached, or
whose input is too deep, raises a `RecursionError`. This is a practical
consequence of frame execution: each pending call is real memory that has to
be tracked somewhere.

## What Kinds of Problems Are Best Solved Recursively?

Recursion fits problems whose structure is **self-similar**: solving the
whole problem means solving one or more smaller versions of the same
problem. Good candidates include:

- **Hierarchical or nested data of unknown depth**: directory trees, nested
  lists, nested JSON/configuration documents. You don't know in advance how
  many levels deep the structure goes.
- **Divide-and-conquer algorithms**: binary search, merge sort. The problem
  is split into smaller sub-problems of the same shape, solved the same way.
- **Definitions that are naturally recursive**: mathematical definitions
  like factorial or Fibonacci are defined in terms of themselves.
- **Traversal where the branching factor is unknown**: exploring every
  sub-directory of a directory, every reply in a comment thread, or every
  hop of a network path.

Recursion is usually a poor fit for simple, fixed-length repetition over a
sequence you can already measure (`for i in range(10)`); a loop expresses
that more directly and without the overhead of extra function calls.

## Why Use Recursion?

- **It mirrors the problem's structure.** A recursive definition of "sum a
  nested list" (the sum of a number is itself; the sum of a list is the sum
  of its items) can be translated almost directly into code.
- **It handles unknown depth without manual bookkeeping.** A recursive
  directory walk does not need to know how deep the folder tree goes; each
  call only has to handle one level and hand off deeper levels to itself.
- **It supports "trusting the recursion."** When writing the recursive case,
  you can assume the recursive call already correctly solves the smaller
  sub-problem, and focus only on how to combine that result at the current
  level.

## Tradeoffs

| Recursion                                              | Iteration                                                |
| ------------------------------------------------------- | --------------------------------------------------------- |
| Often shorter and closer to the problem's definition     | Often more code, but the flow of control is explicit       |
| Uses one stack frame per call; deep recursion can raise `RecursionError` | Uses a fixed amount of memory regardless of how many iterations run |
| Function-call overhead on every step                    | No extra function-call overhead for repetition             |
| State is implicit, held across many paused stack frames  | State is explicit, held in local variables you can inspect directly |
| Naturally fits unknown or variable depth                 | Requires an explicit stack or queue to fit unknown depth (see `sum_nested_iterative` in [02_nested_list_sum_demo.py](../demo/intro/02_nested_list_sum_demo.py)) |

Any recursive function can be rewritten iteratively, usually by managing an
explicit stack (as `sum_nested_iterative` does), but that often makes the
code longer and less obviously connected to the problem's definition. Choose
recursion when its clarity is worth the call-stack overhead and depth limit;
choose iteration when the repetition is simple, the depth could be large, or
memory and performance are a concern.

## Common Use Cases

- **Filesystem traversal**: walking a directory tree of unknown depth with
  `pathlib.Path`, including handling symbolic links and permission errors.
- **Network diagnostics**: a `traceroute`-style tool that expands one hop at
  a time until the destination responds or a hop limit is reached.
- **Parsing and flattening nested data**: converting a nested task list,
  JSON document, or configuration structure into a flat list or table.
- **Divide-and-conquer algorithms**: binary search over sorted data (such as
  sorted log entries), merge sort.
- **Recursive descent parsing**: reading nested expressions or structured
  text where each nested element is parsed the same way as the whole.

## References

1. [01_recursion_demo.py](../demo/intro/01_recursion_demo.py)
2. [02_nested_list_sum_demo.py](../demo/intro/02_nested_list_sum_demo.py)
3. [Python Design and History FAQ: Recursion limit](https://docs.python.org/3/faq/design.html)
4. [`sys.setrecursionlimit`](https://docs.python.org/3/library/sys.html#sys.setrecursionlimit)
