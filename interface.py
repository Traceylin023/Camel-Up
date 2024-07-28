from game import *
from player import *
from colorama import *
import numpy as np


class Interface:
    def __init__(self, game_manager: Game, player_1: Player, player_2: Player):
        """Initialize the interface"""
        self.game = game_manager
        self.player_1 = player_1
        self.player_2 = player_2
        self.main_loop()

    def main_loop(self):
        current_player = player_1
        while True:
            self.display()

            # finish leg if needed
            if self.game.is_finished_leg():
                self.game.finish_leg([player_1, player_2])
                print("The leg has finished.")
                print(f"{player_1} has {player_1.coins} coins, and {player_2} has {player_2.coins} coins.")



            # get users action
            action = self.get_player_input(current_player)
            match action[0]:
                case MoveType.bet:
                    betting_card = action[1]
                    print(f"{current_player} has taken {betting_card}")
                    current_player.add_betting_cards(betting_card)
                case MoveType.quit:
                    break
                case MoveType.token:
                    current_player.add_tokens(1)
                    color, result = self.game.generate_random_roll()
                    camel = self.game.get_camel(color)
                    self.game.move_camel(camel, result)
                    print(f"{Camel(color)} has moved by {result}")
            
            # alternate players
            if current_player == player_1:
                current_player = player_2
            else:
                current_player = player_1

        print("Thank you for playing Camel Up!")



    def display(self):
        """Displays the current game state"""
        init()

        # print tickets
        print(f"Available Tickets: {self.game.ticket_status()}")

        # print dice
        used_dice, available_dice = self.game.dice_status()

        used_dice_output = ""
        for color, result in used_dice:
            used_dice_output += colored(result, "white", f"on_{color.value.lower()}")

        available_dice_output = ""
        for color, result in available_dice:
            available_dice_output += colored("   ", "white", f"on_{color.value.lower()}")

        print(f"Used Dice: {used_dice_output}")
        print(f"Available Dice: {available_dice_output}")

        # print current board state
        print(f"The current board is:")
        for i, camels in enumerate(self.game.blocks):
            print(f"{i:02}: {camels}")

        print(f"{player_1} has {player_1.get_betting_cards()} betting cards and {player_1.get_tokens()} pyramid tokens")
        print(f"{player_2} has {player_2.get_betting_cards()} betting cards and {player_2.get_tokens()} pyramid tokens")

    def get_player_input(self, player: Player) -> tuple[MoveType, Any]:
        """Returns a valid move that the `player` would like to take."""
        print(f"It is {player.name}'s turn. {player.name} may take one of the available betting tokens or roll a die.")
        while True:
            user_input = input("To take a betting token, type 'B'. To roll a die, type 'R'. To exit the game, type 'QUIT'.\n").lower()
            if user_input not in ["r", "b", "quit"]:
                print(f"{user_input} is not valid. Please try again.")
                continue
            
            if user_input == "r":
                move = (MoveType.token, None)
                break

            elif user_input == "b":
                print(f"Please choose a betting ticket from {self.game.ticket_status()}.\nEnter 'R' for RED, 'Y' for YELLOW, 'G' for GREEN, 'B' for BLUE, or 'P' for PURPLE.")
                while True:
                    ticket_color = input("").lower() 
                    if ticket_color in ['r', 'y', 'g', 'b', 'p']:
                        match ticket_color:
                            case 'r':
                                color = Color.red
                            case 'y':
                                color = Color.yellow
                            case 'g':
                                color = Color.green
                            case 'b':
                                color = Color.blue
                            case 'p':
                                color = Color.purple
                        move = (MoveType.bet, self.game.available_betting_tickets[color][-1])
                        break
                break

            elif user_input == "quit":
                move = (MoveType.quit, None)


        if self.game.is_valid_move(move):
            return move
        else:
            return (MoveType.quit, None)
                

if __name__ == "__main__":
    print("Welcome to Camel Up!")
    # player_1_name = input("Enter Player 1's name: ")
    player_1_name = "Alice"
    player_1 = Player(player_1_name)
    player_2_name = "Bob"
    # player_2_name = input("Enter Player 2's name: ")
    player_2 = Player(player_2_name)
    game = Game()
    interface = Interface(game, player_1, player_2)
    interface.display()
