# Directed Reading Questions: Recursion and Call Stacks

## Question 1: Base Cases and Recursive Cases

In `countdown_recursive`, identify the base case and the recursive case.
Then explain, in your own words, what would happen if the base case were
removed from the function.

## Question 2: Frame Execution and the Call Stack

When `countdown_recursive(3)` runs, several stack frames exist at once before
any of them return. How many frames are on the stack at the deepest point,
and what does each frame's `count` value hold at that moment?

## Question 3: Choosing Recursion vs Iteration

`sum_nested_recursive` and `sum_nested_iterative` in
[02_nested_list_sum_demo.py](../demo/intro/02_nested_list_sum_demo.py) both
sum a nested list. What kind of problem structure makes the recursive
version a natural fit, and what does the iterative version have to manage
manually to achieve the same result?
