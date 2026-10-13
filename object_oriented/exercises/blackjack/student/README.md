# Object-Oriented Card and Deck Design Exercise

## Overview

In this team exercise, you'll design and implement two fundamental classes for
card games: `Card` and `Deck`. You'll start by creating your own design, then
refactor it to work with an existing Blackjack game. This exercise focuses on:

- Designing classes to model real-world entities
- Making your own design decisions and tradeoffs
- Reading existing code to discover interface requirements
- Documenting interface specifications through code analysis
- Refactoring code to meet interface requirements
- Implementing encapsulation and data hiding
- Writing tests to verify your implementation
- Understanding how your code integrates with existing systems

TeamSize: 2 students, each has their own copy of the source code.

## Context

You're building the foundation for a card game system. You'll first create
`Card` and `Deck` classes based on your own design decisions. Then, you'll
discover that a complete Blackjack game (`blackjack.py`) needs to use your
classes—but it has specific interface requirements. Your challenge is to
discover those requirements, document them, and refactor your implementation to
satisfy them while maintaining functionality.

## Background

1. [Standard 52 Card Deck](https://en.wikipedia.org/wiki/Standard_52-card_deck)
1. [Blackjack Game](https://bicyclecards.com/how-to-play/blackjack/)

## Project Setup

Before starting the exercise, set up your project environment properly.

### 1. Create Project Directory

```powershell
# Create and navigate to project directory
mkdir blackjack_oo
cd blackjack_oo
```

### 2. Initialize Python Environment with uv

Use `uv` to create a virtual environment and install dependencies:

```powershell
# Initialize a new Python project with uv
uv init

# Create virtual environment
uv venv

# Activate the virtual environment
# On Windows PowerShell:
.venv\Scripts\Activate.ps1

# On Windows CMD:
.venv\Scripts\activate.bat

# On macOS/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies

Install pytest for testing:

```powershell
uv add --dev pytest
```

### 4. Configure VSCode

Create a `.vscode` folder with configuration files:

#### Debugger Configuration (`.vscode/launch.json`)

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Current File",
      "type": "debugpy",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal",
      "justMyCode": true
    },
    {
      "name": "Python: Blackjack Game",
      "type": "debugpy",
      "request": "launch",
      "program": "${workspaceFolder}/blackjack.py",
      "console": "integratedTerminal",
      "justMyCode": true
    },
    {
      "name": "Python: Test with Pytest",
      "type": "debugpy",
      "request": "launch",
      "module": "pytest",
      "args": ["${file}", "-v"],
      "console": "integratedTerminal",
      "justMyCode": true
    }
  ]
}
```

#### Configure Testing in VSCode

Set up pytest testing in VSCode to enable test discovery and execution:

1. **Open the Testing Panel**
   - Click the Testing icon in the left sidebar (flask/beaker icon)
   - Or use Command Palette: `Ctrl+Shift+P` → "Test: Configure Python Tests"

2. **Select pytest as Testing Framework**
   - When prompted, select "pytest" from the list
   - If not prompted, click "Configure Python Tests" button in Testing panel

3. **Configure Test Discovery**
   - When asked "Where are your tests located?", select:
     - **Root directory** (or ".")
   - This tells VSCode that tests are in the same directory as source files
   - VSCode will discover all files matching `test_*.py` or `*_test.py`

4. **Verify Test Configuration**
   - The Testing panel should show a tree view
   - Once you create `test_cards.py`, it will appear here automatically

### 5. Copy Existing Files

Copy the provided files into your project directory:

- [`blackjack.py`](./blackjack.py) - The complete blackjack game implementation

The instructor will provide `test_blackjack.py` later in Part 7, after you
have discovered the interface requirements and refactored your classes.
For now, write your own tests based on your initial design.

### 6. Verify Setup

Test that everything works:

```powershell
# Verify pytest is installed
pytest --version

# Run blackjack (should fail initially - no cards.py yet)
python blackjack.py
```

### Project Structure

After setup, your directory should look like this:

```
blackjack_oo/
├── .venv/                  # Virtual environment (created by uv)
├── .vscode/
│   ├── settings.json      # Python and testing configuration
│   └── launch.json        # Debugger configurations
├── blackjack.py           # Provided: Complete blackjack game
├── cards.py               # You'll create this
└── test_cards.py          # You'll create this
```

## Part 1: Design Thinking

Before writing any code, discuss these questions with your team. There are no
"right" answers yet—you're exploring design possibilities.

### Card Design Questions

1. What attributes should a Card have?
   - What information does a playing card need to store?
   - How should you store rank: as a string ("Ace"), number (14), or both?

2. How should other code access card information?
   - Direct attribute access (`card.rank`)?
   - Method calls (`card.get_rank()`)?
   - Properties?

3. What behaviors (methods) should a Card have?
   - How should a card display itself to users?
   - Should cards be changeable after creation?
   - What operations might you perform on a card?

4. Should cards share any common data?
   - What information is the same for all cards?
   - Where should that data live?

### Deck Design Questions

5. What attributes should a Deck have?
   - What does a deck contain?
   - How do you want to store the cards?

6. What operations do you perform on a deck?
   - Think about a physical deck—what do you do with it?
   - How should these operations be represented as methods?

7. How should a deck be built?
   - What code creates all 52 cards?
   - Where should that code live?

8. What happens when something goes wrong?
   - What if you try to deal from an empty deck?
   - Return `None`, raise an exception, or something else?

Discuss these with your team and sketch out a rough design. Don't look ahead
yet!

## Part 2: Initial Implementation

Create a file called `cards.py` and implement your `Card` and `Deck` classes
inside this file based on your design discussion.

### Your Design, Your Choices

Implement the classes however makes sense to you:

- Choose your own attribute names and types
- Decide how to expose data (methods, properties, public attributes)
- Pick your own method names
- Handle errors your way
- Name things descriptively

### Minimum Functionality

Your classes should support these basic operations (but you choose how):

#### For Card:

- Create a card with a rank and suit
- Get the card's rank
- Get the card's suit
- Display the card as a string

#### For Deck:

- Create a standard 52-card deck
- Shuffle the deck
- Deal one card from the deck
- Handle dealing from an empty deck

Implement your initial design.

## Part 3: Testing Your Implementation

Now write tests for your classes in `test_cards.py`. This helps you verify your
implementation works correctly BEFORE trying to integrate it.

### Why Test First?

- Confirms your implementation actually works
- Documents how your classes are supposed to behave
- Makes refactoring safer later (tests catch regressions)
- Helps you think through edge cases

### Test Template

Use this template and fill in the TODOs based on YOUR design:

```python
import pytest
from cards import Card, Deck

class TestCard:
    """Test the Card class."""

    def test_card_creation(self):
        """Test that a card can be created."""
        # TODO: Create a card using YOUR init
        # TODO: Verify rank and suit are accessible
        pass

    def test_card_display(self):
        """Test that card converts to string nicely."""
        # TODO: Create a card
        # TODO: Convert to string and check format
        pass

    def test_different_ranks(self):
        """Test cards with different ranks (Ace, King, numbers)."""
        # TODO: Test Ace, face cards, number cards
        pass

class TestDeck:
    """Test the Deck class."""

    def test_deck_initialization(self):
        """Test that a deck can be created."""
        # TODO: Create deck and verify it has 52 cards
        # HINT: Deal all cards and count them
        pass

    def test_deal_card(self):
        """Test that dealing cards works."""
        # TODO: Create deck, deal a card
        # TODO: Verify you got a Card object back
        # HINT: Use isinstance(card, Card)
        pass

    def test_empty_deck(self):
        """Test what happens with empty deck."""
        # TODO: Deal all 52 cards
        # TODO: Test YOUR error handling
        # If you return None: assert deck.deal_card() is None
        # If you raise exception: use pytest.raises(ExceptionType)
        pass
```

### Run Your Tests

```bash
pytest test_cards.py -v
```

All tests should pass! If they don't, fix your implementation or your tests.

Complete and run tests for your design.

## Part 4: Integration Challenge

Now for the twist: A complete Blackjack game has been written (`blackjack.py`),
and it needs to use your Card and Deck classes—but it was written with specific
expectations about your interface.

### Try running the game with your current implementation:

```bash
python blackjack.py
```

#### What happens

- Does it work perfectly? (Unlikely on the first try!)
- Do you get `AttributeError`s? (The game might expect `.rank` but you used
  `.get_rank()`)
- Do you get `TypeError`s? (The game might expect certain parameter types)
- Does it work but behave incorrectly? (Values might be interpreted differently)

### Initial exploration

- What interface does `blackjack.py` seem to expect?
- What error messages do you see?
- What differences exist between your design and what the game needs?

Complete this initial exploration.

## Part 5: Discover and Document Requirements

Now dig deeper into `blackjack.py` to discover the exact interface requirements.
Your team needs to identify what your classes must provide.

### Your Task

Open `blackjack.py` and read through the code. Use the checklist below to guide
your exploration. Write your answers down and discuss them verbally as a team

#### Interface Discovery Checklist

Use Ctrl+F (Find) in `blackjack.py` to search for these patterns:

##### Card Class Requirements:

1. Constructor (Search for: `Card(`)

   - [ ] Parameters needed: 
   - [ ] Are ranks strings or integers?
   - [ ] Example ranks you find: 

2. Properties (Search for: `card.rank`, `card.suit`)

   - [ ] Does it use `card.rank` (property) or `card.rank()` (method)?
   - [ ] What attributes does Card need: [ ] rank [ ] suit [ ] rank_value [ ]
         other: 
   - [ ] Type of rank: 
   - [ ] Type of rank_value: 

3. String Display (Search for: `str(card)` or `print(card)`)

   - [ ] Format expected: 

##### Deck Class Requirements:

4. Constructor
   - [ ] How many cards in a new deck: 
   - [ ] Which ranks: 
   - [ ] Which suits: 

5. Methods (Search for: `deck.shuffle`, `deck.deal`)
   - [ ] Method name for dealing: 
   - [ ] What does it return: 
   - [ ] Method name for shuffling: 

6. Empty Deck (Search for: `try:` or `except IndexError`)
   - [ ] When deck is empty, does deal method:
     - [ ] Return None
     - [ ] Raise exception 

### Tips for Discovery

- Use your IDE's "Find" feature (Ctrl+F) to search for patterns
- Look at import statements: `from cards import Card, Deck`
- Error messages from Part 4 reveal requirements!
- Discuss as a team—divide and conquer different sections

Complete the checklist. Keep it handy for refactoring!

## Part 6: Refactoring

Now refactor your `cards.py` to meet the interface requirements you discovered.
Refer to your completed checklist as you work. This is realistic—you often need
to adapt your code to work with other systems!

### Common Issues & Solutions

#### Game expects `card.rank_value` but you only have rank

- Add a `rank_value` property that returns the integer value
- Use a class attribute dict: `RANK_VALUES = {"Ace": 14, "King": 13, ...}`

#### Game expects string ranks ("Ace") but you used integers (14)

- Change to store strings, add rank_value property for integers

#### AttributeError about properties

- Make sure you're using `@property` decorator, not methods
- Use `card.rank` not `card.rank()` in your code

#### IndexError expected but getting None

- Change return None to `raise IndexError("message")`

### Design Improvements to Consider

While refactoring, also consider:

- Class attributes for shared data (`RANK_VALUES`, `SUITS`)
- Protected attributes (`_cards`, `_rank`, `_suit`) for encapsulation
- Type hints for better documentation
- Docstrings for classes and methods

Refactor your implementation. Use the checklist and refactoring guide!

## Part 7: Update Your Tests

Quickly update your `test_cards.py` to match the refactored interface. Focus on
the essentials.

### Why Update Tests?

Your refactoring changed the interface (how your classes are used) but not
the behavior (what they do). Update tests to verify everything still works.

### Quick Update Guide

```python
# If you had methods, change to properties:
def test_card_rank(self):
    card = Card("Ace", "Spades")
    assert card.rank == "Ace"  # Property, not card.get_rank()

# If you used integers, add rank_value test:
def test_rank_value(self):
    card = Card("Ace", "Hearts")
    assert card.rank_value == 14  # NEW property

# If you returned None, change to expect exception:
def test_empty_deck_raises_error(self):
    deck = Deck()
    for _ in range(52):
        deck.deal_card()
    with pytest.raises(IndexError):  # Changed from checking None
        deck.deal_card()
```

### Essential Test Coverage

Make sure these critical tests pass:

#### Card Tests 

- Card created with string rank and suit
- `rank` property returns string
- `rank_value` property returns correct integer
- `suit` property returns string

#### Deck Tests 

- New deck has 52 cards
- `deal_card()` returns a Card object
- `deal_card()` raises `IndexError` when empty

### Run Your Updated Tests

```bash
pytest test_cards.py -v
```

All tests should pass! If not, check your refactoring.

### Verify Integration with Blackjack

After completing interface discovery, refactoring, and updating your own
tests, obtain `test_blackjack.py` from your instructor. Copy it into your
project directory beside `blackjack.py`, `cards.py`, and `test_cards.py`.

Run the provided integration suite without changing it or the Blackjack game:

```bash
pytest test_blackjack.py -v
```

These focused tests verify that:

- Your Card objects work with Blackjack hand values and player displays
- Your shuffled Deck deals all 52 distinct cards and raises `IndexError` when empty
- Cards dealt by your Deck can be received by a Player
- The provided game can deal cards, complete turns, and finish a game using
  your classes

The tests use public methods and properties, not protected attributes such as
`_cards`. They do not require a particular deck storage structure or dealing
order. The complete-game test uses pytest's `monkeypatch` fixture to supply a
stand response and `capsys` to capture printed output; these are provided by
pytest, not methods you need to write.

This is an integration check, not exhaustive testing of every game scenario.
Keep your own `test_cards.py` tests for your classes' behavior.

All tests should pass! If any fail, review the error messages and check your
Card/Deck implementation against the requirements. Correct your classes
rather than changing the provided integration tests.

Update essential tests and verify they pass.

## Part 8: Final Verification

Verify everything works together:

1. **Run your Card/Deck tests:** `pytest test_cards.py -v` (all should pass)
2. **Run the blackjack game tests:** `pytest test_blackjack.py -v` (all should
   pass - confirms your classes work with the game)
3. **Run the game interactively:** `python blackjack.py`
4. Play a few rounds:
   - Cards display properly ("Ace of Spades", not "14 of Spades")
   - Game logic works (dealer hits to 17, winners determined correctly)
   - No errors or crashes

If something doesn't work, check:

- Are your property names exactly `rank`, `suit`, `rank_value`?
- Does `deal_card()` raise `IndexError` (not return `None`)?
- Does your deck create exactly 52 cards?
- Are card ranks stored as **strings** ("Ace") not integers (14)?

## Class Discussion

1. Design Choices

   - What initial design approaches did different teams take?
   - Methods vs properties? Public vs protected attributes?
   - Integer vs string ranks?

2. Testing Experience

   - How did having tests before refactoring help?
   - Did tests catch any refactoring mistakes?

3. Interface Discovery

   - What techniques worked well for finding requirements?
   - What requirements were hardest to discover?
   - How did error messages help?

4. Refactoring Insights

   - What was the most challenging change to make?
   - Why are properties preferred over methods for attributes?
   - Why raise exceptions instead of returning `None`?

5. Key Takeaways

   - How does discovering requirements by reading code compare to being given
     specs?
   - What would you do differently next time?
   - How does this relate to real-world development?

## Tips for Success

- Don't peek at blackjack.py early: Experience making your own design
  choices first
- Test incrementally: Write a little code, test it, repeat
- Be thorough in discovery: Search for ALL uses of Card and Deck in
  blackjack.py
- Read error messages carefully: They reveal what interface the game expects
- Use IDE search features: Ctrl+F is your friend for finding all usages
- Compare interfaces systematically: What does the game call vs what you
  wrote?
- Discuss as a team: Different people may spot different interface
  requirements
- Use properties for read-only data: `@property` makes attributes feel
  natural
- Raise exceptions for errors: More Pythonic than returning `None`
- Keep tests updated: Tests should match your current interface

---
