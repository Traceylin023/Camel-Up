from game import *
from player import *
from colorama import *

class Interface():
    def __init__(self, game_manager: Game, player_1: Player, player_2: Player):
        """Initialize the interface"""
        self.game = game_manager
        self.player_1 = player_1
        self.player_2 = player_2

    def display():
        init()
        pass

if __name__ == "__main__": 
    print("Welcome to Camel Up!")
    player_1_name = input("Enter Player 1 name:")
    player_1 = Player(player_1_name)
    player_2_name = input("Enter Player 2 name:")
    player_2 = Player(player_2_name)
    game = Game(player1, player2)

    init()

