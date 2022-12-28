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

    def test_castling(self):
        self.testEngine.board[0][6].make_move((2, 7))
        self.testEngine.board[0][5].make_move((2, 6))
        self.testEngine.board[0][4].make_move((2, 5))

        self.testEngine.board[0][3].make_move((0, 5))

        self.assertEqual(type(self.testEngine.board[0][5]), pieces.King)
        self.testEngine.do_castling()
        self.assertEqual(type(self.testEngine.board[0][4]), pieces.Rook)

    def test_pawn_change_to_queen(self):
        self.testEngine.board[1][2].set_layout(None)
        self.testEngine.board[1][2].make_move((7, 2))
        self.testEngine.is_pawn_changed(self.testEngine.board[7][2])
        self.assertEqual(type(self.testEngine.board[7][2]), pieces.Queen)

    def test_checkmate(self):
        self.assertFalse(self.testEngine.is_checkmate(self.testEngine.player1))
        self.testEngine.board[0][2].make_move((6, 2))
        self.testEngine.board[0][1].make_move((4, 1))

        self.assertTrue(self.testEngine.is_checkmate(self.testEngine.player1))


if __name__ == '__main__':
    unittest.main()