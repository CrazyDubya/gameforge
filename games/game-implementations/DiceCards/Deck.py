import random
import uuid


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f"{self.rank} of {self.suit}"


class Hand:
    def __init__(self, player_id):
        self.id = str(uuid.uuid4())
        self.player_id = player_id
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def remove_card(self, card):
        if card in self.cards:
            self.cards.remove(card)

    def clear(self):
        self.cards = []

    def __str__(self):
        return f"Hand ({self.id}): {', '.join(str(card) for card in self.cards)}"


class Deck:
    def __init__(self, ranks=None, suits=None):
        self.ranks = ranks or ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        self.suits = suits or ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        self.cards = []
        self.discard_pile = []
        self.hands = {}
        self.create_deck()

    def create_deck(self):
        self.cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        if len(self.cards) > 0:
            return self.cards.pop()
        else:
            return None

    def add_cards(self, cards):
        self.cards.extend(cards)

    def remove_card(self, card):
        if card in self.cards:
            self.cards.remove(card)

    def create_hand(self, player_id):
        if player_id not in self.hands:
            self.hands[player_id] = Hand(player_id)
        return self.hands[player_id]

    def get_hand(self, player_id):
        return self.hands.get(player_id)

    def deal_card(self, player_id):
        card = self.draw_card()
        if card:
            hand = self.create_hand(player_id)
            hand.add_card(card)

    def remove_card_from_hand(self, player_id, card):
        hand = self.get_hand(player_id)
        if hand:
            hand.remove_card(card)

    def clear_hand(self, player_id):
        hand = self.get_hand(player_id)
        if hand:
            hand.clear()

    def discard_card(self, card):
        self.discard_pile.append(card)

    def shuffle_discard_into_deck(self):
        self.cards.extend(self.discard_pile)
        self.discard_pile = []
        self.shuffle()

    def __str__(self):
        return f"Deck: {', '.join(str(card) for card in self.cards)}\nDiscard Pile: {', '.join(str(card) for card in self.discard_pile)}"
