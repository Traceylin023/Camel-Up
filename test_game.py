import unittest
from game import *

class GameTester(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    def test_dice_length(self):
        """Make sure we have a die for each color."""
        used_dice, available_dice = self.game.dice_status()
        self.assertEqual(len(used_dice), 0)
        self.assertEqual(len(available_dice), len(list(Color)))

    def test_one_roll(self):
        """Generates one dice roll."""
        # roll a die
        dice_color, result = self.game.generate_random_roll()
        self.assertIsInstance(dice_color, Color)
        self.assertIn(result, [1, 2, 3])

        # make sure our dice tracker is accurate
        used_dice, available_dice = self.game.dice_status()
        self.assertEqual(len(used_dice), 1)
        self.assertEqual(len(available_dice), 4)

    def test_ticket_status(self):
        """Ensure our starting tickets are all 5."""
        tickets = self.game.ticket_status()
        self.assertEqual(tickets, {color: BettingTicket(color, 5) for color in Color})

    def test_remove_ticket(self):
        """Try taking a ticket."""
        ticket = self.game.remove_ticket(BettingTicket(Color.red, 5))
        self.assertEqual(ticket, BettingTicket(Color.red, 5))

        tickets = self.game.ticket_status()
        correct = {color: BettingTicket(color, 5) for color in Color}
        correct[Color.red] = BettingTicket(Color.red, 3)
        self.assertEqual(tickets, correct)

    def test_move_unstacked_camel(self):
        """Move a unstacked camel forward by 1 square."""
        self.game.blocks = [[] for _ in range(16)]
        square_1_camels = [
            Camel(Color.red),
            Camel(Color.yellow),
            Camel(Color.green),
            Camel(Color.blue),
        ]
        self.game.blocks[0] = square_1_camels
        self.game.blocks[0].append(Camel(Color.purple))

        self.game.move_camel(self.game.get_camel(Color.purple), 1)

        goal_board = [[] for _ in range(16)]
        goal_board[0] = square_1_camels
        goal_board[1] = [self.game.get_camel(Color.purple)]

        self.assertEqual(self.game.blocks, goal_board)

    def test_move_5_stacked_camel(self):
        """Move a stack of 5 camels forward by 1 square."""
        self.game.blocks = [[] for _ in range(16)]
        initial_camels = [
            self.game.get_camel(Color.red),
            self.game.get_camel(Color.yellow),
            self.game.get_camel(Color.green),
            self.game.get_camel(Color.blue),
            self.game.get_camel(Color.purple),
        ]
        self.game.blocks[0] = [camel for camel in initial_camels]

        self.game.move_camel(self.game.get_camel(Color.red), 1)

        goal_board = [[] for _ in range(16)]
        goal_board[1] = initial_camels

        self.assertEqual(self.game.blocks, goal_board)

    def test_move_stacked_camel(self):
        """Move a stack of 2 camels forward by 1 square."""
        # stack of R, Y on the first square; G, B, P on the second
        self.game.blocks = [[] for _ in range(16)]
        self.game.blocks[0] = [self.game.get_camel(Color.red), self.game.get_camel(Color.yellow)]
        self.game.blocks[1] = [
            self.game.get_camel(Color.green),
            self.game.get_camel(Color.blue),
            self.game.get_camel(Color.purple),
        ]

        # move the stack of R, Y on top of G, B, P
        self.game.move_camel(self.game.get_camel(Color.red), 1)

        goal_board = [[] for _ in range(16)]
        goal_board[1] = [
            self.game.get_camel(Color.green),
            self.game.get_camel(Color.blue),
            self.game.get_camel(Color.purple),
            self.game.get_camel(Color.red),
            self.game.get_camel(Color.yellow),
        ]

        self.assertEqual(self.game.blocks, goal_board)

    def test_move_camel_off_board(self):
        """Try moving a camel off the board"""
        # stack of R, Y on the first square; G, B, P on the second
        self.game.blocks = [[] for _ in range(16)]
        self.game.blocks[self.game.num_squares - 2] = [self.game.get_camel(Color.red)]

        # move the stack of R, Y on top of G, B, P
        final_position, game_end = self.game.move_camel(self.game.get_camel(Color.red), 2)
        goal_board = [[] for _ in range(16)]
        goal_board[self.game.num_squares - 1] = [self.game.get_camel(Color.red)]

        self.assertEqual(self.game.blocks, goal_board)
        self.assertEqual(final_position, self.game.num_squares - 1)
        self.assertEqual(game_end, True)

    def test_EV_for_last_camel(self):
        """Test EV of last camel to be -1"""
        self.game.blocks = [[] for _ in range(16)]
        self.game.available_dice = {color: 1 for color in Color}
        self.game.available_dice[Color.purple] = 0
        for camel in self.game.camels:
            self.game.blocks[15].append(camel)
        self.game.move_camel(self.game.camels[-1], -10)
        self.assertEqual(self.game.EV()[self.game.camels[-1].get_color()], -1)

    def test_EV_for_first_camel(self):
        """Test EV of first camel to be 5"""
        self.game.blocks = [[] for _ in range(16)]
        self.game.available_dice = {color: 1 for color in Color}
        self.game.available_dice[Color.purple] = 0
        for camel in self.game.camels:
            self.game.blocks[1].append(camel)
        self.game.move_camel(self.game.camels[-1], 10)
        self.assertEqual(self.game.EV()[self.game.camels[-1].get_color()], 5)

    def test_EV_for_second_camel(self):
        """Test EV of second camel to be 1"""
        self.game.blocks = [[] for _ in range(16)]
        self.game.available_dice = {color: 1 for color in Color}
        self.game.available_dice[Color.purple] = 0
        for camel in self.game.camels:
            self.game.blocks[1].append(camel)
        self.game.move_camel(self.game.camels[-1], 10)
        self.game.move_camel(self.game.camels[-2], 9)
        self.assertEqual(self.game.EV()[self.game.camels[-2].get_color()], 1)

if __name__ == '__main__':
    unittest.main()
