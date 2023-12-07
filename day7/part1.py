from __future__ import annotations

from collections import Counter

from utils import getInput, timeit


CARD_ORDERING = {
    "A": 0,
    "K": 1,
    "Q": 2,
    "J": 3,
    "T": 4,
    "9": 5,
    "8": 6,
    "7": 7,
    "6": 8,
    "5": 9,
    "4": 10,
    "3": 11,
    "2": 12,
    "1": 13,
}


class Hand:
    def __init__(self, cards: str, bid: str):
        self.cards = cards
        card_values = [CARD_ORDERING[c] for c in cards]

        self.bid = int(bid)

        self._most_common_cards = Counter(card_values).most_common(5)
        self._n_cards = len(self._most_common_cards)

        self.value = [self.hand_type] + card_values

    def __repr__(self):
        return "".join(sorted(
            self.cards,
            key=lambda c: CARD_ORDERING[c]
        ))

    def __lt__(self, other):
        return self.value < other.value

    @property
    def hand_type(self):
        # five of a kind
        if self._most_common_cards[0][1] == 5:
            return 1
        # four of a kind
        elif self._most_common_cards[0][1] == 4:
            return 2
        # full house
        elif self._most_common_cards[0][1] == 3 and self._most_common_cards[1][1] == 2:
            return 3
        # three of a kind
        elif self._most_common_cards[0][1] == 3:
            return 4
        # two pair
        elif self._most_common_cards[0][1] == self._most_common_cards[1][1] == 2:
            return 5
        # one pair
        elif self._most_common_cards[0][1] == 2:
            return 6
        # no matches, defaulting to the highest card
        elif self._n_cards == 5:
            return 7
        else:
            raise Exception("Unexpected!")


@timeit
def main(aoc: str):
    hands = sorted([
        Hand(*line.split(" "))
        for line in aoc.splitlines()
    ])

    total_winnings = 0
    for idx, hand in enumerate(hands[::-1]):
        score = (idx+1) * hand.bid
        total_winnings += score

    print(total_winnings)


if __name__ == "__main__":
    main(getInput("./input-test.txt"))
    main(getInput("./input.txt"))
