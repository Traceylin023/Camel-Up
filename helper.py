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

    def __repr__(self) -> str:
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

class BettingTicket:
    def __init__(self, color: Color, price: int):
        assert price in [2, 3, 5]
        self.color = color
        self.value = price

    def __repr__(self) -> str:
        return colored(self.value, self.color.value.lower())


class MoveType(Enum):
    bet = "BET"  # bet on a camel
    token = "TOKEN"  # pyramid token
    quit = "QUIT"
