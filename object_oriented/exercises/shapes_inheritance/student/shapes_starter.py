"""
Shape Drawing System Exercise
==============================

This is your starter file. Implement the Shape, Circle, and Rectangle
classes in the TODO section below. The Canvas class and main() are
provided - do not modify them.

Your task:
1. Create the Shape base class with all required attributes and methods
2. Create Circle and Rectangle subclasses that inherit from Shape
3. Run `pytest test_shapes.py -v` to verify all tests pass
4. Run `python shapes.py` to see your shapes drawn in a window

Key OOP concepts to use:
- class SubClass(ParentClass):  to inherit from a parent
- super().__init__(...)         to call the parent constructor
- def method(self):            to override a parent method
- def __lt__(self, other):     dunder method that lets sorted() order shapes
"""

import math
import turtle

# ---------------------------------------------------------------------------
# TODO 1: Implement the Shape base class
# ---------------------------------------------------------------------------
#
# Requirements:
#   __init__(self, color: str, center: tuple[float, float])
#     - Store color as self._color (protected)
#     - Store center as self._center (protected), e.g. (-180, 0)
#
#   @property color -> str
#     - Return self._color (read-only, no setter - changing the color after
#       the shape is drawn would leave the canvas showing the old color)
#
#   @property center -> tuple[float, float]
#     - Return self._center (read-only, no setter)
#
#   @property area -> float
#     - raise NotImplementedError("Subclasses must implement area")
#     - A property because the area is a computed value that callers read
#       like an attribute: shape.area, no parentheses
#
#   @property perimeter -> float
#     - raise NotImplementedError("Subclasses must implement perimeter")
#     - A property, same as area
#
#   def draw(self, pen)
#     - raise NotImplementedError("Subclasses must implement draw()")
#     - pen is a turtle.Turtle created and passed in by the provided Canvas
#
#   def __lt__(self, other) -> bool
#     - Return self.area < other.area
#     - This "dunder" (double underscore) method is what Python calls when
#       it evaluates shape_a < shape_b. Defining it is all that sorted()
#       and list.sort() need to order a list of shapes by area.
#     - The provided Canvas.largest_shape() calls sorted() on its shapes,
#       so it will not work until you implement __lt__.
#     - Note: reading area raises NotImplementedError on the base Shape,
#       but a Circle or Rectangle runs its own overridden area property -
#       polymorphism!
#
# Drawing recipe used by every shape (see "Turtle Drawing Primer" in README):
#   1. pen.penup()                         lift the pen - moving won't draw
#   2. pen.goto(start_x, start_y)          move to the shape's starting point
#   3. pen.setheading(0); pen.pendown()    face right, put the pen down
#   4. pen.color(self.color)
#      pen.begin_fill() ... draw outline ... pen.end_fill()
#   5. pen.penup()                         leave the pen lifted when done
# ---------------------------------------------------------------------------
# TODO 2: Implement the Circle subclass
# ---------------------------------------------------------------------------
#
# class Circle(Shape):   <-- inherit from Shape
#
#   __init__(self, color: str, center: tuple[float, float], radius: float)
#     - Call super().__init__(color, center)  <-- runs Shape's __init__ first!
#     - Validate radius > 0; raise ValueError if not
#     - Store as self._radius (protected)
#
#   @property radius -> float
#     - Return self._radius
#
#   @property area -> float
#     - Return math.pi * self._radius ** 2   (π × r²)
#
#   @property perimeter -> float
#     - Return 2 * math.pi * self._radius    (circumference = 2πr)
#
#   def draw(self, pen)
#     - pen.circle(r) starts at the pen and curves left, so the pen
#       position becomes the BOTTOM edge of the circle. Start r below
#       the center:
#
#             . - .
#          /         \
#         |   (x, y)  |      <- center
#          \         /
#             ' - '
#               ^ (x, y - radius)  <- start here, facing right
#
#     - Complete method:
#         x, y = self.center
#         pen.penup()
#         pen.goto(x, y - self._radius)
#         pen.setheading(0)
#         pen.pendown()
#         pen.color(self.color)
#         pen.begin_fill()
#         pen.circle(self._radius)
#         pen.end_fill()
#         pen.penup()
# ---------------------------------------------------------------------------
# TODO 3: Implement the Rectangle subclass
# ---------------------------------------------------------------------------
#
# class Rectangle(Shape):   <-- inherit from Shape
#
#   __init__(self, color: str, center: tuple[float, float],
#            width: float, height: float)
#     - Call super().__init__(color, center)
#     - Validate width > 0 and height > 0; raise ValueError for each if not
#     - Store as self._width and self._height (protected)
#
#   @property width -> float
#   @property height -> float
#
#   @property area -> float
#     - Return self._width * self._height
#
#   @property perimeter -> float
#     - Return 2 * (self._width + self._height)
#
#   def draw(self, pen)
#     - Start at the BOTTOM-LEFT corner, facing right:
#
#         +-------------------+   ^
#         |      (x, y)       | height
#         +-------------------+   v
#         ^ (x - width / 2, y - height / 2)
#         <------ width ------>
#
#     - Draw bottom, right, top, left: forward then turn left 90 each time.
#       Opposite sides match, so loop twice (one width + one height per pass).
#     - Fill in the blanks (____):
#         x, y = self.center
#         pen.penup()
#         pen.goto(____, ____)          # bottom-left corner
#         pen.setheading(0)
#         pen.pendown()
#         pen.color(____)
#         pen.begin_fill()
#         for _ in range(2):
#             pen.forward(____)         # bottom or top side
#             pen.left(90)
#             pen.forward(____)         # right or left side
#             pen.left(90)
#         pen.end_fill()
#         pen.penup()
#
#     - Check with: pytest test_shapes.py -k draw -v


