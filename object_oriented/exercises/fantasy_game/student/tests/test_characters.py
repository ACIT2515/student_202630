import pytest

from characters import Character, Mage, MagicArcher, Rogue, Warrior


class TestCharacterAbstract:
    """Test the abstract Character class.

    Verifies that ``Character`` cannot be instantiated directly and that
    concrete subclasses correctly expose all inherited base properties.
    """

    def test_cannot_instantiate_abstract_character(self):
        """Test that Character cannot be instantiated directly."""
        with pytest.raises(TypeError):
            Character("Test")

    def test_character_properties_through_subclass(self):
        """Test Character properties through concrete subclass."""
        warrior = Warrior("Test Warrior")
        assert warrior.name == "Test Warrior"
        assert warrior.health == 120
        assert warrior.level == 1
        assert warrior.is_alive is True


class TestWarrior:
    """Test the Warrior character class.

    Attributes:
        warrior (Warrior): The Warrior instance under test.
        target (Warrior): A Warrior used as the combat target.
    """

    def setup_method(self):
        """Initialise fresh fixtures before each test.

        Attributes:
            warrior (Warrior): Fresh Warrior named "Test Warrior".
            target (Warrior): Fresh Warrior named "Target" used as the attack recipient.
        """
        self.warrior = Warrior("Test Warrior")
        self.target = Warrior("Target")

    def test_warrior_initialization(self):
        """Test warrior is created with correct attributes."""
        assert self.warrior.name == "Test Warrior"
        assert self.warrior.health == 120
        assert self.warrior._attack_power == 15
        assert self.warrior._armor == 5

    def test_get_character_type(self):
        """Test character type is returned correctly."""
        assert self.warrior.character_type == "Warrior"

    def test_get_resource_info_normal(self):
        """Test resource info display."""
        assert self.warrior.resource_info == ", Armor: 5"

    def test_take_damage_with_armor(self):
        """Test damage reduction from armor."""
        initial_health = self.warrior.health
        self.warrior.take_damage(10)  # Should be reduced to 5
        assert self.warrior.health == initial_health - 5

    def test_take_damage_minimum_one(self):
        """Test minimum 1 damage is always applied."""
        initial_health = self.warrior.health
        self.warrior.take_damage(3)  # Should be reduced to 1 after armor
        assert self.warrior.health == initial_health - 1

    def test_special_ability_deals_damage(self):
        """Test berserker rage always deals damage."""
        initial_health = self.target.health
        damage = self.warrior.special_ability(self.target)
        assert damage > 0
        assert self.target.health < initial_health

    def test_special_ability_costs_hp(self):
        """Test berserker rage costs 20 HP."""
        initial_health = self.warrior.health
        self.warrior.special_ability(self.target)
        assert self.warrior.health == initial_health - 20

    def test_special_ability_clamps_hp_to_zero(self):
        """Test berserker rage cannot reduce HP below 0."""
        self.warrior._health = 10
        self.warrior.special_ability(self.target)
        assert self.warrior.health == 0

    def test_attack_normal(self):
        """Test normal attack behavior."""
        initial_health = self.target.health
        damage = self.warrior.attack(self.target)

        assert damage > 0
        assert self.target.health < initial_health

    def test_str_representation(self):
        """Test string representation."""
        result = str(self.warrior)
        assert "Test Warrior" in result
        assert "Warrior" in result
        assert "Lv.1" in result
        assert "HP: 120/120" in result
        assert "Armor: 5" in result

    def test_level_up_armor_bonus(self):
        """Test warrior-specific level-up increases armor by 1."""
        initial_armor = self.warrior._armor
        self.warrior.gain_experience(100)  # Trigger level up
        assert self.warrior._armor == initial_armor + 1


