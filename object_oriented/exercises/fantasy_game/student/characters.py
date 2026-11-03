"""Character classes for the fantasy game.

This module demonstrates several object-oriented Python patterns:

* Abstract base classes (ABC): ``Character`` enforces implementation of
  abstract methods and properties in every concrete subclass.
* Abstract properties: ``character_type`` and ``resource_info`` are declared
  as ``@property @abstractmethod`` pairs.
* Abstract method with concrete body: ``_level_up`` is abstract so every
  subclass must override it and call ``super()._level_up()``, demonstrating
  cooperative multiple inheritance via Python's MRO.
* Multiple inheritance / mixin: ``Enemy(ABC)`` is a mixin that makes
  ``gain_experience`` a no-op. ``Boss(Enemy, Warrior)`` inherits from both.
* Operator overloading (Dunder methods): ``__lt__`` and ``__eq__`` allow
  custom character objects to work natively with built-in functions like
  ``min()`` and ``sorted()``.

Classes:
    Character: Abstract base class defining the common interface.
    Enemy: Mixin ABC for all computer-controlled (non-playable) characters.
    Warrior: Melee fighter with armor and berserker strike.
    Mage: Spell caster whose power scales with level.
    MagicArcher: Ranged fighter with an accuracy-based attack.
    Rogue: Poison-blade fighter with a finite consumable resource.

Example:
    >>> from characters import Warrior, Mage
    >>> warrior = Warrior("Thorin")
    >>> isinstance(warrior, Character)
    True
    >>> warrior.character_type
    'Warrior'
"""

import random
from abc import ABC, abstractmethod


