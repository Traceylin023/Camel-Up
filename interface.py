from game import *
from player import *
from colorama import *
import os


class Interface:
    def __init__(self, game_manager: Game, player_1: Player, player_2: Player):
        """Initialize the interface"""
        self.game = game_manager
        self.player_1 = player_1
        self.player_2 = player_2
        self.main_loop()

    def clear(self):
        """Clears the current display."""
        if os.name == "nt":
            _ = os.system("cls")
        else:
            _ = os.system("clear")

    def main_loop(self):
        """The game run loop."""
        self.clear()
        current_player = player_1
        while True:
            # finish leg if needed
            if self.game.is_finished_leg():
                self.game.finish_leg([player_1, player_2])
                print("************")
                print("The leg has finished.")
                print("************")
                print(
                    f"{player_1} has {player_1.coins} coins, and {player_2} has {player_2.coins} coins."
                )

            self.display()

            # get users action
            action = self.get_player_input(current_player)
            output_message = ""
            match action[0]:
                case MoveType.bet:
                    betting_card = action[1]
                    output_message = (
                        f"***\n{current_player} has taken {betting_card}\n***"
                    )
                    current_player.add_betting_cards(betting_card)
                    self.game.remove_ticket(betting_card)
                case MoveType.quit:
                    print("*********\nThank you for playing Camel Up!\n*********")
                    return
                case MoveType.token:
                    current_player.add_tokens(1)
                    color, result = self.game.generate_random_roll()
                    camel = self.game.get_camel(color)
                    final_square, game_end = self.game.move_camel(camel, result)
                    if game_end:
                        self.finish_game()
                        break
                    output_message = f"***\n{Camel(color)} has moved by {result}\n***"

            self.clear()
            print(output_message)
            if not self.game.is_finished_leg():
                print(f"EV: {self.game.EV()}")

            # alternate players
            if current_player == player_1:
                current_player = player_2
            else:
                current_player = player_1

        print("*********\nThank you for playing Camel Up!\n*********")

    def display(self):
        """Displays the current game state"""
        init()

        # print tickets
        print("--- Ticket Tent ---")
        print(f"Available Tickets: {list(self.game.ticket_status().values())}")
        print("\n")

        # print dice
        print("--- Dice ---")
        used_dice, available_dice = self.game.dice_status()

        used_dice_output = ""
        for color, result in used_dice:
            used_dice_output += colored(result, "white", f"on_{color.value.lower()}")

        available_dice_output = ""
        for color, result in available_dice:
            available_dice_output += colored(
                "   ", "white", f"on_{color.value.lower()}"
            )

        print(f"Used Dice: {used_dice_output}")
        print(f"Available Dice: {available_dice_output}")
        print("\n")

        # print current board state
        print("--- Board ---")
        print(f"The current board is:")
        for i, camels in enumerate(self.game.blocks):
            print(f"{i+1:02}: {camels}")
        print("\n")

        print("--- Player Status ---")
        print(
            f"{player_1} has {player_1.get_betting_cards()} betting cards and {player_1.get_tokens()} pyramid tokens"
        )
        print(
            f"{player_2} has {player_2.get_betting_cards()} betting cards and {player_2.get_tokens()} pyramid tokens"
        )
        print("\n")

    def get_player_input(self, player: Player) -> tuple[MoveType, Any]:
        """Returns a valid move that the `player` would like to take."""
        print("--- User Input ---")
        print(
            f"It is {player.name}'s turn. {player.name} may take one of the available betting tokens or roll a die."
        )
        while True:
            user_input = input(
                "To take a betting token, type 'B'. To roll a die, type 'R'. To exit the game, type 'QUIT'.\n"
            ).lower()
            if user_input not in ["r", "b", "quit"]:
                print(f"{user_input} is not valid. Please try again.")
                continue

            if user_input == "r":
                move = (MoveType.token, None)
                break

            elif user_input == "b":
                print(
                    f"Please choose a betting ticket from {self.game.ticket_status()}.\nEnter 'R' for RED, 'Y' for YELLOW, 'G' for GREEN, 'B' for BLUE, or 'P' for PURPLE."
                )
                while True:
                    ticket_color = input("").lower()
                    if ticket_color in ["r", "y", "g", "b", "p"]:
                        match ticket_color:
                            case "r":
                                color = Color.red
                            case "y":
                                color = Color.yellow
                            case "g":
                                color = Color.green
                            case "b":
                                color = Color.blue
                            case "p":
                                color = Color.purple
                        move = (
                            MoveType.bet,
                            self.game.available_betting_tickets[color][-1],
                        )
                        break
                break

            elif user_input == "quit":
                move = (MoveType.quit, None)
                break

        if self.game.is_valid_move(move):
            return move
        else:
            return (MoveType.quit, None)

    def finish_game(self):
        self.clear()

        if player_1.coins > player_2.coins:
            winner = player_1
        elif player_2.coins > player_1.coins:
            winner = player_2
        else:
            print(
                f"{player_1.name} and {player_2.name} have tied with {player_1.coins} coins!"
            )
            return

        print(f"The winner is {winner.name} with {winner.coins} coins!")


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
