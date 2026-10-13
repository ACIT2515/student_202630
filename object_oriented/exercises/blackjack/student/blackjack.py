#!/usr/bin/env python3
from enum import Enum

from cards import Card, Deck

BLACKJACK = 21


class GameStatus(Enum):
    """Enum representing the possible game status outcomes."""

    PLAYER_WIN = "player_win"
    DEALER_WIN = "dealer_win"
    PUSH = "push"
    CONTINUE = "continue"


class BlackjackHand:
    """
    Represents a hand of cards in Blackjack.

    A hand manages cards and calculates their value according to Blackjack rules.

    Attributes:
        _cards (list): Protected list of Card objects in the hand
    """

    def __init__(self, card: Card):
        """
        Initialize a new hand with the first card.

        Args:
            card (Card): The first card to add to the hand
        """
        self._cards = [card]

    def add_card(self, card: Card):
        """
        Add a card to the hand.

        Args:
            card (Card): The card to add to the hand
        """
        self._cards.append(card)

    @staticmethod
    def __get_card_value(card: Card) -> int:
        """
        Get the Blackjack value of a card.

        This interprets card ranks according to Blackjack rules.
        Static method since it doesn't depend on instance or class state.
        Private because it is only used temporarily when calculating hand

        Args:
            card (Card): The card to evaluate

        Returns:
            int: The Blackjack value (10 for face cards, 11 for Ace,
                 face value for number cards)
        """
        if 10 < card.rank_value < 14:
            # Card is 10, Jack, Queen, or King
            return 10

        elif card.rank_value == 14:  # Card is an Ace
            return 11

        else:  # Card is 2 through 9
            return card.rank_value

    @property
    def value(self) -> int:
        """
        Calculate the total value of the hand for Blackjack.

        Aces are counted as 11 unless that would cause a bust, in which case
        they are counted as 1. Multiple aces are handled correctly.

        Returns:
            int: The total value of the hand
        """
        value = 0
        num_aces = 0

        # Calculate initial value (all Aces count as 11)
        for card in self._cards:
            value += self.__get_card_value(card)
            if card.rank == "Ace":
                num_aces += 1

        # Adjust for Aces if over BLACKJACK
        while value > BLACKJACK and num_aces > 0:
            value -= 10  # Convert one Ace from 11 to 1
            num_aces -= 1

        return value

    @property
    def is_bust(self) -> bool:
        """
        Check if the hand has busted (exceeded 21).

        Returns:
            bool: True if hand value exceeds 21, False otherwise
        """
        return self.value > BLACKJACK

    @property
    def cards(self) -> list[Card]:
        """
        Get the list of cards in the hand.

        Returns:
            list[Card]: List of Card objects
        """
        return self._cards.copy()


class Player:
    """
    Represents a player in Blackjack.

    A player has a name and a hand. This class handles player identity
    and provides methods to interact with their hand.

    Attributes:
        name (str): The player's name
        _hand (Hand): The player's hand of cards
    """

    def __init__(self, name: str, is_dealer: bool):
        """
        Initialize a new player.

        Args:
            name (str): The player's name
            is_dealer (bool): True if this player is the dealer, False otherwise
        """
        self.name = name
        self._is_dealer = is_dealer
        self._hand = None

    @property
    def hand(self) -> BlackjackHand:
        """
        Get the player's hand.

        Returns:
            Hand: The player's hand
        """
        if not self._hand:
            raise ValueError("Player's hand has not been created")

        return self._hand

    @property
    def is_dealer(self) -> bool:
        """
        Check if this player is the dealer.

        Returns:
            bool: True if this player is the dealer, False otherwise
        """
        return self._is_dealer

    def receive_card(self, card: Card):
        """
        Receive a card and add it to the hand, creating the hand if it
        is the first card.

        Args:
            card (Card): The card to receive
        """
        if self._hand:
            self._hand.add_card(card)
        else:
            self._hand = BlackjackHand(card)

    def show_hand(self, initial_reveal: bool = False) -> str:
        """
        Return a string representation of the player's hand.
        If dealer and initial_reveal is True, hide the second card.

        Args:
            initial_reveal (bool): If True and player is dealer, hide second card

        Returns:
            str: String representation of the hand
        """
        if self._hand is None:
            return ""

        cards = self._hand.cards
        if self._is_dealer and initial_reveal:
            # Show first card, hide second
            return f"{cards[0]}\n[HIDDEN CARD]"

        return "\n".join(str(card) for card in cards)


