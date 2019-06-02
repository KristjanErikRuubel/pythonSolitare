"""Golf Solitaire."""
from itertools import zip_longest
from textwrap import dedent

from cards import Deck


class Solitaire:
    """
    Patience class representing a game of Golf Solitaire.

    This game has 7 columns and 5 cards in each column,
    but the methods should work with other valid values as well.
    """

    columns = 7
    cards_in_column = 5

    def __init__(self):
        """
        Constructor, do the setup here.

        After setup with Solitaire.columns = 7, Solitaire.cards_in_column = 5
        You should have:
        self.tableau -> 7 columns of cards with 5 cards in each column
        self.stock -> 16 cards
        self.waste -> 1 card
        """
        self.deck = Deck()
        self.tableau = []
        self.waste = []
        self.stock = []
        self.deck.shuffle_deck()

        for col in range(Solitaire.columns):
            column = []
            # Deal cards to each column in range of given nr.
            for cards in range(Solitaire.cards_in_column):
                column.append(self.deck.deal_card())
            self.tableau.append(column)
        self.waste.append(self.deck.deal_card())

        while not self.deck.is_empty():
            self.stock.append(self.deck.deal_card())

    def can_move(self, card) -> bool:
        """
        Validate if a card from the tableau can be moved to the waste pile.

        The card must be last in the column list and adjacent by rank
        to the topmost card of the waste pile (last in waste list).
        Example: 8 is adjacent to 7 and 9. Ace is only adjacent to 2.
        King is only adjacent to Queen.
        """
        if card.rank is not None:
            for i in self.tableau:
                if len(i) > 0:
                    if card == i[-1]:
                        return card.rank - 1 == self.waste[-1].rank or card.rank + 1 == self.waste[-1].rank
        return False

    def move_card(self, col: int):
        """
        Move a card from the tableau to the waste pile.

        Does not validate the move.
        :param col: index of column
        """
        if len(self.tableau[col]) > 0:
            card = self.tableau[col].pop()
            self.waste.append(card)

    def deal_from_stock(self):
        """
        Deal last card from stock pile to the waste pile.

        If the stock is empty, do nothing.
        """
        if len(self.stock) > 0:
            self.waste.append(self.stock.pop())

    def has_won(self) -> bool:
        """Check for the winning position - no cards left in tableau."""
        for i in self.tableau:
            if len(i) != 0:
                return False
        return True

    def last_cards(self):
        """Return list of last cards in the tableau."""
        return [self.tableau[i][-1] for i in range(len(self.tableau)) if len(self.tableau[i]) != 0]

    def has_lost(self) -> bool:
        """
        Check for the losing position.

        Losing position: no cards left in stock and no possible moves.
        """
        return len(self.stock) == 0 and len([card for card in self.last_cards() if self.can_move(card)]) == 0

    def print_game(self):
        """
        Print the game.

        Assumes:
        Card(decorated=True) by default it is already set to True
        self.tableau -> a list of lists (each list represents a column of cards)
        self.stock -> a list of Card objects that are in the stock
        self.waste_pile -> a list of Card objects that are in the waste pile

        You may modify/write your own print_game.
        """
        print(f" {'    '.join(list('0123456'))}")
        print('-' * 34)
        print("\n".join([(" ".join((map(str, x)))) for x in (zip_longest(*self.tableau, fillvalue="    "))]))
        print()
        print(f"Stock pile: {len(self.stock)} card{'s' if len(self.stock) != 1 else ''}")
        print(f"Waste pile: {self.waste[-1] if self.waste else 'Empty'}")

    @staticmethod
    def rules():
        """Print the rules of the game."""
        print("Rules".center(40, "-"))
        print(dedent("""
                Objective: Move all the cards from each column to the waste pile.

                A card can be moved from a column to the waste pile if the
                rank of that card is one higher or lower than the topmost card
                of the waste pile. Only the first card of each column can be moved.

                You can deal cards from the stock to the waste pile.
                The game is over if the stock is finished and
                there are no more moves left.

                The game is won once the tableau is empty.

                Commands:
                  (0-6) - integer of the column, where the topmost card will be moved
                  (d) - deal a card from the stock
                  (r) - show rules
                  (q) - quit
                  """))

    def play(self):
        """
        Play a game of Golf Solitaire.

        Create the game loop here.
        Use input() for player input.
        Available commands are described in rules().
        """
        allowed_moves = ["0", "1", "2", "3", "4", "5", "6"]
        self.deck.shuffle_deck()
        while True:
            self.print_game()
            if self.has_won():
                print("You won.")
                break
            if self.has_lost():
                print("You lost.")
                break
            command = input()
            if command == "r":
                self.rules()
                continue
            if command in allowed_moves:
                cmd = int(command)
                if cmd < Solitaire.columns:
                    if self.can_move(self.tableau[cmd][-1]) and len(self.tableau[cmd]) != 0:
                        self.move_card(cmd)
                continue
            if command == "d":
                self.deal_from_stock()
                continue
            if command == "q":
                break
            else:
                print("Wrong input " + str(command))
                continue


if __name__ == '__main__':
    s = Solitaire()
    s.play()
