from enum import Enum
from random import randint, choice
from typing import Any
from helper import *
from player import *

dice_range = [1, 3]


class DiceRoll:
    def __init__(self, color, result) -> None:
        assert dice_range[0] <= result
        assert dice_range[1] >= result
        self.color = color
        self.result = result

    def __repr__(self) -> str:
        return f"{self.color}: {self.result}"


class Game:
    """Main game class. Important attributes:
    - blocks [list] a mapping of the current board and camel positions
    - available_dice [list] a list of color representing the available dice
    - available_betting_tickets [list] a list of currently available betting tickets
    """

    def __init__(self) -> None:
        """Creates a Game object."""
        # initialize variables
        num_squares = 16
        self.blocks = [[] for _ in range(num_squares)]
        self.camels = [Camel(color) for color in Color]
        self.available_dice = {color: True for color in Color}

        # move each camel to a random starting position
        for camel in self.camels:
            starting_position = randint(1, 3) - 1
            self.blocks[starting_position].append(camel)

        # create our betting tokens
        self.available_betting_tickets = [
            BettingTicket(color, value) for color in Color for value in [2, 2, 3, 5]
        ]

        print(self.available_betting_tickets)

        print(self.generate_random_roll())

    def is_valid_move(self, move: tuple[MoveType, Any]) -> bool:
        """Returns whether a move is valid, e.g. betting or rolling"""
        move_type = move[0]
        if move_type == MoveType.token and move[1] == None:
            return True
        elif move_type == MoveType.bet:
            desired_ticket = move[1]
            for betting_ticket in self.available_betting_tickets:
                if (
                    desired_ticket.color == betting_ticket.color
                    and desired_ticket.value == betting_ticket.value
                ):
                    return True

        return False
    
    def remove_ticket(self, ticket: BettingTicket) -> BettingTicket:
        """Removes a ticket from the currently available tickets. Returns the ticket if successful."""
        for i, betting_ticket in enumerate(self.available_betting_tickets):
            if ticket.color == betting_ticket.color and ticket.value == betting_ticket.value:
                return self.available_betting_tickets.pop(i)

        raise Exception("Desired betting ticket not found in available betting tickets.")

    def generate_random_roll(self) -> DiceRoll:
        """Returns a random dice roll as (Color, distance)."""
        color = choice(
            [color for color in self.available_dice if self.available_dice[color]]
        )
        self.available_dice[color] = False
        return DiceRoll(color, randint(1, 3))

    def move_camel(self, camel: Camel, distance: int) -> None:
        """Takes a camel and moves it from its current position in `self.blocks` to that position + `distance`.
        Must consider the stacked ordering. Will move camels above the current one."""
        # initialize variables
        current_position = 0
        camels_to_move = [camel]

        # check for the camel in the current board
        for i, block in enumerate(self.blocks):
            if camel in block:
                current_position = i
                current_order = block  # order as in ordering of the camels

                stack_position = current_order.index(
                    camel
                )  # find the position of our camel in the stack
                camels_to_move = current_order[
                    stack_position:-1
                ]  # get a list of our camel and all above it
                [
                    current_order.remove(camel) for camel in camels_to_move
                ]  # remove everything from the current position

        # move camels to ending position
        final_position = current_position + distance
        self.blocks[final_position].append(camels_to_move)

    def give_coin(self, players: list[Player]):
        """At the end of the leg, distributes coins from rolls to the players based on the current game state."""
        for player in players:
            player.coins += player.get_tokens()

    def give_betting(self, players: list[Player]):
        """At the end of the leg, distributes betting coins to the players based on the current game state."""
        # evaluate the status of each camel
        camel_ordering = []
        for block in self.blocks:
            # iterate over the list backwards
            for camel in block:
                camel_ordering.append(camel)

        winning_camel, second_camel = camel_ordering[-2:-1]

        for player in players:
            for betting_ticket in player.get_betting_cards():
                if betting_ticket.color == winning_camel.color:
                    player.coins += betting_ticket.value
                elif betting_ticket.color == second_camel.color:
                    player.coins += 1
                else:
                    player.coins -= 1


if __name__ == "__main__":
    Game()
