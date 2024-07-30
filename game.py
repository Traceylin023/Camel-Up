from enum import Enum
from random import randint, choice
from typing import Any
from helper import *
from player import *
from termcolor import colored
import itertools
from copy import deepcopy

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

    def ticket_status(self) -> dict:
        """Returns a list of the highest available betting tickets for each color, i.e. the information displayed at the ticket tent."""
        max_tickets = {}
        for color in self.available_betting_tickets:
            max_tickets[color] = self.available_betting_tickets[color][-1]

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
        game_end = False

        if final_position >= self.num_squares:
            final_position = self.num_squares - 1
            game_end = True

        for camel in camels_to_move:
            self.blocks[final_position].append(camel)
        return (final_position, game_end)

    def give_coin(self, players: list[Player]):
        """At the end of the leg, distributes coins from rolls to the players based on the current game state."""
        for player in players:
            player.coins += player.get_tokens()


    def get_winning_camels(self, blocks=None) -> tuple[Camel, Camel]:
        """Returns a ordered tuple of the top two camels. If no `blocks` is passed in, evaluates self. If `blocks` is passedd, evaluates that game state."""
        if blocks is None:
            blocks = self.blocks
        # evaluate the status of each camel
        camel_ordering = []
        for block in blocks:
            # iterate over the list backwards
            for camel in block:
                camel_ordering.append(camel)

        return camel_ordering[-1], camel_ordering[-2]

    def give_betting(self, players: list[Player]):
        """At the end of the leg, distributes betting coins to the players based on the current game state."""
        winning_camel, second_camel = self.get_winning_camels() 

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
        # distribute coins
        self.give_coin(players)
        self.give_betting(players)

        # reset players
        for player in players:
            player.betting_cards = []
            player.token = 0

        # reset dice
        self.available_dice = {color: 0 for color in Color}

        # reset available betting tickets
        self.available_betting_tickets = {
            color: [
                BettingTicket(color, 2),
                BettingTicket(color, 2),
                BettingTicket(color, 3),
                BettingTicket(color, 5),
            ]
            for color in Color
        }

    def is_finished_leg(self) -> bool:
        """Returns whether the leg has finished."""
        if len(self.dice_status()[1]) == 0:
            return True

        return False
    
    def expected_winner(self, board: list[list[Camel]], dice_rolls: tuple[int], color_permutation: tuple[Color]) -> tuple[Camel, Camel]:
        """Takes a starting board state, a list of dice rolls, and the color order of the dice. Returns the top two camels."""
        # print(f"dice roll: {len(dice_rolls)}")
        # print(f"color permuation: {len(color_permutation)}")
        assert len(dice_rolls) == len(color_permutation)
        new_game = Game() 
        new_game.blocks = deepcopy(board)
        for i in range(len(color_permutation)):
            new_game.move_camel(Camel(color_permutation[i]), dice_rolls[i])

        return new_game.get_winning_camels()
        
    # *** EXPECTED VALUE CODE ***

    def EV(self) -> list[tuple]:
        """Returns a list of all possible dice combinations"""
        _, available_dice = self.dice_status()
        available_dice = [x[0] for x in available_dice]
        color_permutation = list(itertools.permutations(available_dice))
        dice_product = [1, 2, 3]
        for i in range(len(available_dice) - 1):
            dice_product = list(itertools.product([1, 2, 3], dice_product))
            if i > 0:
                for j, tup in enumerate(dice_product):
                    tup = [tup[0]] + list(tup[1])
                    dice_product[j] = tuple(tup)
            # print(f"{i}: {dice_product}\n")
        first_place = {color:0 for color in Color}
        second_place = {color:0 for color in Color}
        for color in color_permutation:
            for dice_roll in dice_product:
                first_place_camel, second_place_camel = self.expected_winner(self.blocks, dice_roll, color)
                first_place[first_place_camel.get_color()] += 1
                second_place[second_place_camel.get_color()] += 1
        combos = (len(color_permutation) * len(dice_product))
        return [(color, 
                 first_place[color] / combos * self.ticket_status()[color].get_value() + 
                 second_place[color] / combos  - 
                 (combos - first_place[color] - second_place[color]) / combos) for color in Color]

if __name__ == "__main__":
    manager = Game()
