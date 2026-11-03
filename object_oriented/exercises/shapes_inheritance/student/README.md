# Introduction to OOP Inheritance Exercise

## Overview

In this exercise, you'll build a **Shape Drawing System** to practice
**object-oriented inheritance**. 

You will implement:

- A **base class** (`Shape`) that stores a color and a center point and
  defines a shared interface
- Two **subclasses** (`Circle`, `Rectangle`) that inherit
  from `Shape`

A **container class** (`Canvas`) is provided. It holds a collection of shapes
and draws them in a window using Python's built-in `turtle` module.

**Concepts practiced:**

- Defining a subclass: `class Circle(Shape):`
- Calling the parent constructor: `super().__init__(color, center)`
- Overriding methods: `area()`, `perimeter()`, and `draw()`
- Polymorphism — calling the same method on different object types
- `isinstance()` checks
- Properties for accessing object attributes
- Class attributes (read the provided `Canvas.WIDTH` and `Canvas.HEIGHT`)

**Files Provided:**

- `test_shapes.py` — A comprehensive pytest test suite (do not modify)
- `shapes_starter.py` — Starter template with `Canvas` and `main()` provided

**Files You'll Create:**

- `shapes.py` — Your implementation of the three shape classes, made by completing shapes starter.

---

## Background: What Is Inheritance?

Inheritance lets one class **reuse and extend** the behavior of another:

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        raise NotImplementedError("Subclasses must implement speak()")


class Dog(Animal):           # Dog inherits from Animal
    def __init__(self, name, breed):
        super().__init__(name)   # Call Animal's __init__ first
        self.breed = breed

    def speak(self):             # Override Animal's speak()
        return "Woof!"


class Cat(Animal):
    def speak(self):
        return "Meow!"


# Polymorphism: same code, different behavior
animals = [Dog("Rex", "Labrador"), Cat("Whiskers")]
for animal in animals:
    print(animal.speak())   # Calls Dog.speak() or Cat.speak() automatically
```

**Key rules:**

| Concept | Syntax | When to use |
|---|---|---|
| Inherit from a class | `class Sub(Parent):` | When Sub IS-A Parent |
| Call parent constructor | `super().__init__(...)` | Always in `__init__` |
| Override a method | Redefine `def method(self):` in the subclass | When behavior differs |

---

## Scenario

You are building a simple shape drawing system. There are two types of
shapes — circles and rectangles. Both shapes share certain
properties (a color and a center point) and behaviors (they have an area and a
perimeter, and they can draw themselves), but each shape does these things
differently.

**Your Goal:** Implement the three shape classes so that the provided `main()`
function runs successfully, draws your shapes, and all pytest tests pass.

### Canvas Coordinates

The provided `Canvas` opens an 800 x 500 pixel window. These dimensions are
**class attributes** (`Canvas.WIDTH` and `Canvas.HEIGHT`) because every canvas
shares the same size. The point `(0, 0)` is the middle of the window, `x`
increases to the right, and `y` increases upward:

```
(-400, 250)                         (400, 250)
     +-----------------------------------+
     |                                   |
     |     (-180, 0)   (0, 0)  (180, 0)  |
     |         O          +       []     |
     |                                   |
     +-----------------------------------+