class Character(ABC):
    """Abstract base class for all game characters.

    This class defines the common interface and shared functionality for all
    character types in the fantasy game. It enforces implementation of key
    methods through abstract methods while providing common attributes and
    behaviors.

    Args:
        name (str): The character's name
        health (int, optional): The character's maximum and starting health points.
            Defaults to 100.
        attack_power (int, optional): The character's base attack power.
            Defaults to 10.

    Attributes:
        _name (str): The character's name (protected)
        _max_health (int): The character's maximum health points (protected)
        _health (int): The character's current health points (protected)
        _attack_power (int): The character's base attack power (protected)
        _level (int): The character's current level (protected)
        _experience (int): The character's accumulated experience points (protected)

    Note:
        This is an abstract base class and cannot be instantiated directly.
        All subclasses must implement the abstract properties ``character_type``
        and ``resource_info``, the abstract methods ``attack``, ``special_ability``,
        and ``_level_up`` (which must call ``super()._level_up()``).
        It also defines ``__eq__`` and ``__lt__`` to enable health-based comparisons.

    Example:
        >>> # This will raise TypeError
        >>> char = Character("Test")  # Cannot instantiate abstract class
        >>> # Must use concrete subclass instead
        >>> warrior = Warrior("Test")
        >>> warrior.character_type
        'Warrior'
    """

    def __init__(self, name: str, health: int = 100, attack_power: int = 10):
        self._name = name
        self._max_health = health
        self._health = health
        self._attack_power = attack_power
        self._level = 1
        self._experience = 0

    @property
    def name(self) -> str:
        """str: The character's name (read-only)."""
        return self._name

    @property
    def health(self) -> int:
        """int: The character's current health points (read-only)."""
        return self._health

    @property
    def level(self) -> int:
        """int: The character's current level (read-only)."""
        return self._level

    @property
    def is_alive(self) -> bool:
        """bool: True if character has health > 0, False otherwise (read-only)."""
        return self._health > 0

    def __eq__(self, other: object) -> bool:
        """Check if two characters are equal (based on their name)."""
        if not isinstance(other, Character):
            return NotImplemented
        return self.name == other.name

    def __lt__(self, other: object) -> bool:
        """Define the 'less than' (<) operator based on current health.

        This allows lists of characters to be sorted automatically, and
        makes built-in functions like min() and max() work natively!
        """
        if not isinstance(other, Character):
            return NotImplemented
        return self.health < other.health

    def take_damage(self, damage: int):
        """Apply damage to the character.

        Reduces the character's health by the specified damage amount.
        Health cannot go below 0. Prints defeat message if health reaches 0.

        Args:
            damage (int): Amount of damage to apply. Must be non-negative.

        Example:
            >>> char.take_damage(25)
            >>> print(char.health)  # Reduced by 25
        """
        self._health = max(0, self._health - damage)
        if self._health == 0:
            print(f"{self._name} has been defeated!")

    def heal(self, amount: int):
        """Restore health to the character.

        Increases the character's health by the specified amount.
        Health cannot exceed maximum health.

        Args:
            amount (int): Amount of health to restore. Must be non-negative.

        Example:
            >>> char.heal(30)
            Thorin healed for 30 HP
        """
        old_health = self._health
        self._health = min(self._max_health, self._health + amount)
        healed = self._health - old_health
        if healed > 0:
            print(f"{self._name} healed for {healed} HP")

    def gain_experience(self, exp: int):
        """Add experience points and check for level up.

        Adds experience points to the character. If enough experience is
        accumulated (level * 100), triggers a level up.

        Args:
            exp (int): Experience points to add. Must be non-negative.

        Example:
            >>> char.gain_experience(150)
            Thorin leveled up to level 2!
        """
        self._experience += exp
        exp_needed = self._level * 50
        if self._experience >= exp_needed:
            self._level_up()

    @abstractmethod
    def _level_up(self):
        """Apply base level-up stat increases (abstract with concrete body).

        This method is declared abstract so every concrete subclass must
        override it.  The override should call ``super()._level_up()`` first
        to apply the base stat gains, then add any class-specific bonuses.

        Effects (applied via ``super()._level_up()`` call chain):
            - Level increases by 1
            - Max health increases by 20
            - Current health restored to maximum
            - Attack power increases by 5

        Note:
            Declaring an abstract method with a concrete body is valid Python.
            Subclasses cannot skip implementing ``_level_up``, yet they can
            reuse the base logic via cooperative ``super()`` calls —
            a demonstration of MRO-based cooperative inheritance.
        """
        self._level += 1
        self._max_health += 20
        self._health = self._max_health
        self._attack_power += 5
        print(f"{self._name} leveled up to level {self._level}!")

    @abstractmethod
    def attack(self, target) -> int:
        """Perform an attack on the target.

        Abstract method that must be implemented by all subclasses.
        Each character type should have unique attack behavior.

        Args:
            target (Character): The character to attack

        Returns:
            int: Amount of damage dealt

        Raises:
            NotImplementedError: If called on abstract base class
        """
        pass

    @abstractmethod
    def special_ability(self, target=None) -> int:
        """Use the character's special ability.

        Abstract method that must be implemented by all subclasses.
        Each character type should have a unique special ability.

        Args:
            target (Character, optional): The target character (if ability
                affects another character). Defaults to None.

        Returns:
            int: Amount of damage or effect value

        Raises:
            NotImplementedError: If called on abstract base class
        """
        pass

    @property
    @abstractmethod
    def character_type(self) -> str:
        """The character's type label (read-only abstract property).

        Subclasses must implement this as a ``@property``.

        Returns:
            str: The character type, e.g. ``'Warrior'`` or ``'Magic Archer'``.
        """

    @property
    @abstractmethod
    def resource_info(self) -> str:
        """Character-specific resource state (read-only abstract property).

        Subclasses must implement this as a ``@property``.  The returned
        string is appended to ``__str__`` output.

        Returns:
            str: Resource display string, e.g. ``', Armor: 5'``.
        """

    def __str__(self) -> str:
        """Return string representation of the character.

        Returns:
            str: Formatted string with character name, type, level,
                health, and resources

        Example:
            >>> str(warrior)
            'Thorin (Warrior, Lv.1) - HP: 120/120, Armor: 5'
        """
        base_info = (
            f"{self._name} ({self.character_type}, Lv.{self._level})"
            + f"- HP: {self._health}/{self._max_health}"
        )
        return f"{base_info}{self.resource_info}"


