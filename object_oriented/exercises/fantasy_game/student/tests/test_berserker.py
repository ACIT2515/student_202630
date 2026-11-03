from character_pack import Berserker
from characters import Character, Mage


class TestBerserker:
    """Test the Berserker character class.

    Attributes:
        berserker (Berserker): The Berserker instance under test.
        target (Mage): A Mage used as the combat target. Mage has no
            armor, so damage assertions are exact.
    """

    def setup_method(self):
        """Initialise fresh fixtures before each test.

        Attributes:
            berserker (Berserker): Fresh Berserker named "Test Berserker".
            target (Mage): Fresh Mage named "Target". Mage has no armor,
                making damage assertions exact.
        """
        self.berserker = Berserker("Test Berserker")
        self.target = Mage("Target")  # Mage has no armor — damage is exact

    def test_berserker_initialization(self):
        """Test berserker is created with correct starting attributes."""
        assert self.berserker.name == "Test Berserker"
        assert self.berserker.health == 120
        assert self.berserker._attack_power == 8
        assert self.berserker._rage == 0

    def test_is_character_subclass(self):
        """Test that Berserker is a subclass of Character."""
        assert isinstance(self.berserker, Character)

    def test_character_type(self):
        """Test character_type property returns correct label."""
        assert self.berserker.character_type == "Berserker"

    def test_resource_info(self):
        """Test resource_info reflects current rage."""
        assert self.berserker.resource_info == ", Rage: 0"

    def test_str_representation(self):
        """Test __str__ includes name, type, level, HP, and rage."""
        result = str(self.berserker)
        assert "Test Berserker" in result
        assert "Berserker" in result
        assert "Lv.1" in result
        assert "HP: 120/120" in result
        assert "Rage: 0" in result

    def test_attack_deals_damage(self):
        """Test normal attack deals damage equal to attack_power + rage."""
        initial_health = self.target.health
        damage = self.berserker.attack(self.target)
        assert damage == self.berserker._attack_power  # rage starts at 0
        assert self.target.health == initial_health - damage

    def test_attack_increases_rage(self):
        """Test each attack increases rage by 2."""
        self.berserker.attack(self.target)
        assert self.berserker._rage == 2

    def test_attack_damage_scales_with_rage(self):
        """Test successive attacks deal increasing damage as rage grows."""
        self.berserker._rage = 10
        initial_health = self.target.health
        damage = self.berserker.attack(self.target)
        assert damage == self.berserker._attack_power + 10
        assert self.target.health == initial_health - damage

    def test_fallback_double_strike(self):
        """Test frenzied double-strike hits twice below 40% HP."""
        self.berserker._health = int(self.berserker._max_health * 0.4) - 1
        initial_health = self.target.health
        damage = self.berserker.attack(self.target)
        expected_single = self.berserker._attack_power  # rage was 0 before the call
        assert damage == expected_single * 2
        assert self.target.health == initial_health - expected_single * 2
        assert self.berserker._rage == 4

    def test_attack_at_40_percent_hp_is_not_fallback(self):
        """Test fallback does not trigger at exactly 40% HP."""
        self.berserker._health = int(self.berserker._max_health * 0.4)
        initial_health = self.target.health
        damage = self.berserker.attack(self.target)
        assert damage == self.berserker._attack_power
        assert self.target.health == initial_health - damage
        assert self.berserker._rage == 2

    def test_special_ability_deals_triple_attack_power(self):
        """Test Bloodlust deals attack_power * 3 damage."""
        initial_health = self.target.health
        damage = self.berserker.special_ability(self.target)
        assert damage == self.berserker._attack_power * 3
        assert self.target.health == initial_health - damage

    def test_special_ability_costs_twenty_hp(self):
        """Test Bloodlust costs 20 HP."""
        initial_health = self.berserker.health
        self.berserker.special_ability(self.target)
        assert self.berserker.health == initial_health - 20

    def test_special_ability_resets_rage(self):
        """Test Bloodlust resets rage to 0."""
        self.berserker._rage = 14
        self.berserker.special_ability(self.target)
        assert self.berserker._rage == 0

    def test_special_ability_clamps_hp_to_one(self):
        """Test Bloodlust cannot reduce HP below 1."""
        self.berserker._health = 10
        self.berserker.special_ability(self.target)
        assert self.berserker.health == 1

    def test_level_up_applies_base_stat_gains(self):
        """Test level-up increases level by 1 and restores HP to new max."""
        self.berserker.gain_experience(50)
        assert self.berserker.level == 2
        assert self.berserker.health == self.berserker._max_health

    def test_playable_registered(self):
        """Test Berserker appears in Character's discovered subclasses."""
        assert Berserker in Character.__subclasses__()
