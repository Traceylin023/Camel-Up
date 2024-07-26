class Player():
    """Represents a human camel up player.
    """

    def __init__(self, player_name: str):
        """Initialize the player"""
        self.name = player_name
        self.token = 0
        self.betting_cards =[]

    def __str__(self):
        return self.name

    def get_betting_cards(self):
        return self.betting_cards
    
    def get_tokens(self):
        return self.token
    
    def add_betting_cards(self, betting_card: tuple):
        self.betting_cards.add(betting_card)
    
    def add_tokens(self, coin: int):
        self.token += coin