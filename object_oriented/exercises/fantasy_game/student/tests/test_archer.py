from character_pack import Archer
from characters import Character, Mage


class TestArcher:
    """Test the Archer character class.

    Attributes:
        archer (Archer): The Archer instance under test.
        target (Mage): A Mage used as the combat target. Mage has no
            armor, so damage assertions are exact.
    """

    def setup_method(self):
        """Initialise fresh fixtures before each test.

        Attributes:
            archer (Archer): Fresh Archer named "Test Archer".
            target (Mage): Fresh Mage named "Target". Mage has no armor,
                making damage assertions exact.
        """
        self.archer = Archer("Test Archer")
        self.target = Mage("Target")  # Mage has no armor — damage is exact

    def test_archer_initialization(self):
        """Test archer is created with correct starting attributes."""
        assert self.archer.name == "Test Archer"
        assert self.archer.health == 80
        assert self.archer._attack_power == 15
        assert self.archer._arrows == 5

    def test_is_character_subclass(self):
        """Test that Archer is a subclass of Character."""
        assert isinstance(self.archer, Character)

    def test_character_type(self):
        """Test character_type property returns correct label."""
        assert self.archer.character_type == "Archer"

    def test_resource_info(self):
        """Test resource_info reflects current arrow count."""
        assert self.archer.resource_info == ", Arrows: 5"

    def test_str_representation(self):
        """Test __str__ includes name, type, level, HP, and arrows."""
        result = str(self.archer)
        assert "Test Archer" in result
        assert "Archer" in result
        assert "Lv.1" in result
        assert "HP: 80/80" in result
        assert "Arrows: 5" in result

    def test_attack_with_arrows_deals_attack_power_damage(self):
        """Test normal attack deals attack_power damage when arrows available."""
        initial_health = self.target.health
        damage = self.archer.attack(self.target)
        assert damage == self.archer._attack_power
        assert self.target.health == initial_health - damage

    def test_attack_consumes_arrow(self):
        """Test each normal attack reduces arrow count by 1."""
        initial_arrows = self.archer._arrows
        self.archer.attack(self.target)
        assert self.archer._arrows == initial_arrows - 1

    def test_attack_no_arrows_deals_dagger_damage(self):
        """Test attack with no arrows deals the fixed 5 dagger damage."""
        self.archer._arrows = 0
        damage = self.archer.attack(self.target)
        assert damage == 5

    def test_attack_no_arrows_does_not_go_negative(self):
        """Test arrow count cannot go below 0 when attacking without arrows."""
        self.archer._arrows = 0
        self.archer.attack(self.target)
        assert self.archer._arrows == 0

    def test_attack_at_40_percent_hp_is_not_fallback(self):
        """Test fallback does not trigger at exactly 40% HP."""
        self.archer._health = int(self.archer._max_health * 0.4)  # exactly 32
        initial_health = self.target.health
        damage = self.archer.attack(self.target)
        assert damage == self.archer._attack_power
        assert self.target.health == initial_health - damage

    def test_fallback_miss_deals_zero_damage(self, monkeypatch):
        """Test fallback below 40% can miss and deal 0 damage."""
        self.archer._health = int(self.archer._max_health * 0.4) - 1  # below 40%
        initial_health = self.target.health
        initial_arrows = self.archer._arrows
        monkeypatch.setattr("character_pack.random.random", lambda: 0.1)
        damage = self.archer.attack(self.target)
        assert damage == 0
        assert self.target.health == initial_health
        assert self.archer._arrows == initial_arrows

    def test_fallback_hit_deals_normal_damage(self, monkeypatch):
        """Test fallback below 40% can still hit for normal arrow damage."""
        self.archer._health = int(self.archer._max_health * 0.4) - 1  # below 40%
        initial_health = self.target.health
        initial_arrows = self.archer._arrows
        monkeypatch.setattr("character_pack.random.random", lambda: 0.9)
        damage = self.archer.attack(self.target)
        assert damage == self.archer._attack_power
        assert self.target.health == initial_health - damage
        assert self.archer._arrows == initial_arrows - 1

    def test_special_ability_restores_three_arrows(self):
        """Test Restock adds 3 arrows."""
        self.archer._arrows = 1
        self.archer.special_ability()
        assert self.archer._arrows == 4

    def test_special_ability_costs_ten_hp(self):
        """Test Restock costs 10 HP."""
        initial_health = self.archer.health
        self.archer.special_ability()
        assert self.archer.health == initial_health - 10

    def test_special_ability_clamps_hp_to_one(self):
        """Test Restock cannot reduce HP below 1."""
        self.archer._health = 5
        self.archer.special_ability()
        assert self.archer.health == 1

    def test_special_ability_returns_zero(self):
        """Test Restock returns 0 (no direct damage dealt)."""
        result = self.archer.special_ability(self.target)
        assert result == 0

    def test_level_up_adds_two_arrows(self):
        """Test Archer-specific level-up bonus adds 2 arrows."""
        initial_arrows = self.archer._arrows
        self.archer.gain_experience(50)
        assert self.archer._arrows == initial_arrows + 2

    def test_level_up_applies_base_stat_gains(self):
        """Test level-up increases level by 1 and restores HP to new max."""
        self.archer.gain_experience(50)
        assert self.archer.level == 2
        assert self.archer.health == self.archer._max_health

    def test_playable_registered(self):
        """Test Archer appears in Character's discovered subclasses."""
        assert Archer in Character.__subclasses__()
