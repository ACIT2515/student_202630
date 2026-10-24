# Mid-Term Exam

## Test Format

The exam is 2 hours long.

This is a written exam to be completed on paper. Code samples and solutions will
be short. You will write and trace code by hand using Python 3.14 or 3.15.

You will be provided with a reference sheet.

## Exam Topics

### Flow Control

- Translate a written requirement into Boolean conditions, loops, and state
  updates.
- Choose and order conditions so the code handles the specified cases.

References: [Variables, control flow, and functions](../../../subjects/python_review/notes/variables_control_flow_functions.md)

### Program and Project Structure

- Add an entry-point guard so a module can be run as a program or imported
  without running its main program.
- Organize a solution so processing logic is separate from file access,
  command-line interaction, and printing.

References: [Modules, packages, and imports](../../../subjects/modules_packages/notes/modules_packages_imports.md)

### Command-Line Arguments

- Use `sys.argv` to access arguments supplied when a program is run from the
  command line.
- Distinguish the program name from the arguments, check that the required
  arguments were provided, and convert argument strings to the types needed by
  the program.
- Use command-line arguments to control a program's inputs or behaviour.

References: [Python program arguments and `sys.argv`](../../../subjects/cmdline_arguments/notes/python_cmdline_args_argparse.md)

### Functions

- Trace function and method calls in execution order and determine the value
  returned.
- Write or complete a function or method using its given parameters, including
  positional or keyword arguments.

References: [Variables, control flow, and functions](../../../subjects/python_review/notes/variables_control_flow_functions.md)

### Higher-Order Functions and Decorators

- Trace code that passes a function as an argument or returns a function as a
  result.
- Follow a decorator and wrapper to determine the order in which the wrapped
  and wrapper code executes.
- Trace how `*args` and `**kwargs` collect and forward positional and keyword
  arguments.

References: [Higher-order functions and decorators](../../../subjects/decorators_higher_order_function/notes/higher_order_functions_decorators.md); [Argument unpacking](../../../subjects/argument_un_packing/notes/argument_unpacking_args_kwargs.md)

#### Note

These topics may appear in supplied code. You will be expected to explain or
trace its behaviour, not write a complete program using these techniques.

### Collections, Iteration, and Data Processing

- Process lists and dictionaries to select, transform, or summarize records
  without changing the input when that is not required.
- Write or trace a loop that tracks the current item separately from results
  accumulated across the whole sequence.
- Initialize, update, or reset variables at the appropriate point in an
  iteration.
- Select records using conditions from a requirement and combine information
  from multiple input records into a result.
- Check whether a key is in a dictionary and use that result to update its
  value.
- Handle empty collections and other boundary cases.

References: [Collections and iteration](../../../subjects/python_review/notes/collections_iterations.md)

### Files, Structured Data, and Exceptions

- Read data from a file using a context manager and process it after the file
  has been opened.
- Read CSV rows as dictionaries and convert numeric text to the required type.
- Select relevant records from file data and return or report the required
  result.
- Identify and handle common file I/O errors in a supplied scenario.

References: [Reading and writing files](../../../subjects/file_io/notes/file_io.md); [JSON and CSV files](../../../subjects/file_io/notes/json_csv_reading_writing.md); [Collections and iteration](../../../subjects/python_review/notes/collections_iterations.md); [Exceptions](../../../subjects/exceptions/notes/exceptions.md)

### Classes, Objects, and Object-Oriented Design

- Initialize instance attributes using `__init__` and `self`.
- Write or complete methods that inspect or change an object's state, checking
  whether an operation is allowed before changing that state.
- Trace how creating an object, changing an attribute, or assigning another
  reference affects the objects involved.
- Determine when objects have independent or shared mutable state, and use
  object identity to distinguish objects from references.
- Predict what is displayed when an object is printed, including the effect of
  `__str__`.
- Choose public, protected, or private naming conventions for attributes and
  methods in a described design.
- Use encapsulation to ensure that methods maintain valid object state.
- Identify an appropriate general class and specialized class, and use
  inheritance to share behaviour where appropriate.

References: [Object-oriented programming](../../../subjects/object_oriented/notes/oop_python_intro.md); [Inheritance and abstract base classes](../../../subjects/object_oriented/notes/oo_inheritence_abc.md)

### Recursion

- Trace recursive calls using the base case, call frames, and progress toward
  termination.
- Determine how return values move back through the recursive calls.

References: [Recursion and call stacks](../../../subjects/recursion/notes/recursion_call_stacks.md)

#### Note

Recursion may appear in supplied code. You will be expected to explain or trace
its behaviour, not write a complete recursive program.

### Testing

- Write pytest tests for specified behaviour, including boundary cases and
  expected outcomes.
- Given a test and an operation, determine what result and object state should
  be checked.
- Use test results or supplied code to identify behaviour that is incorrect or
  not yet tested.

References: [Pytest](../../../subjects/testing_pytest/notes/pytest.md)

### Project Management with `uv`

- Explain how `uv` is used to manage a project's environment and dependencies.
- Choose or describe a project environment that isolates dependencies from
  other projects.
- Compare the benefits and practical costs of using separate environments.

References: [Virtual environments and dependencies](../../../subjects/uv_dependencies_virtual_environments/notes/virtual_environments_dependencies.md)

## Question Types

### Writing Short Programs (40%)

Write a short function or method body that meets a stated requirement. A
programming question may involve basic classes and objects.

### Code Reading, Tracing, and Error Identification (25%)

Trace supplied code to predict its output and follow changes to values and
object state. Identify and correct a logic error.

### Code Completion (15%)

Complete a supplied program by filling in missing expressions or statements.
Questions focus on selecting the correct logic rather than recalling syntax.

### Programming Decisions and Logic Choices (20%)

Compare approaches, justify a design choice, or describe how to test or
investigate behaviour. Answer each written subpart using concise bullet points
or at most two sentences.