class TestMage:
    """Test the Mage character class.

    Attributes:
        mage (Mage): The Mage instance under test.
        target (Warrior): A Warrior used as the combat target.
    """

    def setup_method(self):
        """Initialise fresh fixtures before each test.

        Attributes:
            mage (Mage): Fresh Mage named "Test Mage".
            target (Warrior): Fresh Warrior named "Target" used as the attack recipient.
        """
        self.mage = Mage("Test Mage")
        self.target = Warrior("Target")

    def test_mage_initialization(self):
        """Test mage is created with correct attributes."""
        assert self.mage.name == "Test Mage"
        assert self.mage.health == 80
        assert self.mage._attack_power == 8
        assert self.mage._spell_power == 20

    def test_get_character_type(self):
        """Test character type is returned correctly."""
        assert self.mage.character_type == "Mage"

    def test_get_resource_info(self):
        """Test resource info display."""
        assert self.mage.resource_info == ", SP: 20"

    def test_attack_above_threshold(self):
        """Test Magic Missile fires when HP above 40% of max (>32)."""
        # Default health 80 > 40% of 80 (32)
        initial_target_health = self.target.health
        damage = self.mage.attack(self.target)
        assert damage > 0
        assert self.target.health < initial_target_health
        assert self.mage.health == 80  # No HP cost for regular attack

    def test_attack_below_threshold(self):
        """Test staff prod fires when HP at or below 40% of max."""
        self.mage._health = 32  # Not > 40% of 80
        damage = self.mage.attack(self.target)
        assert damage == self.mage._attack_power // 2
        assert self.mage._health == 32  # No HP cost

    def test_special_ability_deals_damage(self):
        """Test fireball always deals damage."""
        initial_health = self.target.health
        damage = self.mage.special_ability(self.target)
        assert damage > 0
        assert self.target.health < initial_health

    def test_special_ability_costs_hp(self):
        """Test fireball costs 25 HP."""
        initial_health = self.mage.health
        self.mage.special_ability(self.target)
        assert self.mage.health == initial_health - 25

    def test_special_ability_clamps_hp_to_zero(self):
        """Test fireball cannot reduce HP below 0."""
        self.mage._health = 10
        self.mage.special_ability(self.target)
        assert self.mage.health == 0

    def test_level_up_mage_bonuses(self):
        """Test mage-specific level up bonuses."""
        self.mage._experience = 100  # Trigger level up
        initial_spell_power = self.mage._spell_power
        self.mage.gain_experience(0)
        assert self.mage.level == 2
        assert self.mage._spell_power == initial_spell_power + 8


class TestMagicArcher:
    """Test the MagicArcher character class.

    Attributes:
        archer (MagicArcher): The MagicArcher instance under test.
        target (Warrior): A Warrior used as the combat target.
    """

    def setup_method(self):
        """Initialise fresh fixtures before each test.

        Attributes:
            archer (MagicArcher): Fresh MagicArcher named "Test Archer".
            target (Warrior): Fresh Warrior named "Target" used as the attack recipient.
        """
        self.archer = MagicArcher("Test Archer")
        self.target = Warrior("Target")

    def test_archer_initialization(self):
        """Test archer is created with correct attributes."""
        assert self.archer.name == "Test Archer"
        assert self.archer.health == 90
        assert self.archer._attack_power == 12
        assert self.archer._accuracy == 0.85

    def test_get_character_type(self):
        """Test character type is returned correctly."""
        assert self.archer.character_type == "Magic Archer"

    def test_get_resource_info(self):
        """Test resource info display."""
        assert self.archer.resource_info == ", Acc: 85%"

    def test_attack_above_threshold_no_hp_cost(self):
        """Test enchanted arrow fires above 40% HP with no HP cost."""
        import random

        random.seed(1)  # Ensure hit
        initial_hp = self.archer.health
        self.archer.attack(self.target)
        assert self.archer.health == initial_hp  # No HP cost

    def test_attack_below_threshold(self):
        """Test dagger fallback fires when HP at or below 40% of max."""
        self.archer._health = 36  # Not > 40% of 90
        damage = self.archer.attack(self.target)
        assert damage == self.archer._attack_power // 2
        assert self.archer._health == 36  # No HP cost

    def test_special_ability_deals_damage(self):
        """Test triple shot always deals damage."""
        initial_health = self.target.health
        damage = self.archer.special_ability(self.target)
        expected = (self.archer._attack_power + 5) * 3
        assert damage == expected
        assert self.target.health < initial_health

    def test_special_ability_costs_hp(self):
        """Test triple shot costs 20 HP."""
        initial_hp = self.archer.health
        self.archer.special_ability(self.target)
        assert self.archer.health == initial_hp - 20

    def test_special_ability_clamps_hp_to_zero(self):
        """Test triple shot cannot reduce HP below 0."""
        self.archer._health = 15
        self.archer.special_ability(self.target)
        assert self.archer.health == 0

    def test_special_ability_no_target(self):
        """Test triple shot without target."""
        damage = self.archer.special_ability()
        expected = (self.archer._attack_power + 5) * 3
        assert damage == expected

    def test_level_up_accuracy_bonus(self):
        """Test magic archer-specific level-up improves accuracy by 0.02."""
        initial_accuracy = self.archer._accuracy
        self.archer.gain_experience(100)  # Trigger level up
        assert self.archer._accuracy == pytest.approx(initial_accuracy + 0.02)


