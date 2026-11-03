"""Last Stand: Warlord's Siege — Boss Wave Survival Game.

The player assembles a team of 3 heroes and must survive 3 escalating
waves of computer-controlled enemies, culminating in a boss fight against
Warlord Groth.

Objective: Defeat all three waves without losing your entire team.

Waves:
    1  — A small scouting force (2 enemies drawn from a light roster)
    2  — A stronger warband (2–3 enemies from the full roster)
    3  — The Warlord Rises: Warlord Groth (Boss) + 1–2 reinforcements

Player controls: Choose an action (Attack / Special Ability / Wait) and a
target for every living hero each round. Enemies act automatically after
all heroes have taken their turn, utilizing a "smart AI" that targets the
weakest hero via Python's built-in ``min()`` function (enabled by the
``Character.__lt__`` operator overload).

Classes:
    Boss: A heavily armoured boss enemy derived from Warrior.
    WaveSurvivalGame: Manages the full game loop, team building, and waves.

Usage:
    Run this module directly to start a new game:
        python warlords_siege.py
"""

import random

from characters import Character, Enemy, Mage, MagicArcher, Rogue, Warrior
from utility import describe, prompt_int, separator


class Boss(Enemy, Warrior):
    """A fearsome boss enemy with boosted Warrior stats.

    Combines the ``Enemy`` mixin (no XP gain via MRO) with the full
    ``Warrior`` class (armor, berserker strike).  Demonstrates multiple
    inheritance and MRO::

        Boss → Enemy → Warrior → Character → ABC → object

    ``gain_experience`` resolves to ``Enemy``'s no-op because ``Enemy``
    comes first in the base-class list.  All combat behaviour — ``attack``,
    ``special_ability``, armor damage reduction — is inherited from
    ``Warrior``.

    Starting stats: HP 250, attack_power 25, armor 8.

    Args:
        name (str): The boss's name.

    Example:
        >>> boss = Boss("Warlord Groth")
        >>> boss.health
        250
        >>> boss.character_type
        'Boss'
        >>> isinstance(boss, Enemy)
        True
        >>> isinstance(boss, Warrior)
        True
    """

    def __init__(self, name: str):
        super().__init__(name)
        self._max_health = 250
        self._health = 250
        self._attack_power = 25
        self._armor = 8

    @property
    def character_type(self) -> str:
        """Returns:
        str: Always ``'Boss'``.
        """
        return "Boss"


