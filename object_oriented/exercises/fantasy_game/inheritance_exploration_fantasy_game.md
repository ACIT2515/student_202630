# Exercise: Object-Oriented Design in "Last Stand: Warlord's Siege"

Welcome to the codebase for **Last Stand: Warlord's Siege**! This fantasy game
was built specifically to demonstrate core Object-Oriented Programming (OOP)
concepts in Python.

In this exercise, you will play the game, analyze the source code, and answer
questions about its architecture, before finally expanding the game yourself.

The initial code is avialable via your Last Stand: Warlord's Siege Expand the Roster Lab.

---

## Part 1: Play the Game

Before looking at the code, experience the game from the player's perspective.

1. Open a terminal and run the game: `python warlords_siege.py`
2. Build a team of 3 heroes and play through at least one wave.
3. Observe how enemies target your heroes, and how characters behave differently
   when their HP drops below 40%.

---

## Part 2: Code Analysis

Read through `characters.py` and `warlords_siege.py` alongside the RealPython
article on Inheritance and Composition. Answer the following foundational
Object-Oriented Programming (OOP) questions.

### 1. Classes, Objects, and Attributes

Before diving into inheritance, we need to understand the basic building blocks
of OOP.

#### Question 1a

What is the difference between a "Class" and an "Object" (also called an
instance)? Find an example in `warlords_siege.py` where a class is instantiated
to create an object, and paste that line of code.

#### Question 1b

Look at the `Character` class's `__init__` method in `characters.py`. Identify
two _attributes_ (state/data) that every character has, and identify two
_methods_ (behaviors/actions) that every character can perform.

### 2. Inheritance ("Is-A" Relationship)

Inheritance allows us to create specialized versions of existing classes.

#### Question 2a

In `characters.py`, the `Warrior` class is defined with
`class Warrior(Character):`, meaning it inherits from
`Character`. In plain English, what is the major advantage of doing this rather
than writing the `Warrior` class completely from scratch?

#### Question 2b

Look closely at the `Mage` class. You will notice it has its own `attack`
method, but it does _not_ have its own `take_damage` method. If an enemy attacks
a `Mage` object, how does the program know how to reduce the Mage's health if
the code isn't written inside the `Mage` class itself?

### 3. Abstract Base Classes (ABC)

The `Character` class is built as an Abstract Base Class (ABC).

#### Question 3a

According to the codebase and the assigned reading, what is the primary purpose
of an Abstract Base Class? Why do we create them if they don't do all the work
themselves?

#### Question 3b

In `warlords_siege.py`, temporarily add the line
`test_character = Character("Bob")` at the bottom of the file and run it. What
exact error do you get? Why is it a good design choice to prevent developers
from creating a generic `Character` directly?

### 4. Overriding and Extensibility

Subclasses can change or add to the behaviors of their parent classes.

#### Question 4a

Both the `Character` base class and the `Rogue` class mention an `attack`
method. Why does the `Rogue` class write its own version of
`attack(self, target)`? What would happen if the developer forgot to include it?

#### Question 4b

Look at the `_level_up` method inside the `Warrior` class. It contains the line
`super()._level_up()`. Based on your reading, what does the `super()` function
do here, and why is it useful instead of just copying and pasting the level-up
code from the parent class?

### 5. Composition ("Has-A" Relationship)

The article emphasizes that while inheritance means "Is A", composition means
"Has A" or "Uses A".

#### Question 5a

Currently, this game relies on Inheritance (`Mage` _is a_ `Character`). Imagine
we want to allow characters to equip, drop, and trade generic items like a
"Steel Sword" or a "Wooden Shield". Based on your readings, should we use
Inheritance or Composition to add these items to our heroes? Explain why.

#### Question 5b

Composition is actually already being used in a few places in this project! Look
at the `WaveSurvivalGame` class in `warlords_siege.py`. How does it use
Composition to build the player's team and the enemy's team? (Hint: what do the
`_player_team` and `_enemy_team` attributes hold?)

### 6. Game Class Diagram (UML)

To fully grasp the game's design, it helps to visualize how the pieces connect.

#### Question 6

Create a rough UML class diagram mapping out the game's architecture. You can
use a tool like draw.io, Mermaid, other diagramming software, or even pen and
paper (take a clear photo).

Your diagram must include at least:
- The base `Character` class.
- At least three playable subclasses (e.g., `Warrior`, `Mage`, `Rogue`) showing
  their inheritance relationship to `Character` (lines with hollow arrows
  pointing to the parent).
- The `Enemy` mixin and how the `Boss` class inherits from multiple parents
  (`Enemy` and `Warrior`).
- The `WaveSurvivalGame` class, showing a composition/aggregation relationship (a
  line with a diamond) indicating that it "has" or "contains" `Character`
  objects.


