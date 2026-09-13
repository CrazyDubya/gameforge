class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f"{self.rank} of {self.suit}"


class RankAPI:
    def __init__(self):
        self.ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        self.suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']

    def get_card_value_blackjack(self, card):
        if card.rank in ['Jack', 'Queen', 'King']:
            return 10
        elif card.rank == 'Ace':
            return 11
        else:
            return int(card.rank)

    def get_card_value_poker(self, card):
        return self.ranks.index(card.rank) + 2

    def get_hand_value_blackjack(self, hand):
        total = sum(self.get_card_value_blackjack(card) for card in hand)
        num_aces = sum(1 for card in hand if card.rank == 'Ace')

        while total > 21 and num_aces > 0:
            total -= 10
            num_aces -= 1

        return total

    def get_hand_rank_poker(self, hand):
        ranks = [self.get_card_value_poker(card) for card in hand]
        suits = [card.suit for card in hand]

        if self.is_royal_flush(ranks, suits):
            return "Royal Flush"
        elif self.is_straight_flush(ranks, suits):
            return "Straight Flush"
        elif self.is_four_of_a_kind(ranks):
            return "Four of a Kind"
        elif self.is_full_house(ranks):
            return "Full House"
        elif self.is_flush(suits):
            return "Flush"
        elif self.is_straight(ranks):
            return "Straight"
        elif self.is_three_of_a_kind(ranks):
            return "Three of a Kind"
        elif self.is_two_pair(ranks):
            return "Two Pair"
        elif self.is_one_pair(ranks):
            return "One Pair"
        else:
            return "High Card"

    def is_royal_flush(self, ranks, suits):
        return self.is_flush(suits) and set(ranks) == set(range(10, 15))

    def is_straight_flush(self, ranks, suits):
        return self.is_flush(suits) and self.is_straight(ranks)

    def is_four_of_a_kind(self, ranks):
        return any(ranks.count(rank) == 4 for rank in ranks)

    def is_full_house(self, ranks):
        return self.is_three_of_a_kind(ranks) and self.is_one_pair(ranks)

    def is_flush(self, suits):
        return len(set(suits)) == 1

    def is_straight(self, ranks):
        return len(set(ranks)) == 5 and max(ranks) - min(ranks) == 4

    def is_three_of_a_kind(self, ranks):
        return any(ranks.count(rank) == 3 for rank in ranks)

    def is_two_pair(self, ranks):
        return len(set(ranks)) == 3 and self.is_one_pair(ranks)

    def is_one_pair(self, ranks):
        return len(set(ranks)) == 4
