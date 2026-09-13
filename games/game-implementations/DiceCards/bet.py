import uuid


class Player:
    def __init__(self, name, initial_balance=0):
        self.id = str(uuid.uuid4())
        self.name = name
        self.balance = initial_balance
        self.markers = {}
        self.bets = []

    def __str__(self):
        return f"Player: {self.name}, Balance: {self.balance}, Markers: {self.markers}, Bets: {self.bets}"


class Bet:
    def __init__(self, player_id, amount, odds, bet_type):
        self.id = str(uuid.uuid4())
        self.player_id = player_id
        self.amount = amount
        self.odds = odds
        self.bet_type = bet_type
        self.resolved = False
        self.payout = 0

    def __str__(self):
        return f"Bet: {self.id}, Player: {self.player_id}, Amount: {self.amount}, Odds: {self.odds}, Type: {self.bet_type}, Resolved: {self.resolved}, Payout: {self.payout}"


class Marker:
    def __init__(self, player_id, amount):
        self.id = str(uuid.uuid4())
        self.player_id = player_id
        self.amount = amount
        self.resolved = False

    def __str__(self):
        return f"Marker: {self.id}, Player: {self.player_id}, Amount: {self.amount}, Resolved: {self.resolved}"


class BetAPI:
    def __init__(self):
        self.players = {}
        self.bets = []
        self.markers = []
        self.bank_balance = 0
        self.bet_id_counter = 1
        self.marker_id_counter = 1

    def generate_bet_id(self):
        bet_id = f"BET-{self.bet_id_counter}"
        self.bet_id_counter += 1
        return bet_id

    def generate_marker_id(self):
        marker_id = f"MARKER-{self.marker_id_counter}"
        self.marker_id_counter += 1
        return marker_id

    def add_player(self, name, initial_balance=0):
        player = Player(name, initial_balance)
        self.players[player.id] = player
        return player.id

    def remove_player(self, player_id):
        if player_id in self.players:
            del self.players[player_id]
        else:
            raise ValueError(f"Player with ID {player_id} does not exist.")

    def add_marker(self, player_id, amount):
        if player_id in self.players:
            if amount > 0:
                marker = Marker(player_id, amount)
                marker.id = self.generate_marker_id()
                self.markers.append(marker)
                self.players[player_id].markers[marker.id] = marker
                self.bank_balance += amount
                return marker.id
            else:
                raise ValueError("Marker amount must be positive.")
        else:
            raise ValueError(f"Player with ID {player_id} does not exist.")

    def resolve_marker(self, marker_id):
        for marker in self.markers:
            if marker.id == marker_id:
                if not marker.resolved:
                    player = self.players[marker.player_id]
                    if player.balance >= marker.amount:
                        player.balance -= marker.amount
                        self.bank_balance -= marker.amount
                        marker.resolved = True
                        return
                    else:
                        raise ValueError(f"Player with ID {player.id} has insufficient funds to resolve the marker.")
                else:
                    raise ValueError(f"Marker with ID {marker_id} is already resolved.")
        raise ValueError(f"Marker with ID {marker_id} does not exist.")

    def place_bet(self, player_id, amount, odds, bet_type):
        if player_id in self.players:
            player = self.players[player_id]
            if player.balance >= amount:
                if amount > 0:
                    bet = Bet(player_id, amount, odds, bet_type)
                    bet.id = self.generate_bet_id()
                    self.bets.append(bet)
                    player.bets.append(bet)
                    player.balance -= amount
                    self.bank_balance += amount
                    return bet.id
                else:
                    raise ValueError("Bet amount must be positive.")
            else:
                raise ValueError(f"Player with ID {player_id} has insufficient funds.")
        else:
            raise ValueError(f"Player with ID {player_id} does not exist.")

    def resolve_bet(self, bet_id, win):
        for bet in self.bets:
            if bet.id == bet_id:
                if not bet.resolved:
                    player = self.players[bet.player_id]
                    if win:
                        payout = bet.amount * bet.odds
                        player.balance += payout
                        self.bank_balance -= payout
                        bet.payout = payout
                    bet.resolved = True
                    return
                else:
                    raise ValueError(f"Bet with ID {bet_id} is already resolved.")
        raise ValueError(f"Bet with ID {bet_id} does not exist.")

    def get_player_balance(self, player_id):
        if player_id in self.players:
            return self.players[player_id].balance
        else:
            raise ValueError(f"Player with ID {player_id} does not exist.")

    def get_bank_balance(self):
        return self.bank_balance
