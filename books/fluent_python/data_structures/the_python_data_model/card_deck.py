from __future__ import annotations

import collections

Card = collections.namedtuple("Card", ["rank", "suit"])

class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list("JQKA")
    suits = "spades diamonds clubs hearts".split()
    
    def __init__(self) -> None:
        self._cards = [
            Card(rank, suit)
            for suit in self.suits
            for rank in self.ranks
        ]
        
    def __len__(self) -> int:
        return len(self._cards)
    
    def __getitem__(self, position) -> Card:
        return self._cards[position]
    

deck = FrenchDeck()

print(f"French deck has: {len(deck)} cards")
for card in reversed(deck):
    print(card)