(-400, -250)                        (400, -250)
```

Each shape's `center` is the `(x, y)` point the shape is drawn around.

---

## Project Setup

### 1. Create Project Directory

```powershell
mkdir shapes_inheritance_oo
cd shapes_inheritance_oo
```

### 2. Initialize Python Environment with uv

```powershell
uv init --no-package
```

### 3. Install Dependencies

```powershell
uv add --dev pytest
```

### 4. Configure VS Code

The provided launch configuration lets you run the program and debug tests
with **F5**; copy it into your project in step 5.

Create `.vscode/settings.json` to enable test discovery:

```json
{
  "python.testing.pytestArgs": ["."],
  "python.testing.unittestEnabled": false,
  "python.testing.pytestEnabled": true
}
```

### 5. Copy Provided Files

Copy both files into your project directory:

- [`test_shapes.py`](./test_shapes.py) — pytest test suite
- [`shapes_starter.py`](./shapes_starter.py) — Starter template

Copy the provided [`launch.json`](./.vscode/launch.json) into the `.vscode`
folder in your project, then rename `shapes_starter.py` to `shapes.py`:

### 6. Verify Setup

```powershell
pytest --version
python shapes.py   # Will fail until you implement the shape classes
```

### Project Structure

```
shapes_inheritance_oo/
├── .venv/
├── .vscode/
│   ├── launch.json
│   └── settings.json
├── test_shapes.py       # Provided — do not modify
└── shapes.py            # Your implementation (copy of shapes_starter.py)
```

---

## Your Goal: Complete the Classes

The `shapes_starter.py` file contains a complete `Canvas` class and `main()`
function. Your job is to implement the three shape classes in the TODO
section so the program runs and all tests pass. 

** Do not modify `Canvas` or `main()`.**

---

## Turtle Drawing Primer

Your `draw()` methods use Python's built-in `turtle` module. Think of the
`pen` as a robot holding a marker on the canvas. You give it commands one at a
time: lift the marker, move somewhere, put the marker down, then move to draw
lines.

### The Pen Commands You Need

The provided `Canvas` creates the pen and passes it to your `draw()` method.
You only need these commands:

| Command | What it does |
|---|---|
| `pen.penup()` | Lift the marker so moving does **not** draw a line |
| `pen.pendown()` | Put the marker down so moving **does** draw a line |
| `pen.goto(x, y)` | Move straight to the point `(x, y)` |
| `pen.setheading(0)` | Face right (east). `90` is up, `180` is left, `270` is down |
| `pen.color(name)` | Set the line and fill color, e.g. `"red"` or `"#00aa88"` |
| `pen.begin_fill()` | Start remembering the outline that should be filled |
| `pen.end_fill()` | Fill the outline drawn since `begin_fill()` |
| `pen.forward(distance)` | Move forward `distance` pixels in the facing direction |
| `pen.left(angle)` | Turn counterclockwise by `angle` degrees |
| `pen.circle(radius)` | Draw a full circle, curving to the left of the pen |

### The Drawing Recipe

Both shapes follow the same four steps. Only steps 2 and 4 differ:

1. Lift the pen: `pen.penup()`
1. Move to the **starting point** of the shape with `pen.goto(...)`
1. Face right and put the pen down: `pen.setheading(0)` then `pen.pendown()`
1. Set the color and draw the outline between `pen.begin_fill()` and
   `pen.end_fill()`

Always start with `x, y = self.center` to unpack the inherited center into two
variables.

### Try It First

Before writing your classes, save this as `turtle_practice.py` and run it.
It draws a filled green square whose bottom-left corner is at `(0, 0)`:

```python
import turtle


def main():
    """Draw one filled square to practice the pen commands."""
    pen = turtle.Turtle()
    pen.penup()
    pen.goto(0, 0)
    pen.setheading(0)
    pen.pendown()
    pen.color("green")
    pen.begin_fill()
    for _ in range(4):
        pen.forward(100)
        pen.left(90)
    pen.end_fill()
    turtle.done()


if __name__ == "__main__":
    main()
```

Experiment by changing the `goto` point, the color, and the `forward`
distance. Close the window to end the program.

---

## Class Requirements

### Class 1: `Shape` (Base Class)

The `Shape` class stores what every shape has in common and defines the shared
interface for all shapes.

#### `__init__(self, color: str, center: tuple[float, float])`

Both arguments are **required** — a shape cannot be created without a color
and a position.

- Store `color` as `self._color` (protected)
- Store `center` as `self._center` (protected), for example `(-180, 0)`

#### `@property color` and `@color.setter`

- Getter: return `self._color`
- Setter: update `self._color` to `value`

#### `@property center`

Return `self._center`. There is no setter, so the center is read-only.

#### `def area(self) -> float`

Raise `NotImplementedError("Subclasses must implement area()")`.

#### `def perimeter(self) -> float`

Raise `NotImplementedError("Subclasses must implement perimeter()")`.

#### `def draw(self, pen)`

Raise `NotImplementedError("Subclasses must implement draw()")`.

The `pen` is a `turtle.Turtle` object that the provided `Canvas` passes in.

---

### Class 2: `Circle(Shape)` (Subclass)

```python
class Circle(Shape):   # <-- inherits from Shape
```

#### `__init__(self, color: str, center: tuple[float, float], radius: float)`

```python
super().__init__(color, center)   # MUST call parent constructor first
```

- Validate `radius > 0`; raise `ValueError` if not
- Store as `self._radius`

#### `@property radius -> float`

Return `self._radius`.

#### `def area(self) -> float`

Area of a circle: **π × r²**

```python
import math
return math.pi * self._radius ** 2
```

#### `def perimeter(self) -> float`

Circumference: **2 × π × r**

```python
return 2 * math.pi * self._radius
```

#### `def draw(self, pen)`

Turtle's `pen.circle(radius)` does **not** draw around the pen's position.
It starts at the pen, which becomes the **bottom edge** of the circle, and
curves counterclockwise. To center the circle on `self.center`, start
`radius` pixels below the center:

```
          . - .
       /         \
      |   (x, y)  |     <- center
       \         /
          ' - '
            ^
      (x, y - radius)   <- start the pen here, facing right
```

The complete method follows the drawing recipe:

```python
def draw(self, pen):
    x, y = self.center
    pen.penup()                       # 1. lift the pen
    pen.goto(x, y - self._radius)     # 2. move to the bottom of the circle
    pen.setheading(0)                 # 3. face right...
    pen.pendown()                     #    ...and put the pen down
    pen.color(self.color)             # 4. set color and draw the outline
    pen.begin_fill()
    pen.circle(self._radius)
    pen.end_fill()
