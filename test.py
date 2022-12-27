import unittest

import attributesconf
import pieces
from gameEngine import GameEngine


class ChessTestCase(unittest.TestCase):

    def __init__(self, methodName: str = ...):
        super().__init__(methodName)
        self.testEngine = GameEngine(attributesconf.mainFEN)
        self.testEngine.create_board()

        for piece in self.testEngine.player1.pieces:
            piece.set_engine(self.testEngine)
        for piece in self.testEngine.player2.pieces:
            piece.set_engine(self.testEngine)

    def test_adding_pieces_to_players(self):
        blackPieces = self.testEngine.player1.pieces
        whitePieces = self.testEngine.player2.pieces
        self.assertEqual(len(blackPieces), 16)
        self.assertEqual(len(whitePieces), 16)

        for piece in blackPieces:
            self.assertEqual(piece.get_piece_color(), "b")
        for piece in whitePieces:
            self.assertEqual(piece.get_piece_color(), "w")

    def test_pieces_attributes(self):
        self.assertEqual(type(self.testEngine.board[1][0]), pieces.Pawn)
        self.assertFalse(self.testEngine.board[1][0].alreadyMoved)

        self.testEngine.board[1][0].generate_moves()
        self.assertEqual(self.testEngine.board[1][0].availableMoves, [(2, 0), (3, 0)])

        self.testEngine.board[1][0].make_move((2, 0))
        self.testEngine.board[2][0].is_already_moved(True)
        self.assertEqual(self.testEngine.board[2][0].coordinates, (2, 0))
        self.assertTrue(self.testEngine.board[2][0].alreadyMoved)

    def test_reset_step(self):
        previousBoard = [x[:] for x in self.testEngine.board]

        self.testEngine.board[1][0].make_move((2, 0))
        self.testEngine.board[1][3].make_move((2, 3))
        self.assertNotEqual(self.testEngine.board, previousBoard)

        self.testEngine.unmake_move()
        self.testEngine.unmake_move()
        self.assertEqual(self.testEngine.board, previousBoard)

    def test_minmax_depth_1(self):
        self.testEngine.ai.set_depth(1)

        self.testEngine.board[1][0].make_move((5, 0))
        self.assertEqual(self.testEngine.board[5][0].coordinates, (5, 0))

        computerMove = self.testEngine.board[5][0].computer_move()
        self.assertEqual(computerMove[1], (5, 0))


if __name__ == '__main__':
    unittest.main()