class WaveSurvivalGame:
    """Manages the Last Stand: Warlord's Siege game loop.

    The player builds a team of three heroes, then faces three waves of
    increasingly dangerous computer-controlled enemies.  Each round, every
    living hero acts in sequence (player chooses action and target), then
    every living enemy attacks automatically.  A partial heal is awarded
    after waves 1 and 2.  The game ends in victory when all three waves
    are cleared, or in defeat when all heroes fall.

    Attributes:
        _player_team (list[Character]): Heroes controlled by the player.
        _enemy_team (list[Character]): Enemies for the current wave.
        _wave_number (int): Current wave index (1–3).

    Example:
        >>> game = WaveSurvivalGame()
        >>> game.run()  # Starts the interactive session
    """

    # Single master name pool used for any enemy type regardless of class
    _ENEMY_NAMES: list[str] = [
        "Iron Guard",
        "Bloodaxe",
        "Stone Fist",
        "Grim Vanguard",
        "Scar",
        "Hex Witch",
        "Bone Seer",
        "Void Caster",
        "Shadow Weaver",
        "Ash Darkness",
        "Poacher",
        "Black Bolt",
        "Skull",
        "Venom",
        "Thug",
        "Cutthroat",
        "Shade Runner",
        "Viper",
        "Night Stalker",
        "Imp",
    ]

    _WAVE_TITLES: dict[int, list[str]] = {
        1: [
            "The Vanguard",
            "The Scouting Party",
            "The First Wave",
            "Advance Skirmishers",
        ],
        2: [
            "The Dark Company",
            "The War Host",
            "The Marauders",
            "The Iron Warband",
        ],
    }

    def __init__(self):
        self._player_team: list[Character] = []
        self._enemy_team: list[Character] = []
        self._wave_number = 0
        # Character.__subclasses__() is a built-in Python method that returns
        # a list of every class that directly inherits from Character.
        # It is called here (inside __init__, not at import time) so any classes
        # defined in other modules are included, as long as they are imported
        # before the game is started.
        #
        # enumerate(..., 1) walks the list and pairs each class with a counter
        # that starts at 1:  i=1 → Warrior,  i=2 → Mage,  i=3 → MagicArcher …
        #
        # For each pair we store one entry in the dict:
        #   key   → str(i)        the menu number as a string: "1", "2", …
        #   value → (label, cls)  a tuple of (display name, the class itself)
        #
        # cls("_") creates a temporary instance just to read its character_type
        # property (e.g. "Magic Archer"). The instance is discarded immediately.
        #
        # Example with the base four classes:
        #   {"1": ("Warrior", Warrior), "2": ("Mage", Mage),
        #    "3": ("Magic Archer", MagicArcher), "4": ("Rogue", Rogue)}
        self._character_options: dict[str, tuple[str, type]] = {
            str(i): (cls("_").character_type, cls)
            for i, cls in enumerate(Character.__subclasses__(), 1)
        }
        all_classes = Character.__subclasses__()
        self._wave_pools: dict[int, list[type]] = {
            1: [Warrior, MagicArcher],
            2: all_classes,
            3: all_classes,  # plus Boss — see _build_wave_enemies
        }

    def _print_team_status(self) -> None:
        """Print the current HP and resource state for both teams.

        Prints a formatted block showing every hero and every enemy,
        with ``[DEFEATED]`` replacing the stat line for fallen characters.
        """
        print("\n" + "-" * 60)
        print("YOUR HEROES")
        print("-" * 60)
        for hero in self._player_team:
            if hero.is_alive:
                print(f"  {hero}")
            else:
                print(f"  {hero.name} — [DEFEATED]")

        print("\nENEMIES")
        print("-" * 60)
        for enemy in self._enemy_team:
            if enemy.is_alive:
                print(f"  {enemy}")
            else:
                print(f"  {enemy.name} — [DEFEATED]")
        print("-" * 60)

    def _print_action_result(self) -> None:
        """Print both teams' state after a combat action.

        Delegates to ``_print_team_status`` with a header label so the
        player can see the immediate effect of each action.
        """
        print("  ── State after action ──")
        self._print_team_status()

    def _all_enemies_defeated(self) -> bool:
        """Check whether every enemy in the current wave has fallen.

        Returns:
            bool: ``True`` if all enemies have 0 HP, ``False`` otherwise.
        """
        return all(not e.is_alive for e in self._enemy_team)

    def _all_heroes_defeated(self) -> bool:
        """Check whether every hero on the player's team has fallen.

        Returns:
            bool: ``True`` if all heroes have 0 HP, ``False`` otherwise.
        """
        return all(not h.is_alive for h in self._player_team)

    def _select_enemy_target(self) -> Character | None:
        """Ask the player to pick a living target from the enemy team.

        Displays a numbered list of all living enemies and reads a valid
        integer choice from stdin.

        Returns:
            Character | None: The chosen enemy, or ``None`` if no living
                enemies remain.
        """
        alive = [e for e in self._enemy_team if e.is_alive]
        if not alive:
            return None
        print("  Choose a target:")
        for i, enemy in enumerate(alive, start=1):
            print(f"    [{i}] {enemy}")
        choice = prompt_int("  Target: ", 1, len(alive))
        return alive[choice - 1]

    def _hero_act(self, hero: Character) -> None:
        """Handle one hero's turn, letting the player choose an attack level.

        Presents four options and reads the player's choice:

        * ``[1]`` Conservative Strike — ``attack_power // 2``, no HP cost,
          always available.
        * ``[2]`` Attack — full-power ``attack()``, requires HP > 40 % of max.
        * ``[3]`` Special Ability — maximum power ``special_ability()``,
          costs the hero HP, requires HP > 40 % of max.
        * ``[4]`` Wait — skip this hero's turn.

        If the player picks level 2 or 3 while the hero is at or below the
        40 % threshold, the action is automatically downgraded to level 1 and
        the player is notified.

        Args:
            hero (Character): The hero whose turn is being resolved.
        """
        threshold = hero._max_health * 0.40
        above_threshold = hero._health > threshold

        print(f"\n  {hero.name}'s turn  ({hero.character_type})")
        if isinstance(hero, Warrior):
            print(f"    (Armor: {hero._armor} — reduces all incoming damage)")
        print(
            "    [1] Conservative Strike — half-power cautious attack, always available"
        )
        print(f"    [2] Attack              — {describe(hero.attack)}")
        print(f"    [3] Special Ability     — {describe(hero.special_ability)}")
        print("    [4] Wait (skip turn)")
        action = prompt_int("  Action: ", 1, 4)

        if action == 4:
            print(f"  {hero.name} waits...")
            return

        target = self._select_enemy_target()
        if target is None:
            return

        # Auto-downgrade: levels 2 and 3 both require HP above the 40 % threshold
        if action in (2, 3) and not above_threshold:
            print(
                f"  {hero.name} is too injured for that "
                f"— falling back to a conservative strike!"
            )
            action = 1

        target_hp_before = target.health
        hero_hp_before = hero.health

        if action == 1:
            damage = hero._attack_power // 2
            print(f"  {hero.name} makes a cautious strike at {target.name}!")
            target.take_damage(damage)
        elif action == 2:
            hero.attack(target)
        else:  # action == 3
            hero.special_ability(target)

        target_hp_lost = target_hp_before - target.health
        if target_hp_lost > 0:
            print(
                f"  → {target.name}: {target_hp_before} HP"
                f" → {target.health} HP (−{target_hp_lost})"
            )

        hero_hp_lost = hero_hp_before - hero.health
        if hero_hp_lost > 0:
            print(
                f"  → {hero.name}: {hero_hp_before} HP"
                f" → {hero.health} HP (−{hero_hp_lost})"
            )

        self._print_action_result()

        if not target.is_alive:
            print(f"  *** {target.name} has been defeated! ***")
            if isinstance(target, Enemy):  # only enemies award XP
                hero.gain_experience(50)
                print(f"  {hero.name} gains 50 XP  (total: {hero._experience} XP)")

    def _enemy_turn(self) -> None:
        """Resolve the enemy phase — every living enemy attacks once.

        Each enemy uses a "smart AI" to find the most vulnerable target,
        picking the living hero with the lowest HP using ``min(alive_heroes)``.
        There is a 25 % chance the enemy uses its ``special_ability`` instead
        of a normal ``attack``. Defeated heroes are removed from the target
        pool immediately so subsequent enemies cannot attack a corpse.
        """
        alive_heroes = [h for h in self._player_team if h.is_alive]
        for enemy in self._enemy_team:
            if not enemy.is_alive or not alive_heroes:
                continue

            target = min(alive_heroes)
            print(
                f"\n  {enemy.name} ({enemy.character_type}) ruthlessly"
                f" targets the weakest hero: {target.name}!"
            )

            hp_before = target.health
            # 25 % chance to use special ability instead of normal attack
            if random.random() < 0.25:
                enemy.special_ability(target)
            else:
                enemy.attack(target)

            hp_lost = hp_before - target.health
            if hp_lost > 0:
                print(
                    f"  → {target.name}: {hp_before} HP → {target.health} HP (−{hp_lost})"
                )

            self._print_action_result()

            if not target.is_alive:
                print(f"  *** {target.name} has fallen! ***")
                alive_heroes.remove(target)

            input("  [Press Enter to continue...]")

    def _spawn_enemy(self, cls: type) -> Character:
        """Create one enemy of the given class with a random name.

        Draws a name from the shared ``_ENEMY_NAMES`` pool that is not
        already in use by another enemy on the current team.  Falls back
        to a generic ``ClassName N`` label if all names are taken.

        Args:
            cls (type): The character subclass to instantiate.

        Returns:
            Character: A freshly created enemy of the requested type.
        """
        used = {e.name for e in self._enemy_team}
        available = [n for n in self._ENEMY_NAMES if n not in used]
        fallback = f"{cls.__name__} {len(self._enemy_team) + 1}"
        name = random.choice(available) if available else fallback
        return cls(name)

    def _build_wave_enemies(self) -> None:
        """Populate ``_enemy_team`` for the current wave.

        Clears the enemy list then fills it according to wave rules:

        * Wave 1: 2 enemies drawn from the light roster (Warrior / MagicArcher).
        * Wave 2: 2–3 enemies drawn from the full four-class roster.
        * Wave 3: Warlord Groth (Boss) is always present, plus 1–2 random
          reinforcements drawn from the full roster.

        The exact composition varies each run so no two games are identical.
        """
        self._enemy_team = []
        pool = self._wave_pools[self._wave_number]

        if self._wave_number == 1:
            count = 2
        elif self._wave_number == 2:
            count = random.randint(2, 3)
        else:
            # Wave 3: boss is guaranteed; add 1–2 random reinforcements
            self._enemy_team.append(Boss("Warlord Groth"))
            for _ in range(random.randint(1, 2)):
                self._enemy_team.append(self._spawn_enemy(random.choice(pool)))
            return

        chosen_types = random.choices(pool, k=count)
        for cls in chosen_types:
            self._enemy_team.append(self._spawn_enemy(cls))

    def _wave_intro(self) -> None:
        """Print the wave introduction banner and wait for the player.

        Displays the wave title, lists every enemy with their class
        description, then blocks on an Enter keypress so the player can
        read the information before combat begins.
        """
        separator()
        if self._wave_number == 3:
            title = "WAVE 3 — *** THE WARLORD RISES ***"
        else:
            wave_title = random.choice(self._WAVE_TITLES[self._wave_number])
            title = f"WAVE {self._wave_number} — {wave_title}"
        print(f"  {title}")
        print("  Enemies:")
        for enemy in self._enemy_team:
            print(f"    • {enemy}")
            print(f"      {describe(type(enemy))}")
        separator()
        input("  Press Enter when you are ready...")

    def _run_wave(self) -> bool:
        """Execute one full wave of combat.

        Increments the wave counter, builds the enemy team, shows the
        intro banner, then runs the round loop until either all enemies
        are defeated or all heroes have fallen.  Awards a partial heal
        (25 % of max HP) to surviving heroes after waves 1 and 2.

        Returns:
            bool: ``True`` if at least one hero survived the wave;
                ``False`` if the entire player team was defeated.
        """
        self._wave_number += 1
        self._build_wave_enemies()
        self._wave_intro()

        levels_before = {h.name: h.level for h in self._player_team}
        round_num = 1
        while not self._all_enemies_defeated() and not self._all_heroes_defeated():
            print(f"\n{'~'*60}")
            print(f"  Round {round_num}")
            self._print_team_status()

            # --- Player phase: every living hero acts once ---
            print("\n== HERO PHASE ==")
            for hero in self._player_team:
                if not hero.is_alive:
                    continue
                if self._all_enemies_defeated():
                    break
                self._hero_act(hero)

            if self._all_enemies_defeated():
                break

            # --- Enemy phase: every living enemy attacks once ---
            print("\n== ENEMY PHASE ==")
            self._enemy_turn()

            round_num += 1

        if self._all_heroes_defeated():
            return False

        separator()
        print(f"  Wave {self._wave_number} cleared!")
        separator()

        levelled_up = [
            h
            for h in self._player_team
            if h.is_alive and h.level > levels_before[h.name]
        ]
        if levelled_up:
            print("  LEVEL UP SUMMARY")
            for hero in levelled_up:
                old = levels_before[hero.name]
                print(f"    {hero.name}: Lv.{old} → Lv.{hero.level}" f"  — {hero}")
            print()

        # Partial heal between waves (not after the final wave)
        if self._wave_number < 3:
            print("  Your heroes rest briefly and recover 25 % of their max HP.\n")
            for hero in self._player_team:
                if hero.is_alive:
                    hero.heal(hero._max_health // 4)

        return True

    def _build_player_team(self) -> None:
        """Interactively assemble the player's team of three heroes.

        Prompts for a name and class choice for each of the three hero
        slots, instantiates the chosen ``Character`` subclass, and
        appends it to ``_player_team``.  Prints each hero's attack and
        special ability descriptions after creation.
        """
        num_options = len(self._character_options)
        print("\nAssemble your team of 3 heroes.")
        print("Available classes:")
        for key, (class_name, klass) in self._character_options.items():
            desc = describe(klass)
            print(f"  [{key}] {class_name} — {desc}")
        print()

        for slot in range(1, 4):
            print(f"Hero slot {slot}:")
            raw_name = input("  Name (leave blank for a default): ").strip()
            name = raw_name if raw_name else f"Hero {slot}"
            cls_key = str(prompt_int(f"  Class [1-{num_options}]: ", 1, num_options))
            class_name, cls = self._character_options[cls_key]
            hero = cls(name)
            self._player_team.append(hero)
            print(f"  → {hero.name} the {hero.character_type} joins your team!")
            print(f"     Attack:  {describe(hero.attack)}")
            print(f"     Special: {describe(hero.special_ability)}\n")

    def run(self) -> None:
        """Start and run a complete game session.

        Prints the title screen and rules, calls ``_build_player_team``,
        then iterates through all three waves via ``_run_wave``.  Prints
        a victory or defeat message when the session ends.

        Example:
            >>> game = WaveSurvivalGame()
            >>> game.run()
        """
        separator()
        print("  LAST STAND: WARLORD'S SIEGE")
        print("  Survive three waves of enemies and defeat Warlord Groth.")
        print()
        print("  HOW TO PLAY")
        print("  • Each round your heroes act first — pick an attack level or Wait.")
        print(
            "  •   [1] Conservative Strike — half-power, no HP cost, always available."
        )
        print(
            "  •   [2] Attack              — full power, requires HP above 40 % of max."
        )
        print("  •   [3] Special Ability     — maximum power, costs your hero HP.")
        print(
            "  • If your hero is below 40 % HP, higher levels downgrade automatically."
        )
        print("  • Then the enemy team retaliates automatically.")
        print("  • Defeat all enemies in a wave to advance.")
        print("  • You receive a partial heal between waves.")
        print("  • Lose if all your heroes fall.")
        separator()

        self._build_player_team()

        for _ in range(3):
            survived = self._run_wave()
            if not survived:
                separator()
                print("  GAME OVER")
                print("  Your heroes have fallen. The Warlord's forces prevail.")
                separator()
                return

        separator()
        print("  VICTORY!")
        print("  You have defeated Warlord Groth and saved the realm!")
        print()
        print("  Surviving heroes:")
        for hero in self._player_team:
            if hero.is_alive:
                print(f"    {hero}")
        separator()


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    game = WaveSurvivalGame()
    game.run()
