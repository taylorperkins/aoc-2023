from __future__ import annotations

from collections import Counter

from utils import getInput, timeit


CARD_ORDERING = {
    "A": 0,
    "K": 1,
    "Q": 2,
    "J": 14,  # "joker" is now the weakest
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
        self.bid = int(bid)

        pure_cards = []
        card_values = []
        n_jokers = 0
        for c in cards:
            order = CARD_ORDERING[c]
            card_values.append(order)
            if c == 'J':
                n_jokers += 1
            else:
                pure_cards.append(order)

        if n_jokers == 5:
            self._most_common_cards = [("J", 5,)]
        else:
            # only consider the "pure" cards, non-wild
            self._most_common_cards = (
                Counter(pure_cards)
                .most_common(5)
            )

            # in every case, you always want the joker to be
            # the same as the most common card. This will allow
            # you to bypass 3-of-a-kind/full-house scenarios
            (card, n,) = self._most_common_cards.pop(0)
            self._most_common_cards.insert(0, (card, n+n_jokers,))

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
