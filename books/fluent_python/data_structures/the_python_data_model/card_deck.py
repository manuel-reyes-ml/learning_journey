# Practice special methods in Python classes (dunder = double underscore function)

from __future__ import annotations

import collections

# Construct a simple class to represent individual cards
Card = collections.namedtuple("Card", ["rank", "suit"])

class FrenchDeck:
    # Class-level attributes -> shared to all instances
    ranks = [str(n) for n in range(2, 11)] + list("JQKA")
    suits = "spades diamonds clubs hearts".split()
    
    def __init__(self) -> None:
        # Instance-level attributes -> each per instance
        self._cards = [
            Card(rank, suit)
            for suit in self.suits
            for rank in self.ranks
        ]

    # Get size of object (instance)
    def __len__(self) -> int:
        return len(self._cards)
    
    # Allow object to be called by:
    #   x in y, y[:], reversed(), sorted(), etc...
    def __getitem__(self, position: int) -> Card:
        return self._cards[position]
    

deck = FrenchDeck()

print(f"French deck has: {len(deck)} cards")
for card in reversed(deck):
    print(card)