class TestRogue:
    """Test the Rogue character class.

    Attributes:
        rogue (Rogue): The Rogue instance under test.
        target (Warrior): A Warrior used as the combat target.
    """

    def setup_method(self):
        """Initialise fresh fixtures before each test.

        Attributes:
            rogue (Rogue): Fresh Rogue named "Test Rogue".
            target (Warrior): Fresh Warrior named "Target" used as the attack recipient.
        """
        self.rogue = Rogue("Test Rogue")
        self.target = Warrior("Target")

    def test_rogue_initialization(self):
        """Test rogue is created with correct attributes."""
        assert self.rogue.name == "Test Rogue"
        assert self.rogue.health == 85
        assert self.rogue._attack_power == 11
        assert self.rogue._max_poison_charges == 5
        assert self.rogue._poison_charges == 5
        assert not hasattr(self.rogue, "_stealth")

    def test_get_character_type(self):
        """Test character type is returned correctly."""
        assert self.rogue.character_type == "Rogue"

    def test_get_resource_info(self):
        """Test resource info shows poison charges only."""
        assert self.rogue.resource_info == ", Poison: 5"

    def test_attack_above_threshold(self):
        """Test full dagger combo fires when HP above 40% of max (>34)."""
        initial_health = self.target.health
        damage = self.rogue.attack(self.target)
        assert damage > 0
        assert self.target.health < initial_health

    def test_attack_below_threshold(self):
        """Test weak slash fires when HP at or below 40% of max."""
        self.rogue._health = 34  # Not > 40% of 85
        damage = self.rogue.attack(self.target)
        assert damage == self.rogue._attack_power // 2

    def test_attack_no_poison_below_threshold(self):
        """Test poison is never applied during weak slash."""
        self.rogue._health = 34
        initial_charges = self.rogue._poison_charges
        self.rogue.attack(self.target)
        assert self.rogue._poison_charges == initial_charges  # Unchanged

    def test_special_ability_deals_damage(self):
        """Test shadow strike always deals damage."""
        initial_health = self.target.health
        damage = self.rogue.special_ability(self.target)
        assert damage > 0
        assert self.target.health < initial_health

    def test_special_ability_costs_hp(self):
        """Test shadow strike costs 15 HP."""
        initial_hp = self.rogue.health
        self.rogue.special_ability(self.target)
        assert self.rogue.health == initial_hp - 15

    def test_special_ability_clamps_hp_to_zero(self):
        """Test shadow strike cannot reduce HP below 0."""
        self.rogue._health = 10
        self.rogue.special_ability(self.target)
        assert self.rogue.health == 0

    def test_special_ability_uses_poison_charge(self):
        """Test shadow strike consumes a poison charge if available."""
        initial_charges = self.rogue._poison_charges
        self.rogue.special_ability(self.target)
        assert self.rogue._poison_charges == initial_charges - 1

    def test_special_ability_no_poison_when_empty(self):
        """Test shadow strike deals base damage when no poison charges."""
        self.rogue._poison_charges = 0
        damage = self.rogue.special_ability(self.target)
        # Base: attack_power * 2 + rand(-2, 6); no +8 poison bonus
        assert damage <= self.rogue._attack_power * 2 + 6
        assert self.rogue._poison_charges == 0  # No charge to consume

    def test_gain_experience_restores_charge(self):
        """Test that gaining XP (on kill) restores 1 poison charge."""
        self.rogue._poison_charges = 2
        self.rogue.gain_experience(10)
        assert self.rogue._poison_charges == 3

    def test_gain_experience_does_not_exceed_max_charges(self):
        """Test that replenishment is capped at max charges."""
        self.rogue._poison_charges = 5  # already full
        self.rogue.gain_experience(10)
        assert self.rogue._poison_charges == 5

    def test_level_up_charges_bonus(self):
        """Test rogue-specific level-up expands max poison charges by 1."""
        initial_max = self.rogue._max_poison_charges
        self.rogue.gain_experience(100)  # Trigger level up
        assert self.rogue._max_poison_charges == initial_max + 1
        assert self.rogue._poison_charges == self.rogue._max_poison_charges


