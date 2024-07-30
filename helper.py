"""
Classes and attributes that may be needed in more than one file.
"""

from enum import Enum
from termcolor import colored


class Color(Enum):
    red = "RED"
    green = "GREEN"
    blue = "BLUE"
    yellow = "YELLOW"
    purple = "MAGENTA"

    def __str__(self) -> str:
        return colored(self.name, self.value.lower())

    def colorize(self, string) -> str:
        return colored(string, self.value.lower())


class Camel:
    def __init__(self, color) -> None:
        self.color = color

    def __repr__(self) -> str:
        return colored(self.color.name[0].upper(), self.color.value.lower())

    def __str__(self) -> str:
        return colored(self.color.name[0].upper(), self.color.value.lower())

    def __eq__(self, other_camel):
        if isinstance(other_camel, Camel):
            return self.color == other_camel.color
        return False
    def get_color(self):
        return self.color


class BettingTicket:
    def __init__(self, color: Color, price: int):
        assert price in [2, 3, 5]
        self.color = color
        self.value = price

    def __repr__(self) -> str:
        return colored(self.value, self.color.value.lower())

    def __eq__(self, other_ticket) -> bool:
        if isinstance(other_ticket, BettingTicket):
            return (self.color == other_ticket.color) and (self.value == other_ticket.value)
        return False
    def get_value(self):
        return self.value


class MoveType(Enum):
    bet = "BET"  # bet on a camel
    token = "TOKEN"  # pyramid token
    quit = "QUIT"
