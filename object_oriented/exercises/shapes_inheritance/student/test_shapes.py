"""Tests for the Shape Drawing System inheritance exercise."""

import math
import turtle

import pytest
from shapes import Canvas, Circle, Rectangle, Shape


class FakePen:
    """Stand-in for turtle.Turtle that records calls instead of drawing."""

    def __init__(self):
        self.calls = []

    def penup(self):
        self.calls.append(("penup",))

    def pendown(self):
        self.calls.append(("pendown",))

    def goto(self, x, y):
        self.calls.append(("goto", x, y))

    def setheading(self, angle):
        self.calls.append(("setheading", angle))

    def color(self, value):
        self.calls.append(("color", value))

    def begin_fill(self):
        self.calls.append(("begin_fill",))

    def end_fill(self):
        self.calls.append(("end_fill",))

    def circle(self, radius):
        self.calls.append(("circle", radius))

    def forward(self, distance):
        self.calls.append(("forward", distance))

    def left(self, angle):
        self.calls.append(("left", angle))

    def hideturtle(self):
        self.calls.append(("hideturtle",))

    def speed(self, value):
        self.calls.append(("speed", value))


class FakeScreen:
    """Stand-in for turtle.Screen that records its settings."""

    def __init__(self):
        self.size = None
        self.background = None
        self.window_title = None

    def setup(self, width, height):
        self.size = (width, height)

    def bgcolor(self, value):
        self.background = value

    def title(self, value):
        self.window_title = value


@pytest.fixture
def canvas_with_shapes():
    """Provide an empty canvas and one of each shape."""
    canvas = Canvas("Test Canvas")
    circle = Circle("red", (0, 0), 5.0)
    rectangle = Rectangle("blue", (10, 20), 4.0, 6.0)
    return canvas, circle, rectangle


@pytest.fixture
def pen():
    """Provide a fake pen that records drawing calls without opening a window."""
    return FakePen()


@pytest.fixture
def fake_turtle(monkeypatch, pen):
    """Replace turtle's window functions so Canvas.draw() opens no window.

    Returns:
        tuple: The (screen, pen) fakes that Canvas.draw() will use.
    """
    screen = FakeScreen()

    def fake_screen():
        return screen

    def fake_turtle_pen():
        return pen

    def fake_done():
        pass

    monkeypatch.setattr(turtle, "Screen", fake_screen)
    monkeypatch.setattr(turtle, "Turtle", fake_turtle_pen)
    monkeypatch.setattr(turtle, "done", fake_done)
    return screen, pen


def test_base_shape_cannot_be_used_directly():
    """A bare Shape is unusable regardless of how the class enforces it.

    Accepts either error so the test works whether Shape uses
    NotImplementedError stubs or ABC abstract methods - the suite tests
    the behavior, not the mechanism.
    """
    with pytest.raises((TypeError, NotImplementedError)):
        Shape("red", (0, 0)).area


def test_color_property_is_read_only():
    circle = Circle("red", (0, 0), 5.0)
    assert circle.color == "red"
    with pytest.raises(AttributeError):
        circle.color = "blue"


def test_circle_stores_attributes():
    circle = Circle("red", (-180, 0), 5.0)
    assert circle.color == "red"
    assert circle.center == (-180, 0)
    assert circle.radius == 5.0


@pytest.mark.parametrize("radius", [0.0, -3.0])
def test_circle_rejects_non_positive_radius(radius):
    with pytest.raises(ValueError):
        Circle("red", (0, 0), radius)


def test_circle_area():
    assert Circle("red", (0, 0), 5.0).area == pytest.approx(math.pi * 25)


def test_circle_perimeter():
    assert Circle("red", (0, 0), 5.0).perimeter == pytest.approx(2 * math.pi * 5)


def test_circle_draw_starts_below_center_and_uses_color(pen):
    Circle("red", (-180, 0), 50).draw(pen)
    assert ("goto", -180, -50) in pen.calls
    assert ("color", "red") in pen.calls
    assert ("circle", 50) in pen.calls


def test_circle_draw_lifts_pen_at_end(pen):
    Circle("red", (-180, 0), 50).draw(pen)
    assert pen.calls[-1] == ("penup",)


def test_rectangle_stores_attributes():
    rectangle = Rectangle("blue", (180, 0), 4.0, 6.0)
    assert rectangle.color == "blue"
    assert rectangle.center == (180, 0)
    assert rectangle.width == 4.0
    assert rectangle.height == 6.0


