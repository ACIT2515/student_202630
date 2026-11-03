# Lab: Warlords - Siege Expand the Roster

Your task is to act as a developer for _Last Stand: Warlord's Siege_. You must
design and implement **one** completely new character class.

> **Constraints — do not modify these files:**
> - `characters.py` — the core class hierarchy is locked.
> - `warlords_siege.py` — the game engine is locked.
>
> All new code goes into `character_pack.py` (your character class) and
> `warlords_siege_expanded.py` (the launcher you will write in Step 6).

## Development Roadmap

Follow these steps to build your character inside `characters.py`:

1. **Class Definition:** Create your class so it inherits from the base class
   (e.g., `class Archer(Character):`).
2. **The Setup:** Write the `__init__` method. Make sure to call
   `super().__init__(name, max_health, attack_power)` to set up the inherited
   attributes, then add your character's unique attribute (like
   `self._arrows = 5`).
3. **Fulfilling the Contract:** `Character` is an Abstract Base Class. It will
   crash if you don't implement the required abstract properties
   (`character_type`, `resource_info`) and methods (`attack`, `special_ability`,
   `_level_up`). Start by returning simple strings or basic print statements for
   these to get the game to run.
4. **Implement the Logic:** Fill in the combat mechanics based on the archetype
   you choose below. Make sure to include the "fallback" mechanic where attacks
   become desperate if health drops to 40% or below!

## The Archetypes

Choose ONE of the following starter archetypes to build:

### Option A: The Archer (Resource Management)

#### Stats

Low max health (80), high attack power (15).

#### Unique Attribute

`self._arrows` starts at 5.

#### Attack

Check if `self._arrows > 0`. If yes, deal `attack_power` damage and subtract 1
arrow. If no arrows, deal a weak "dagger" attack (only 5 damage).

#### Special Ability

_Restock_. Restores 3 arrows but costs 10 HP to perform (they get exhausted
gathering them).

#### Fallback (<40% HP)

They panic and fire blindly. 50% chance to miss entirely (deal 0 damage),
otherwise normal attack damage.

### Option B: The Berserker (State-based Math)

#### Stats

High max health (120), low base attack (8).

#### Unique Attribute

`self._rage` starts at 0.

#### Attack

Deals damage equal to `attack_power + self._rage`. Every time they attack,
`self._rage` increases by 2.

#### Special Ability

_Bloodlust_. Costs 20 HP. Deals heavy damage (`attack_power * 3`) and resets
`self._rage` back to 0.

#### Fallback (<40% HP)

Frenzied strikes! Their basic `attack` now hits twice. (Call
`target.take_damage` two times in a row).

### Option C: The Cleric (Breaking the Mold)

#### Stats

Average max health (90), very low base attack (4).

#### Unique Attribute

`self._spell_power` starts at 15 (just like the Mage).

#### Attack

Deals their tiny base `attack_power`. Every time they attack,
`self._spell_power` increases by 1.

#### Special Ability

_Holy Light_. Costs 15 HP to cast (like other characters, specials burn HP).
Instead of attacking the enemy, the Cleric focuses inward! They heal themselves
for `self._spell_power * 2` HP. (Use `target.take_damage(0)` to satisfy the game
loop, and manually increase `self._health`, making sure it doesn't exceed
`self._max_health`).

#### Fallback (<40% HP)

Desperate Prayer. The Cleric's `attack` method now also heals them for 5 HP, in
addition to dealing 0 damage to the enemy.

## Final Requirements

When your class is complete, you must:

1. Add three single-line code comments (`#`) inside your code labeling:
   - Where you initialize a new **attribute** specific to your class.
   - Where you utilize **inheritance** (by calling `super()`).
   - Where you are **overriding** a method or property from the parent class.
2. Run the game and verify your new character appears in the team-building menu
   automatically — Python finds all direct subclasses of `Character` at startup.

---

## Step 4: Place Your Class in `character_pack.py`

Rather than adding your new class directly to `characters.py`, package it in a
**separate module** called `character_pack.py`. This keeps the original module
clean and demonstrates that `Character.__subclasses__()` finds classes across
module boundaries.

```python
# character_pack.py
from characters import Character


class Archer(Character):   # inherit from Character
    ...
```

Any of the new character types (Archer, Berserker, Cleric) belong in this one
file.

---

## Step 5: Test Your Character

A test suite is provided in `tests/` for each archetype. Run the tests for
**your** archetype to verify your implementation is correct before moving on.

### Run a single archetype's tests

```bash
uv run pytest tests/test_archer.py -v
uv run pytest tests/test_berserker.py -v
uv run pytest tests/test_cleric.py -v
```

### Run the full test suite

```bash
uv run pytest -v
```

A passing run looks like:

```
tests/test_archer.py::TestArcher::test_archer_initialization   PASSED
tests/test_archer.py::TestArcher::test_attack_with_arrows_deals_attack_power_damage PASSED
...
16 passed
```

If a test fails, read the assertion message carefully — it tells you exactly
which attribute or return value doesn't match the expected specification.

---

## Step 6: Write the Expanded Game Launcher

Create a new file called `warlords_siege_expanded.py`. Its job is to load your
new character class and then start the game **without touching `warlords_siege.py`
or `characters.py`**.

Your file must:

1. Import `character_pack` so that Python defines your new class (and therefore
   registers it as a subclass of `Character`).
2. Import `WaveSurvivalGame` from `warlords_siege`.
3. Instantiate the game and call `run()`.

Here is the structure — fill in the blanks:

```python
# warlords_siege_expanded.py

# TODO: import character_pack here
# TODO: import WaveSurvivalGame here

if __name__ == "__main__":
    # TODO: create the game and run it
    ...
```

Once complete, run it:

```bash
uv run warlords_siege_expanded.py
```

You should now see your new character in the team-building menu alongside the
original four classes.

### Why does import order matter here?

`WaveSurvivalGame.__init__` builds its character menu by calling
`Character.__subclasses__()`, which returns every class that directly inherits
from `Character` **at that moment**. If `character_pack` is imported **before**
the game object is created, your new class is already known to Python and will
appear in the menu automatically.

If you import `WaveSurvivalGame` first and create it before importing
`character_pack`, your character will be missing from the menu — Python hasn't
seen the class yet.
