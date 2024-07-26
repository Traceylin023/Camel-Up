from game import *
from player import *

class Interface():
    def __init__(self, game_manager: Game, player_1: Player, player_2: Player):
        """Initialize the interface"""
        self.game = game_manager
        self.player_1 = player_1
        self.player_2 = player_2

    def display():
        pass