class Enemy(ABC):
    """Mixin ABC that marks a character as computer-controlled (NPC).

    Inherit from ``Enemy`` (alongside a concrete character class) to signal
    that the character is AI-controlled and should never gain experience or
    level up during combat.

    Place ``Enemy`` *before* the concrete class in the base-class list so
    Python's MRO resolves ``gain_experience`` to this no-op before reaching
    ``Character``'s real implementation::

        class Boss(Enemy, Warrior): ...
        # MRO: Boss → Enemy → Warrior → Character → ABC → object

    Example:
        >>> from warlords_siege import Boss
        >>> boss = Boss("Warlord Groth")
        >>> isinstance(boss, Enemy)
        True
        >>> isinstance(boss, Warrior)
        True
    """

    def gain_experience(self, exp: int):
        """No-op — computer-controlled enemies never level up.

        Args:
            exp (int): Ignored.
        """
        pass


class Warrior(Character):
    """Melee fighter with heavy armor and a berserker special strike.

    Combat dynamics
    ---------------
    * Full attack (HP > 40 % of max): Power Strike — ``attack_power``
      + random(−3, 8) with a 30 % chance of a critical hit that doubles
      damage.
    * Fallback (HP ≤ 40 % of max): Desperate lunge at ``attack_power // 2``.
    * Special — Berserker Rage (always fires): costs 20 HP; deals
      ``attack_power × 2`` + random(0, 10).  Clamped to 0; can be lethal.
    * Unique mechanic — Armor: reduces all incoming damage by
      ``_armor``; minimum 1 damage always applied.

    Starting stats: HP 120, attack_power 15, armor 5.

    Args:
        name (str): The warrior's name

    Attributes:
        _armor (int): Flat damage reduction applied to every hit (protected).

    Example:
        >>> warrior = Warrior("Conan")
        >>> warrior.attack(enemy)          # Power Strike above 40 % HP
        Conan swings their sword at Enemy!
        >>> warrior.special_ability(enemy) # Berserker Rage — costs 20 HP
        Conan enters BERSERKER RAGE! (\u221220 HP)
           The berserker strike engulfs Enemy!
    """

    def __init__(self, name: str):
        super().__init__(name, health=120, attack_power=15)
        self._armor = 5

    @property
    def character_type(self) -> str:
        """Returns:
        str: Always ``'Warrior'``.
        """
        return "Warrior"

    @property
    def resource_info(self) -> str:
        """Returns:
        str: Armor value, e.g. ``', Armor: 5'``.
        """
        return f", Armor: {self._armor}"

    def take_damage(self, damage: int):
        """Apply damage with armor reduction.

        Reduces incoming damage by the armor value, with a minimum of 1.

        Args:
            damage (int): Incoming damage amount

        Note:
            Prints armor reduction message when armor absorbs damage.

        Example:
            >>> warrior.take_damage(10)  # With 5 armor
            Thorin's armor reduces damage by 5
        """
        reduced_damage = max(1, damage - self._armor)
        if damage > reduced_damage:
            print(
                f"{self._name}'s armor reduces damage" f" by {damage - reduced_damage}"
            )
        super().take_damage(reduced_damage)

    def special_ability(self, target=None):
        """Unleash a berserker strike at terrible personal cost.

        Channels raw fury into a devastating blow — always fires regardless
        of current HP.  The downside: burns 20 of the warrior's own HP
        (clamped to 0), which can bring a low-health warrior dangerously
        close to death or finish them outright.

        Args:
            target (Character, optional): The character to target.
                If None, damage is calculated but not applied.

        Returns:
            int: Amount of damage dealt

        Note:
            Berserker Rage costs 20 HP and deals 2 × attack_power + random(0, 10).

        Example:
            >>> damage = warrior.special_ability(enemy)
            Thorin enters BERSERKER RAGE! (\u221220 HP)
               The berserker strike engulfs Enemy!
        """
        self._health = max(0, self._health - 20)
        damage = self._attack_power * 2 + random.randint(0, 10)
        print(f"{self._name} enters BERSERKER RAGE! (\u221220 HP)")
        if target:
            print(f"   The berserker strike engulfs {target.name}!")
            target.take_damage(damage)
        return damage

    def attack(self, target):
        """Perform a warrior sword attack.

        Above 40 % of max HP, delivers a full Power Strike with a 30 % chance
        of a critical hit that doubles damage.  Below the threshold the warrior
        is too injured to fight at full strength and falls back to a desperate
        lunge at half power with no crit chance.

        Args:
            target (Character): The character to attack

        Returns:
            int: Amount of damage dealt (doubled on critical hit)

        Example:
            >>> damage = warrior.attack(enemy)
            Thorin swings their sword at Enemy!
            >>> # Or on critical hit:
            CRITICAL HIT! Thorin delivers a devastating blow to Enemy!
            >>> # Or when below 40 % HP:
            Thorin fights through the pain with a desperate lunge at Enemy!
        """
        if self._health > self._max_health * 0.40:
            base_damage = self._attack_power + random.randint(-3, 8)
            if random.random() < 0.3:  # 30% crit chance
                base_damage *= 2
                print(
                    f"CRITICAL HIT! {self._name}",
                    f" delivers a devastating blow to {target.name}!",
                )
            else:
                print(f"{self._name} swings their sword at {target.name}!")
        else:
            base_damage = self._attack_power // 2
            print(
                f"{self._name} fights through the pain with a"
                f" desperate lunge at {target.name}!"
            )

        target.take_damage(base_damage)

        return base_damage

    def _level_up(self):
        """Level up with warrior-specific bonuses.

        Calls the base level-up (via ``super()``) then increases armor by 1,
        making the warrior more resilient at higher levels.

        Effects:
            - All standard effects via ``super()._level_up()``
            - ``_armor`` increases by 1
        """
        super()._level_up()
        self._armor += 1
        print(f"{self._name}'s armor has thickened!")


