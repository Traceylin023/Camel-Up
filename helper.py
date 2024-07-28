"""
Classes and attributes that may be needed in more than one file.
"""

from enum import Enum


class Color(Enum):
    red = "R"
    green = "G"
    blue = "B"
    yellow = "Y"
    purple = "P"


class Camel:
    def __init__(self, color) -> None:
        self.color = color

    def __repr__(self) -> str:
        return f"{self.color} Camel"


class BettingTicket:
    def __init__(self, color: Color, price: int):
        assert price in [2, 3, 5]
        self.color = color
        self.value = price

    def __repr__(self) -> str:
        return f"Betting Ticket: {self.color} @ {self.value}"


class MoveType(Enum):
    bet = "BET"  # bet on a camel
    token = "TOKEN"  # pyramid token