@pytest.mark.parametrize(
    ("width", "height"),
    [(-1.0, 6.0), (0.0, 6.0), (4.0, -1.0), (4.0, 0.0)],
)
def test_rectangle_rejects_non_positive_dimensions(width, height):
    with pytest.raises(ValueError):
        Rectangle("blue", (0, 0), width, height)


def test_rectangle_area():
    assert Rectangle("blue", (0, 0), 4.0, 6.0).area == pytest.approx(24.0)


def test_rectangle_perimeter():
    assert Rectangle("blue", (0, 0), 4.0, 6.0).perimeter == pytest.approx(20.0)


def test_rectangle_draw_starts_at_bottom_left_corner_and_uses_color(pen):
    Rectangle("blue", (180, 0), 200, 100).draw(pen)
    assert ("goto", 80, -50) in pen.calls
    assert ("color", "blue") in pen.calls
    assert pen.calls.count(("forward", 200)) == 2
    assert pen.calls.count(("forward", 100)) == 2


def test_rectangle_draw_lifts_pen_at_end(pen):
    Rectangle("blue", (180, 0), 200, 100).draw(pen)
    assert pen.calls[-1] == ("penup",)


def test_circle_and_rectangle_inherit_from_shape():
    assert isinstance(Circle("red", (0, 0), 5.0), Shape)
    assert isinstance(Rectangle("blue", (0, 0), 4.0, 6.0), Shape)


def test_shapes_provide_polymorphic_area_and_perimeter():
    circle = Circle("red", (0, 0), 1.0)
    rectangle = Rectangle("blue", (0, 0), 2.0, 3.0)
    assert circle.area == pytest.approx(math.pi)
    assert rectangle.area == pytest.approx(6.0)
    assert circle.perimeter == pytest.approx(2 * math.pi)
    assert rectangle.perimeter == pytest.approx(10.0)


def test_lt_compares_shapes_by_area():
    small = Circle("red", (0, 0), 1.0)
    big = Rectangle("blue", (0, 0), 10.0, 10.0)
    assert small < big
    assert not big < small


def test_sorted_orders_shapes_smallest_to_largest():
    small = Rectangle("green", (0, 0), 1.0, 2.0)
    medium = Circle("red", (0, 0), 2.0)
    large = Rectangle("blue", (0, 0), 5.0, 10.0)
    assert sorted([large, small, medium]) == [small, medium, large]


def test_canvas_dimensions_are_class_attributes():
    assert Canvas.WIDTH == 800
    assert Canvas.HEIGHT == 500
    assert Canvas("Any Canvas").WIDTH == Canvas.WIDTH


def test_canvas_stores_name():
    assert Canvas("My Canvas").name == "My Canvas"


def test_canvas_starts_empty():
    assert Canvas("Empty Canvas").shape_count == 0


def test_add_shape_increases_count(canvas_with_shapes):
    canvas, circle, _ = canvas_with_shapes
    canvas.add_shape(circle)
    assert canvas.shape_count == 1


def test_total_area_is_zero_for_empty_canvas(canvas_with_shapes):
    canvas, _, _ = canvas_with_shapes
    assert canvas.total_area == pytest.approx(0.0)


def test_total_area_sums_shapes(canvas_with_shapes):
    canvas, circle, rectangle = canvas_with_shapes
    canvas.add_shape(circle)
    canvas.add_shape(rectangle)
    assert canvas.total_area == pytest.approx(circle.area + rectangle.area)


def test_largest_shape_returns_shape_with_greatest_area(canvas_with_shapes):
    canvas, circle, rectangle = canvas_with_shapes
    canvas.add_shape(circle)
    canvas.add_shape(rectangle)
    assert canvas.largest_shape() is circle


def test_largest_shape_returns_none_when_canvas_is_empty():
    assert Canvas("Empty").largest_shape() is None


def test_canvas_draw_uses_class_dimensions(fake_turtle):
    screen, _ = fake_turtle
    Canvas("My Drawing").draw()
    assert screen.size == (Canvas.WIDTH, Canvas.HEIGHT)
    assert screen.background == Canvas.BACKGROUND
    assert screen.window_title == "My Drawing"


def test_canvas_draw_draws_every_shape(fake_turtle, canvas_with_shapes):
    _, pen = fake_turtle
    canvas, circle, rectangle = canvas_with_shapes
    canvas.add_shape(circle)
    canvas.add_shape(rectangle)
    canvas.draw()
    assert ("color", "red") in pen.calls
    assert ("circle", 5.0) in pen.calls
    assert ("color", "blue") in pen.calls
    assert ("forward", 4.0) in pen.calls