class Mage(Character):
    """Spell caster with high magic damage and a devastating fireball.

    Combat dynamics
    ---------------
    * Full attack (HP > 40 % of max): Magic Missile — ``spell_power``
      + random(−5, 10).
    * Fallback (HP ≤ 40 % of max): Weak staff prod at
      ``attack_power // 2``.
    * Special — Fireball (always fires): costs 25 HP; deals
      ``spell_power × 2`` + random(0, 15).  Clamped to 0; can be lethal.
    * Unique mechanic — Spell Power: scales with level (``_spell_power``
      +8 per level-up), making the Mage stronger than other classes
      over a long game.

    Starting stats: HP 80, attack_power 8, spell_power 20.

    Args:
        name (str): The mage's name

    Attributes:
        _spell_power (int): Base magical damage added to every spell (protected).

    Example:
        >>> mage = Mage("Merlin")
        >>> mage.attack(enemy)          # Magic Missile above 40 % HP
        Merlin casts Magic Missile at Enemy!
        >>> mage.special_ability(enemy) # Fireball — costs 25 HP
        Merlin casts FIREBALL! (\u221225 HP)
           The fireball engulfs Enemy!
    """

    def __init__(self, name: str):
        super().__init__(name, health=80, attack_power=8)
        self._spell_power = 20

    @property
    def character_type(self) -> str:
        """Returns:
        str: Always ``'Mage'``.
        """
        return "Mage"

    @property
    def resource_info(self) -> str:
        """Returns:
        str: Spell power, e.g. ``', SP: 20'``.
        """
        return f", SP: {self._spell_power}"

    def attack(self, target):
        """Cast Magic Missile or fall back to a weak staff prod.

        Above 40 % of max HP the mage has enough vitality to shape a Magic
        Missile dealing spell_power + random(-5, 10) damage.  Below the
        threshold the mage is too depleted and prods weakly with a staff
        at half attack_power.

        Args:
            target (Character): The character to attack

        Returns:
            int: Amount of damage dealt

        Example:
            >>> damage = mage.attack(enemy)
            Merlin casts Magic Missile at Enemy!
            >>> # Or when below 40 % HP:
            Merlin is too depleted to cast! Prodding weakly with staff...
        """
        if self._health > self._max_health * 0.40:
            damage = self._spell_power + random.randint(-5, 10)
            print(f"{self._name} casts Magic Missile at {target.name}!")
            target.take_damage(damage)
            return damage
        else:
            print(
                f"{self._name} is too depleted to cast!"
                " Prodding weakly with staff..."
            )
            damage = self._attack_power // 2
            target.take_damage(damage)
            return damage

    def special_ability(self, target=None):
        """Cast Fireball at terrible personal cost.

        Deals massive magical damage — always fires regardless of current HP.
        The downside: burns 25 of the mage's own HP (clamped to 0), which
        can bring a low-health mage dangerously close to death or finish
        them outright.

        Args:
            target (Character, optional): The character to target.
                If None, damage is calculated but not applied.

        Returns:
            int: Amount of damage dealt

        Note:
            Fireball costs 25 HP and deals 2 × spell_power + random(0, 15).

        Example:
            >>> damage = mage.special_ability(enemy)
            Merlin casts FIREBALL! (−25 HP)
               The fireball engulfs Enemy!
        """
        self._health = max(0, self._health - 25)
        damage = self._spell_power * 2 + random.randint(0, 15)
        print(f"{self._name} casts FIREBALL! (\u221225 HP)")
        if target:
            print(f"   The fireball engulfs {target.name}!")
            target.take_damage(damage)
        return damage

    def _level_up(self):
        """Level up with mage-specific bonuses.

        In addition to standard level up benefits, mages gain extra spell power.

        Effects:
            - All standard level up effects (health, attack, level)
            - Spell power increases by 8
        """
        super()._level_up()
        self._spell_power += 8
        print(f"{self._name}'s magical power has increased!")