```

---

### Class 3: `Rectangle(Shape)` (Subclass)

#### `__init__(self, color: str, center: tuple[float, float], width: float, height: float)`

```python
super().__init__(color, center)
```

- Validate `width > 0` and `height > 0`; raise `ValueError` for each
- Store as `self._width`, `self._height`

#### Properties: `width`, `height`

Return `self._width` and `self._height` respectively.

#### `def area(self) -> float`

Area of a rectangle: **width × height**

#### `def perimeter(self) -> float`

Perimeter: **2 × (width + height)**

#### `def draw(self, pen)`

Draw the rectangle so its center is at `self.center`. The pen starts at the
**bottom-left corner**, which is half the width to the left of the center and
half the height below it:

```
     +-------------------+   ^
     |                   |   |
     |      (x, y)       | height
     |                   |   |
     +-------------------+   v
     ^
     (x - width / 2, y - height / 2)   <- start here, facing right

     <------ width ------>
```

From the corner, the pen draws the bottom, right, top, and left sides by
moving forward and turning left 90 degrees after each side. Opposite sides are
the same length, so the loop runs twice, drawing one width and one height
each time.

Fill in the blanks (`____`) using the drawing recipe and the diagram:

```python
def draw(self, pen):
    x, y = self.center
    pen.penup()
    pen.goto(____, ____)          # bottom-left corner
    pen.setheading(0)
    pen.pendown()
    pen.color(____)
    pen.begin_fill()
    for _ in range(2):
        pen.forward(____)         # bottom or top side
        pen.left(90)
        pen.forward(____)         # right or left side
        pen.left(90)
    pen.end_fill()
```

Check your work with `pytest test_shapes.py -k draw -v`.

---

### Provided: `Canvas`

You do not write this class, but read it to see how it uses your shapes.

| Member | Purpose |
|---|---|
| `WIDTH`, `HEIGHT`, `BACKGROUND` | Class attributes shared by every canvas |
| `name` | Window title |
| `add_shape(shape)` | Adds any `Shape` subclass |
| `shape_count` | Number of shapes on the canvas |
| `total_area` | Sum of `area()` for every shape |
| `largest_shape()` | Shape with the greatest `area()`, or `None` |
| `draw()` | Opens a window and calls `shape.draw(pen)` on every shape |

`Canvas.draw()` never checks whether a shape is a `Circle` or a `Rectangle`.
It calls `shape.draw(pen)` and Python runs the correct overridden method.
That is polymorphism.

---

## Running Your Code

```powershell
# Run the main() function - opens a window; close it to end the program
python shapes.py

# Run all tests
pytest test_shapes.py -v

# Run only the drawing tests (names that include "draw")
pytest test_shapes.py -k draw -v

# Run with coverage
pytest test_shapes.py --cov=shapes --cov-report=term-missing
```

---

## Suggested Order of Implementation

Work through the classes in this order — the tests build on each other:

1. **`Shape`** — base class (color, center, properties, stubs)
1. **`Circle`** — simplest subclass (one extra attribute: radius)
1. **`Rectangle`** — two extra attributes (width, height)

Run `pytest test_shapes.py -v` after each class to track progress. The tests
never open a window: the `pen` fixture provides a `FakePen` that records
drawing calls, and the `fake_turtle` fixture uses pytest's `monkeypatch` to
replace turtle's window functions. Run `python shapes.py` once all tests pass
to see your shapes drawn.

---

## Discussion Questions

After completing the exercise, discuss with your partner:

1. What would happen if `Circle.__init__` forgot to call
   `super().__init__(color, center)`? Try it and observe the error.

1. How can `Canvas.draw()` and `Canvas.total_area` work with both circles and
   rectangles without checking their type?

1. Why are `WIDTH` and `HEIGHT` class attributes on `Canvas` while `name` is
   an instance attribute?

1. What is the difference between `isinstance(c, Circle)` and
   `isinstance(c, Shape)` for a `Circle` object `c`?

---

## Turtle References

- [turtle - Turtle graphics (Python documentation)](https://docs.python.org/3.14/library/turtle.html)
  - [Tutorial](https://docs.python.org/3.14/library/turtle.html#turtle-tutorial) - a short walkthrough of the basics
  - [Turtle motion](https://docs.python.org/3.14/library/turtle.html#turtle-motion) - `forward`, `left`, `goto`, `setheading`, `circle`
  - [Pen control](https://docs.python.org/3.14/library/turtle.html#pen-control) - `penup`, `pendown`, `color`
  - [Filling](https://docs.python.org/3.14/library/turtle.html#filling) - `begin_fill`, `end_fill`
  - [Methods of TurtleScreen/Screen](https://docs.python.org/3.14/library/turtle.html#methods-of-turtlescreen-screen) - `setup`, `bgcolor`, `title` (used by the provided `Canvas`)
- [Beginner's Guide to the Python turtle Library (Real Python)](https://realpython.com/beginners-guide-python-turtle/)
- [Tk color names](https://www.tcl-lang.org/man/tcl8.6/TkCmd/colors.htm) - every color name you can pass to `pen.color()`
