from enum import Enum
from random import randint, choice
from typing import Any
from helper import *
from player import *
from termcolor import colored

dice_range = [1, 3]


class Game:
    """Main game class. Important attributes:
    - blocks [list] a mapping of the current board and camel positions
    - available_dice [list] a list of color representing the available dice
    - available_betting_tickets [list] a list of currently available betting tickets
    """

    def __init__(self) -> None:
        """Creates a Game object."""
        # initialize variables
        self.num_squares = 16
        self.blocks = [[] for _ in range(self.num_squares)]
        self.camels = [Camel(color) for color in Color]
        self.available_dice = {color: 0 for color in Color}

        # move each camel to a random starting position
        for camel in self.camels:
            starting_position = randint(1, 3) - 1
            self.blocks[starting_position].append(camel)

        # create our betting tokens
        self.available_betting_tickets = {
            color: [
                BettingTicket(color, 2),
                BettingTicket(color, 2),
                BettingTicket(color, 3),
                BettingTicket(color, 5),
            ]
            for color in Color
        }

    def is_valid_move(self, move: tuple[MoveType, Any]) -> bool:
        """Returns whether a move is valid, e.g. betting or rolling"""
        move_type = move[0]
        if (
            move_type == MoveType.token
            and move[1] == None
            and len(self.dice_status()[1]) > 0
        ):
            return True
        elif move_type == MoveType.bet:
            desired_ticket = move[1]
            for betting_ticket in self.available_betting_tickets[desired_ticket.color]:
                if desired_ticket.value == betting_ticket.value:
                    return True

        return False

    def remove_ticket(self, ticket: BettingTicket) -> BettingTicket:
        """Removes a ticket from the currently available tickets. Returns the ticket if successful."""
        for i, betting_ticket in enumerate(
            self.available_betting_tickets[ticket.color]
        ):
            if ticket.value == betting_ticket.value:
                return self.available_betting_tickets[ticket.color].pop(i)

        raise Exception(
            "Desired betting ticket not found in available betting tickets."
        )

    def ticket_status(self) -> list[BettingTicket]:
        """Returns a list of the highest available betting tickets for each color, i.e. the information displayed at the ticket tent."""
        max_tickets = []
        for tickets_by_color in self.available_betting_tickets.values():
            max_tickets.append(tickets_by_color[-1])

        return max_tickets

    def generate_random_roll(self) -> tuple[Color, int]:
        """Returns a random dice roll as (Color, distance)."""
        color = choice(
            [color for color, result in self.available_dice.items() if result == 0]
        )
        roll = randint(*dice_range)
        self.available_dice[color] = roll
        return (color, roll)

    def dice_status(self) -> tuple[list[tuple[Color, int]], list[tuple[Color, int]]]:
        """Returns a tuple containing a list of used dice and unused dice. Each dice is represented by a color and a integer result."""
        used_dice = []
        available_dice = []
        for color, result in self.available_dice.items():
            if result != 0:
                used_dice.append((color, result))
            else:
                available_dice.append((color, result))

        return (used_dice, available_dice)

    def get_camel(self, color: Color) -> Camel:
        """Returns the camel matching a given color."""
        for camel in self.camels:
            if camel.color == color:
                return camel
        return None

    def move_camel(self, camel: Camel, distance: int) -> int:
        """Takes a camel and moves it from its current position in `self.blocks` to that position + `distance`.
        Must consider the stacked ordering. Will move camels above the current one. Returns the final position of the camel stack."""
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
                if stack_position < len(current_order) - 1:
                    camels_to_move = current_order[
                        stack_position:
                    ]  # get a list of our camel and all above it
                # print(f"{stack_position = }, {camels_to_move = }, {current_order = }, {current_position = }")
                [
                    current_order.remove(camel) for camel in camels_to_move
                ]  # remove everything from the current position

        # move camels to ending position
        final_position = current_position + distance

        if final_position >= self.num_squares:
            final_position = self.num_squares - 1

        for camel in camels_to_move:
            self.blocks[final_position].append(camel)
        return final_position

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

        winning_camel, second_camel = camel_ordering[-1], camel_ordering[-2]

        for player in players:
            for betting_ticket in player.get_betting_cards():
                if betting_ticket.color == winning_camel.color:
                    player.coins += betting_ticket.value
                elif betting_ticket.color == second_camel.color:
                    player.coins += 1
                else:
                    player.coins -= 1

    def finish_leg(self, players: list[Player]):
        """Housekeeping at the end of each leg of the game."""
        self.give_coin(players)
        self.give_betting(players)
        self.available_dice = {color: 0 for color in Color}
        for player in players:
            player.betting_cards = []
            player.token = 0

    def is_finished_leg(self) -> bool:
        """Returns whether the leg has finished."""
        if len(self.dice_status()[1]) == 0:
            return True

        return False


if __name__ == "__main__":
    manager = Game()