class MagicArcher(Character):
    """Ranged fighter who channels life force into enchanted arrows.

    Combat dynamics
    ---------------
    * Full attack (HP > 40 % of max): Enchanted Arrow — 85 % hit
      chance; deals ``attack_power`` + random(0, 12).  Miss returns 0
      damage.  No HP cost.
    * Fallback (HP ≤ 40 % of max): Dagger strike at
      ``attack_power // 2`` — always hits, no HP cost.
    * Special — Magic Triple Shot (always fires): costs 20 HP; deals
      ``(attack_power + 5) × 3``.  Clamped to 0; can be lethal.
    * Unique mechanic — Accuracy: the full attack has a 15 % miss
      chance, making it the only standard attack that can deal 0 damage.

    Starting stats: HP 90, attack_power 12, accuracy 0.85.

    Args:
        name (str): The archer's name

    Attributes:
        _accuracy (float): Hit probability for the enchanted arrow (0.0–1.0)
            (protected).

    Example:
        >>> archer = MagicArcher("Legolas")
        >>> archer.attack(enemy)          # Enchanted Arrow above 40 % HP
        Legolas looses an enchanted arrow at Enemy!
        >>> archer.special_ability(enemy) # Triple Shot — costs 20 HP
        Legolas fires a MAGIC TRIPLE SHOT! (\u221220 HP)
           All three arrows hit Enemy!
    """

    def __init__(self, name: str):
        super().__init__(name, health=90, attack_power=12)
        self._accuracy = 0.85

    @property
    def character_type(self) -> str:
        """Returns:
        str: Always ``'Magic Archer'``.
        """
        return "Magic Archer"

    @property
    def resource_info(self) -> str:
        """Returns:
        str: Accuracy percentage, e.g. ``', Acc: 85%'``.
        """
        return f", Acc: {int(self._accuracy * 100)}%"

    def attack(self, target):
        """Shoot an enchanted arrow or use dagger backup.

        Above 40 % of max HP the archer has enough vitality to enchant an
        arrow with 85 % accuracy and full attack_power + random damage.  Below
        the threshold the archer is too drained and falls back to a quick
        dagger strike at half power that always hits.

        Args:
            target (Character): The character to attack

        Returns:
            int: Amount of damage dealt (0 if enchanted arrow misses)

        Note:
            Enchanted arrow has 85 % hit chance; deals attack_power + random(0, 12).
            Dagger deals half attack_power but always hits.

        Example:
            >>> damage = archer.attack(enemy)
            Legolas looses an enchanted arrow at Enemy!
            >>> # Or on miss:
            Legolas's arrow flies wide of Enemy!
            >>> # Or when below 40 % HP:
            Legolas is too drained! Drawing dagger instead...
        """
        if self._health > self._max_health * 0.40:
            if random.random() < self._accuracy:
                damage = self._attack_power + random.randint(0, 12)
                print(f"{self._name} looses an enchanted arrow at {target.name}!")
                target.take_damage(damage)
                return damage
            else:
                print(f"{self._name}'s arrow flies wide of {target.name}!")
                return 0
        else:
            print(f"{self._name} is too drained! Drawing dagger instead...")
            damage = self._attack_power // 2
            target.take_damage(damage)
            return damage

    def special_ability(self, target=None):
        """Fire a magic triple shot at terrible personal cost.

        Unleashes three enchanted arrows simultaneously — always fires
        regardless of current HP.  The downside: burns 20 of the archer's
        own HP (clamped to 0), risking injury in exchange for devastating
        ranged output.

        Args:
            target (Character, optional): The character to target.
                If None, damage is calculated but not applied.

        Returns:
            int: Total damage dealt

        Note:
            Triple shot costs 20 HP and deals (attack_power + 5) × 3 damage.

        Example:
            >>> damage = archer.special_ability(enemy)
            Legolas fires a MAGIC TRIPLE SHOT! (−20 HP)
               All three arrows hit Enemy!
        """
        self._health = max(0, self._health - 20)
        damage_per_arrow = self._attack_power + 5
        total_damage = damage_per_arrow * 3
        print(f"{self._name} fires a MAGIC TRIPLE SHOT! (\u221220 HP)")
        if target:
            print(f"   All three arrows hit {target.name}!")
            target.take_damage(total_damage)
        return total_damage

    def _level_up(self):
        """Level up with magic archer-specific bonuses.

        Calls the base level-up (via ``super()``) then improves accuracy
        by 0.02 (capped at 0.99), making shots harder to miss at higher levels.

        Effects:
            - All standard effects via ``super()._level_up()``
            - ``_accuracy`` increases by 0.02 (max 0.99)
        """
        super()._level_up()
        self._accuracy = min(0.99, self._accuracy + 0.02)
        print(f"{self._name}'s aim has sharpened!")