# ---------------------------------------------------------------------------
# PROVIDED: Canvas class - do not modify
# ---------------------------------------------------------------------------
class Canvas:
    """
    A drawing canvas that holds a collection of shapes and draws them.

    The canvas size is shared by every Canvas, so it is defined with
    class attributes rather than instance attributes.

    Demonstrates polymorphism - the canvas reads area and calls draw() on
    each shape without needing to know the specific shape type.
    """

    WIDTH = 800
    HEIGHT = 500
    BACKGROUND = "white"

    def __init__(self, name: str):
        """
        Initialize a canvas.

        Args:
            name (str): The name of the canvas, shown in the window title
        """
        self.name = name
        self._shapes = []

    def add_shape(self, shape: Shape):
        """
        Add a shape to the canvas.

        Args:
            shape (Shape): The shape to add (any Shape subclass)
        """
        self._shapes.append(shape)

    @property
    def shape_count(self) -> int:
        """Get the total number of shapes on the canvas."""
        return len(self._shapes)

    @property
    def total_area(self) -> float:
        """Get the sum of areas of all shapes on the canvas."""
        total = 0.0
        for shape in self._shapes:
            total += shape.area
        return total

    def largest_shape(self):
        """
        Return the shape with the largest area.

        Uses sorted(), which orders the shapes with Shape.__lt__, instead
        of a hand-written search loop. The last shape in ascending order
        is the largest.

        Returns:
            Shape: The shape with the largest area, or None if canvas is empty
        """
        if not self._shapes:
            return None
        return sorted(self._shapes)[-1]

    def draw(self):
        """
        Open a turtle window and draw every shape on the canvas.

        The window stays open until the user closes it.
        """
        screen = turtle.Screen()
        screen.setup(Canvas.WIDTH, Canvas.HEIGHT)
        screen.bgcolor(Canvas.BACKGROUND)
        screen.title(self.name)

        pen = turtle.Turtle()
        pen.hideturtle()
        pen.speed(0)

        for shape in self._shapes:
            shape.draw(pen)  # Polymorphism: Circle.draw() or Rectangle.draw()

        turtle.done()


def main():
    """Demonstration of the shape drawing system with inheritance."""

    # 1. Print header
    print("Shape Drawing System Demo")
    print("=" * 50)

    # 2. Create canvas (its size comes from the Canvas class attributes)
    canvas = Canvas("My Drawing")
    print(f"Canvas size: {Canvas.WIDTH} x {Canvas.HEIGHT}")

    # 3. Create shapes - each subclass calls super().__init__(color, center)
    circle = Circle("red", (-180, 0), 100)
    rect = Rectangle("blue", (180, 0), 240, 160)

    # 4. Add shapes to canvas (polymorphism - canvas accepts any Shape)
    canvas.add_shape(circle)
    canvas.add_shape(rect)

    # 5. Display canvas statistics
    print(f"\nCanvas: '{canvas.name}'")
    print(f"Total shapes on canvas: {canvas.shape_count}")
    print(f"Total area:             {canvas.total_area:.2f}")

    # 6. Find the largest shape (sorted() uses Shape.__lt__)
    biggest = canvas.largest_shape()
    print(f"\nLargest shape: {type(biggest).__name__} ({biggest.area:.2f})")

    # 7. Sort the shapes by area - sorted() compares them with Shape.__lt__
    print("\nShapes sorted by area (smallest to largest):")
    for shape in sorted([rect, circle]):
        print(f"  {type(shape).__name__}: {shape.area:.2f}")

    # 8. Demonstrate isinstance() and the inherited attributes
    print("\nDemonstrating isinstance() checks:")
    for shape in [circle, rect]:
        print(f"  {type(shape).__name__} at {shape.center} in {shape.color}")
        print(f"    isinstance(shape, Shape)?     {isinstance(shape, Shape)}")
        print(f"    isinstance(shape, Circle)?    {isinstance(shape, Circle)}")
        print(f"    isinstance(shape, Rectangle)? {isinstance(shape, Rectangle)}")

    # 9. color is read-only - a recolored shape must be a new object
    print("\nTrying to change the circle's color...")
    try:
        circle.color = "purple"
    except AttributeError:
        print("AttributeError: color is read-only - create a new shape instead")

    # 10. Draw the shapes - close the window to end the program
    print("\nDrawing shapes... close the window to exit.")
    canvas.draw()


if __name__ == "__main__":
    main()