class BlackjackGame:
    """
    Manages a game of Blackjack.

    Attributes:
        _deck (Deck): The deck of cards for the game
        _player (Player): The player in the game
        _dealer (Player): The dealer
    """

    def __init__(self, player_name: str):
        """Initialize a new Blackjack game.

        Args:
            player_name (str): The name of the player
        """
        self._deck = Deck()
        self._deck.shuffle()
        self._player = Player(player_name, is_dealer=False)
        self._dealer = Player("Dealer", is_dealer=True)

    def deal_initial_cards(self):
        """
        Deal the initial two cards to both player and dealer.

        Cards are dealt alternately: one to player, one to dealer, repeated twice.
        This follows standard casino dealing procedure.
        """
        # Deal two cards to player and dealer
        for card_no in range(2):
            self._player.receive_card(self._deck.deal_card())
            self._dealer.receive_card(self._deck.deal_card())

    def determine_winner(self, initial_check: bool = False) -> GameStatus:
        """
        Determine the winner by comparing player and dealer hands.

        Args:
            initial_check: If True, only checks for initial blackjack (21 with 2 cards).
                          If False, performs full winner determination.

        Returns:
            GameStatus: Status indicating outcome:
                - PLAYER_WIN: Player wins
                - DEALER_WIN: Dealer wins
                - PUSH: Tie
                - CONTINUE: Game continues (only when initial_check=True)
        """
        if initial_check:
            # Perform initial check for blackjack
            match (
                self._player.hand.value == BLACKJACK,
                self._dealer.hand.value == BLACKJACK,
            ):
                case (True, True):
                    return GameStatus.PUSH
                case (True, False):
                    return GameStatus.PLAYER_WIN
                case (False, True):
                    return GameStatus.DEALER_WIN
                case _:
                    return GameStatus.CONTINUE
        else:
            # Full winner determination (final results)
            if self._player.hand.is_bust:
                return GameStatus.DEALER_WIN
            elif self._dealer.hand.is_bust:
                return GameStatus.PLAYER_WIN
            else:
                player_value = self._player.hand.value
                dealer_value = self._dealer.hand.value

                if player_value == dealer_value:
                    return GameStatus.PUSH
                return (
                    GameStatus.PLAYER_WIN
                    if player_value > dealer_value
                    else GameStatus.DEALER_WIN
                )

    def player_turn(self, choice) -> bool:
        """Execute a single player turn (one decision).

        Prompts player for hit or stand, and processes
        next decision.

        Returns:
            bool: True if player should be prompted again,
        """
        if choice in ("h", "hit"):
            card = self._deck.deal_card()
            self._player.receive_card(card)

            # If Player busted they should not be prompted again
            return not self._player.hand.is_bust

        # Return False for stand, True for invalid input (to continue prompting)
        return choice not in ("s", "stand")

    def dealer_turns(self) -> list[str]:
        """Execute the dealer's turns.
        Dealer must hit until reaching 17 or higher.

        Returns:
            list[str]: List of action to display
        """
        actions = []

        actions.append("\nDealer reveals hand:")
        actions.append(self._dealer.show_hand())
        actions.append(f"Dealer's value: {self._dealer.hand.value}")

        while self._dealer.hand.value < 17:
            actions.append("\nDealer hits...")
            card = self._deck.deal_card()
            self._dealer.receive_card(card)
            actions.append(f"Dealer drew: {card}")
            actions.append(f"Dealer's new value: {self._dealer.hand.value}")

            if self._dealer.hand.is_bust:
                actions.append("\nDealer BUST! Dealer exceeded 21.")
                break
        else:
            if self._dealer.hand.value >= 17:
                actions.append(f"\nDealer stands with {self._dealer.hand.value}")

        return actions

    def final_results(self, game_status: GameStatus) -> str:
        """
        Generate the final results message for the game.

        Shows both hands with their values and the appropriate winner message.
        Automatically detects if this is an initial blackjack by checking if
        both players have exactly 2 cards.

        Args:
            game_status: The status of the game (PLAYER_WIN, DEALER_WIN, or PUSH)

        Returns:
            str: Formatted string containing the final results
        """
        result = []

        # Determine if this is an initial blackjack (both players have exactly 2 cards)
        # and one of them has blackjack
        is_initial_blackjack = (
            len(self._player.hand.cards) == 2
            and len(self._dealer.hand.cards) == 2
            and (
                self._player.hand.value == BLACKJACK
                or self._dealer.hand.value == BLACKJACK
            )
        )

        # Add appropriate banner
        result.append("\n" + "=" * 50)
        if is_initial_blackjack:
            result.append("BLACKJACK!")
        else:
            result.append("FINAL RESULTS")
        result.append("=" * 50)

        # Show final hands
        result.append("\nDealer's hand:")
        result.append(self._dealer.show_hand())
        result.append(f"Dealer's hand value: {self._dealer.hand.value}")

        result.append(f"\n{self._player.name}'s hand:")
        result.append(self._player.show_hand())
        result.append(f"{self._player.name}'s hand value: {self._player.hand.value}")

        # Generate result message based on status
        if game_status == GameStatus.PUSH:
            if is_initial_blackjack:
                result.append(
                    f"\nBoth {self._player.name} and Dealer have Blackjack! PUSH!"
                )
            else:
                result.append(f"\nPUSH! It's a tie at {self._player.hand.value}.")
        elif game_status == GameStatus.PLAYER_WIN:
            if is_initial_blackjack:
                result.append(f"\n{self._player.name} has Blackjack! You win!")
            elif self._dealer.hand.is_bust:
                result.append(f"\n{self._player.name.upper()} WINS! Dealer busted.")
            else:
                result.append(f"\n{self._player.name.upper()} WINS! Higher hand value.")
        elif game_status == GameStatus.DEALER_WIN:
            if is_initial_blackjack:
                result.append("\nDealer has Blackjack! Dealer wins.")
            elif self._player.hand.is_bust:
                result.append(f"\nDEALER WINS! {self._player.name} busted.")
            else:
                result.append("\nDEALER WINS! Higher hand value.")

        return "\n".join(result)

    def play(self):
        """
        Play a complete game of Blackjack.

        This orchestrates the entire game flow and handles all console output.
        """
        # Deal initial cards
        print("\n" + "=" * 50)
        print("DEALING CARDS...")
        print("=" * 50)
        self.deal_initial_cards()

        # Show initial hands (dealer's second card hidden)
        print(f"\n{self._player.name}'s hand:")
        print(self._player.show_hand())
        print(f"Value: {self._player.hand.value}")

        print("\nDealer's hand:")
        print(self._dealer.show_hand(initial_reveal=True))

        # Check for immediate blackjack
        game_status = self.determine_winner(initial_check=True)
        if game_status != GameStatus.CONTINUE:
            print(self.final_results(game_status))
            return

        # Player's turn
        print("\n" + "=" * 50)
        print("PLAYER'S TURN")
        print("=" * 50)

        continue_playing = True
        while continue_playing and not self._player.hand.is_bust:

            choice = (
                input(f"\n{self._player.name}, would you like to (h)it or (s)tand? ")
                .lower()
                .strip()
            )
            continue_playing = self.player_turn(choice)

            print(f"{self._player.name} current hand:")
            print(f"{self._player.show_hand()}")
            print(f"Value: {self._player.hand.value}")

        # Only continue to dealer's turn if player didn't bust
        if not self._player.hand.is_bust:
            print("\n" + "=" * 50)
            print("DEALER'S TURN")
            print("=" * 50)
            dealer_actions = self.dealer_turns()
            for action in dealer_actions:
                print(action)

        # Determine winner and display results
        game_status = self.determine_winner()
        print(self.final_results(game_status))


def main():
    """
    Main function to run the Blackjack game.

    Allows playing multiple rounds.
    """
    print("\n" + "=" * 50)
    print("WELCOME TO OBJECT-ORIENTED BLACKJACK!")
    print("=" * 50)
    print("\nRules:")
    print("- Get as close to 21 as possible without going over")
    print("- Number cards are worth their face value")
    print("- Face cards (J, Q, K) are worth 10")
    print("- Aces are worth 11 or 1 (whichever is better)")
    print("- Dealer must hit until reaching 17 or higher")

    # Get player name
    player_name = input("\nEnter your name: ").strip()
    if not player_name:
        player_name = "Player"

    play_again = "y"

    while play_again.lower().startswith("y"):
        # Create and play a new game
        game = BlackjackGame(player_name)
        game.play()

        # Ask if players want to play again
        play_again = input("\n\nWould you like to play again? (y/n): ").strip()

    print("\n" + "=" * 50)
    print("Thanks for playing! Goodbye!")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    main()