class Rogue(Character):
    """Agile fighter with poisoned blades and a shadow strike.

    Combat dynamics
    ---------------
    * Full attack (HP > 40 % of max): Twin-dagger combo —
      ``attack_power`` + random(−2, 6), with a 40 % chance to apply
      poison (+8 damage, consumes 1 charge).
    * Fallback (HP ≤ 40 % of max): Weak slash at
      ``attack_power // 2``; no poison chance.
    * Special — Shadow Strike (always fires): costs 15 HP; deals
      ``attack_power × 2`` + random(−2, 6) with guaranteed poison
      (+8 damage) if any charges remain (consumes 1 charge).  Clamped
      to 0; can be lethal.
    * Unique mechanic — Poison charges: finite consumable resource
      (max 5).  Restored by 1 per kill (``gain_experience`` override),
      keeping the rogue relevant in sustained combat.

    Starting stats: HP 85, attack_power 11, poison_charges 5.

    Args:
        name (str): The rogue's name

    Attributes:
        _poison_charges (int): Remaining poison applications (protected).
        _max_poison_charges (int): Maximum charges; cap for replenishment
            (protected).

    Example:
        >>> rogue = Rogue("Shadowblade")
        >>> rogue.attack(enemy)          # Twin daggers above 40 % HP
        Shadowblade strikes Enemy with twin daggers!
        >>> rogue.special_ability(enemy) # Shadow Strike — costs 15 HP
        Shadowblade launches a SHADOW STRIKE! (\u221215 HP)
    """

    def __init__(self, name: str):
        super().__init__(name, health=85, attack_power=11)
        self._max_poison_charges = 5
        self._poison_charges = self._max_poison_charges

    @property
    def character_type(self) -> str:
        """Returns:
        str: Always ``'Rogue'``.
        """
        return "Rogue"

    @property
    def resource_info(self) -> str:
        """Returns:
        str: Poison charge count, e.g. ``', Poison: 5'``.
        """
        return f", Poison: {self._poison_charges}"

    def attack(self, target):
        """Attack with daggers and possible poison.

        Above 40 % of max HP, strikes with a full dagger combo and has a
        40 % chance to apply poison for +8 bonus damage (consuming 1 charge).
        Below the threshold the rogue is too sluggish and can only manage a
        weak slash at half power with no poison chance.

        Args:
            target (Character): The character to attack

        Returns:
            int: Amount of damage dealt (including poison bonus)

        Note:
            Full combo: attack_power + random(-2, 6) + possible 8 poison damage.
            Weak slash: attack_power // 2, no poison.

        Example:
            >>> damage = rogue.attack(enemy)
            Shadowblade strikes Enemy with twin daggers!
            >>> # With poison:
            The blade was poisoned! Extra damage dealt!
            >>> # Or when below 40 % HP:
            Shadowblade stumbles, managing only a weak slash at Enemy!
        """
        if self._health > self._max_health * 0.40:
            base_damage = self._attack_power + random.randint(-2, 6)
            print(f"{self._name} strikes {target.name} with twin daggers!")
            if self._poison_charges > 0 and random.random() < 0.4:
                self._poison_charges -= 1
                base_damage += 8
                print("The blade was poisoned! Extra damage dealt!")
        else:
            base_damage = self._attack_power // 2
            print(
                f"{self._name} stumbles, managing only a weak slash"
                f" at {target.name}!"
            )

        target.take_damage(base_damage)
        return base_damage

    def gain_experience(self, exp: int):
        """Gain experience and restore one poison charge per kill.

        Delegates to the base class for level-up logic, then restores
        1 poison charge (up to the maximum) as a reward for each kill.

        Args:
            exp (int): Experience points awarded.
        """
        super().gain_experience(exp)
        if self._poison_charges < self._max_poison_charges:
            self._poison_charges += 1
            print(
                f"  {self._name} recoats a blade "
                f"({self._poison_charges}/{self._max_poison_charges} charges)"
            )

    def special_ability(self, target=None):
        """Launch a Shadow Strike at terrible personal cost.

        Materialises from darkness for a devastating double-damage strike —
        always fires regardless of current HP.  The downside: burns 15 of
        the rogue's own HP (clamped to 0) and guarantees poison if any
        charges remain (consuming 1 charge).

        Args:
            target (Character, optional): The character to target.
                If None, damage is calculated but not applied.

        Returns:
            int: Amount of damage dealt

        Note:
            Shadow Strike costs 15 HP and deals 2 × attack_power + random(-2, 6).
            Guaranteed poison (+8 damage) if poison charges > 0.

        Example:
            >>> damage = rogue.special_ability(enemy)
            Shadowblade launches a SHADOW STRIKE! (−15 HP)
            The blade was poisoned! Extra damage dealt!
        """
        self._health = max(0, self._health - 15)
        base_damage = self._attack_power * 2 + random.randint(-2, 6)
        print(f"{self._name} launches a SHADOW STRIKE! (\u221215 HP)")
        if self._poison_charges > 0:
            self._poison_charges -= 1
            base_damage += 8
            print("The blade was poisoned! Extra damage dealt!")
        if target:
            target.take_damage(base_damage)
        return base_damage

    def _level_up(self):
        """Level up with rogue-specific bonuses.

        Calls the base level-up (via ``super()``) then expands the poison
        charge capacity by 1 and fully refills to the new maximum.

        Effects:
            - All standard effects via ``super()._level_up()``
            - ``_max_poison_charges`` increases by 1
            - ``_poison_charges`` restored to new maximum
        """
        super()._level_up()
        self._max_poison_charges += 1
        self._poison_charges = self._max_poison_charges
        print(f"{self._name}'s toxin reserves have expanded!")


# ---------------------------------------------------------------------------
# Playable character registry
# ---------------------------------------------------------------------------

# All playable classes defined in this module, in menu display order.
# To add a new class to the base game, define it above and add it here.
PLAYABLE_CLASSES: list[type] = [Warrior, Mage, MagicArcher, Rogue]