class TestCharacterBaseFeatures:
    """Test base Character class features through concrete implementations.

    Attributes:
        character (Warrior): A Warrior used as a concrete stand-in for
            the abstract ``Character`` interface.
    """

    def setup_method(self):
        """Initialise fresh fixtures before each test.

        Attributes:
            character (Warrior): Fresh Warrior named "Test Character".
        """
        self.character = Warrior("Test Character")

    def test_take_damage(self):
        """Test basic damage application."""
        initial_health = self.character.health
        self.character.take_damage(10)
        # Warrior has armor, so actual damage will be less
        assert self.character.health < initial_health

    def test_take_damage_death(self):
        """Test character death."""
        self.character.take_damage(200)  # More than max health
        assert self.character.health == 0
        assert self.character.is_alive is False

    def test_heal(self):
        """Test healing."""
        self.character.take_damage(50)
        damaged_health = self.character.health
        self.character.heal(20)
        assert self.character.health > damaged_health

    def test_heal_max_limit(self):
        """Test healing cannot exceed max health."""
        max_health = self.character._max_health
        self.character.heal(50)
        assert self.character.health == max_health

    def test_gain_experience(self):
        """Test experience gain."""
        initial_exp = self.character._experience
        self.character.gain_experience(50)
        assert self.character._experience == initial_exp + 50

    def test_character_comparisons(self):
        """Test operator overloading for equality and less-than."""
        char1 = Warrior("Hero A")
        char2 = Warrior("Hero B")

        # Give char1 less health
        char1.take_damage(50)
        assert char1 < char2  # char1 has lower health

        # Test built-in min
        weakest = min([char1, char2])
        assert weakest == char1

        # Test equality (based on name for our implementation)
        char3 = Warrior("Hero A")
        assert char1 == char3
        assert char1 != char2

    def test_level_up(self):
        """Test leveling up."""
        self.character.gain_experience(100)  # Should trigger level up
        assert self.character.level == 2
        assert self.character._max_health == 140  # Base 120 + 20
        assert self.character.health == 140  # Restored to max
        assert self.character._attack_power == 20  # Base 15 + 5

    def test_is_alive_property(self):
        """Test is_alive property."""
        assert self.character.is_alive is True
        self.character._health = 0
        assert self.character.is_alive is False
