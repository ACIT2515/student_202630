from character_pack import Cleric
from characters import Character, Mage


class TestCleric:
    """Test the Cleric character class.

    Attributes:
        cleric (Cleric): The Cleric instance under test.
        target (Mage): A Mage used as the combat target. Mage has no
            armor, so damage assertions are exact.
    """

    def setup_method(self):
        """Initialise fresh fixtures before each test.

        Attributes:
            cleric (Cleric): Fresh Cleric named "Test Cleric".
            target (Mage): Fresh Mage named "Target". Mage has no armor,
                making damage assertions exact.
        """
        self.cleric = Cleric("Test Cleric")
        self.target = Mage("Target")  # Mage has no armor — damage is exact

    def test_cleric_initialization(self):
        """Test cleric is created with correct starting attributes."""
        assert self.cleric.name == "Test Cleric"
        assert self.cleric.health == 90
        assert self.cleric._attack_power == 4
        assert self.cleric._spell_power == 15

    def test_is_character_subclass(self):
        """Test that Cleric is a subclass of Character."""
        assert isinstance(self.cleric, Character)

    def test_character_type(self):
        """Test character_type property returns correct label."""
        assert self.cleric.character_type == "Cleric"

    def test_resource_info(self):
        """Test resource_info reflects current spell power."""
        assert self.cleric.resource_info == ", SP: 15"

    def test_str_representation(self):
        """Test __str__ includes name, type, level, HP, and spell power."""
        result = str(self.cleric)
        assert "Test Cleric" in result
        assert "Cleric" in result
        assert "Lv.1" in result
        assert "HP: 90/90" in result
        assert "SP: 15" in result

    def test_attack_deals_base_attack_power_damage(self):
        """Test normal attack always deals exactly attack_power damage."""
        initial_health = self.target.health
        damage = self.cleric.attack(self.target)
        assert damage == self.cleric._attack_power
        assert self.target.health == initial_health - damage

    def test_attack_increases_spell_power(self):
        """Test each attack increases spell_power by 1."""
        initial_sp = self.cleric._spell_power
        self.cleric.attack(self.target)
        assert self.cleric._spell_power == initial_sp + 1

    def test_fallback_heals_self(self):
        """Test fallback below 40% heals 5 HP and deals 0 damage."""
        self.cleric._health = 30  # below 40% of 90 (36)
        hp_before = self.cleric.health
        target_before = self.target.health
        initial_sp = self.cleric._spell_power
        damage = self.cleric.attack(self.target)
        assert damage == 0
        assert self.target.health == target_before
        assert self.cleric.health == hp_before + 5
        assert self.cleric._spell_power == initial_sp + 1

    def test_attack_at_40_percent_hp_is_not_fallback(self):
        """Test fallback does not trigger at exactly 40% HP."""
        self.cleric._health = int(self.cleric._max_health * 0.4)  # exactly 36
        hp_before = self.cleric.health
        target_before = self.target.health
        damage = self.cleric.attack(self.target)
        assert damage == self.cleric._attack_power
        assert self.target.health == target_before - damage
        assert self.cleric.health == hp_before

    def test_special_ability_heals_self(self):
        """Test Holy Light heals cleric for spell_power * 2 HP."""
        self.cleric._health = 50
        hp_before = self.cleric.health
        self.cleric.special_ability(self.target)
        expected_heal = min(
            self.cleric._spell_power * 2, self.cleric._max_health - (hp_before - 15)
        )
        assert self.cleric.health == hp_before - 15 + expected_heal

    def test_special_ability_costs_fifteen_hp(self):
        """Test Holy Light costs 15 HP before the heal is applied."""
        self.cleric._health = 70
        self.cleric._spell_power = 0  # isolate the HP cost from healing
        self.cleric.special_ability(self.target)
        assert self.cleric.health == 55

    def test_special_ability_capped_at_max_health(self):
        """Test Holy Light cannot restore HP above max health."""
        self.cleric._health = self.cleric._max_health
        self.cleric.special_ability(self.target)
        assert self.cleric.health <= self.cleric._max_health

    def test_special_ability_returns_zero(self):
        """Test Holy Light returns 0 (no direct damage dealt)."""
        result = self.cleric.special_ability(self.target)
        assert result == 0

    def test_special_ability_deals_zero_damage_to_target(self):
        """Test Holy Light deals 0 damage to the target."""
        initial_health = self.target.health
        self.cleric.special_ability(self.target)
        assert self.target.health == initial_health

    def test_level_up_increases_spell_power(self):
        """Test Cleric-specific level-up bonus adds 5 spell power."""
        initial_sp = self.cleric._spell_power
        self.cleric.gain_experience(50)
        assert self.cleric._spell_power == initial_sp + 5

    def test_level_up_applies_base_stat_gains(self):
        """Test level-up increases level by 1 and restores HP to new max."""
        self.cleric.gain_experience(50)
        assert self.cleric.level == 2
        assert self.cleric.health == self.cleric._max_health

    def test_playable_registered(self):
        """Test Cleric appears in Character's discovered subclasses."""
        assert Cleric in Character.__subclasses__()
