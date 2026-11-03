# Last Stand: Warlord's Siege - OOP Demonstration Game

A fantasy wave-survival game system that demonstrates 
object-oriented programming principles in Python

## Features

### Abstract Base Classes

Enforced interface contracts (`attack`, `special_ability`) via Python's `abc`
module.

### Abstract Properties

Utilizing `@property` decorators with `@abstractmethod`.

### Inheritance & Polymorphism

Multiple distinct character classes (Warrior, Mage, Archer, Rogue) exhibiting
polymorphic behavior in combat loops.

### Mixins & Multiple Inheritance

The `Enemy` mixin and the `Boss` class demonstrate Python's Method Resolution
Order (MRO).

### Subclass Discovery (`__subclasses__()`)

Playable characters are discovered automatically at startup via
`Character.__subclasses__()`, which returns all direct subclasses of
`Character`.

### Operator Overloading

Implementing `__lt__` and `__eq__` (dunder methods) to allow the AI to quickly
target the weakest hero using the built-in `min()` function.

## Quick Start

### Play the Game

To run the interactive game directly in your terminal:

```bash
python warlords_siege.py
```

## Project Structure

```
fantasy_game/
|-- README.md                    # This file
|-- pyproject.toml               # Project metadata and dev dependencies (pytest, pylint)
|-- uv.lock                      # Locked dependency versions (managed by uv, do not edit)
|-- .python-version              # Python version pin read by uv
|-- characters.py                # Core OOP hierarchy (Character, subclasses, Mixin)
|-- warlords_siege.py            # Main game loop and execution logic
|-- utility.py                   # CLI helper functions
|-- tests/
    |-- test_characters.py       # Comprehensive test suite for characters.py
    |-- test_archer.py           # Archer test suite - for expansion pack
    |-- test_berserker.py        # Berserker test suite - for expansion pack
    |-- test_cleric.py           # Cleric test suite - for expansion pack
```

## Characters & Mechanics

### Character Archetypes

#### Warrior

High armor, heavy berserker damage at the cost of personal HP.

#### Mage

High spell damage scaling rapidly with level, standard fireball attack.

#### Magic Archer

Uses chance-based accuracy. High burst damage potential.

#### Rogue

Relies on a finite consumable resource (Poison Charges) replenished on kill.

### Enemy "Smart AI" Engine

When the enemies calculate their turns in `warlords_siege.py`, they don't pick
targets randomly. Thanks to operator overloading (`__lt__` compares health), the
game simply calls `min(alive_heroes)` to automatically unleash attacks upon your
weakest, most vulnerable team member!

## Testing

Run the comprehensive test suite to verify the logic inside `characters.py`:

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v
```

### Test Coverage includes:

- Abstract base class structural enforcement
- Mixin and multiple inheritance MRO behavior
- Damage calculations, critical hits, and armor mitigation
- Operator overloading built-ins (`==`, `<`, `min()`, `max()`)
- Subclass registry presence
