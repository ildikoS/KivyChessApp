import itertools
import random
import time

import attributesconf

tile_size = attributesconf.tile_size


class LastPieceStep:
    def __init__(self, board, piece, targetMove):
        self.board = [x[:] for x in board]
        self.piece = piece
        self.alreadyMoved = self.piece.alreadyMoved
        self.coordinates = piece.coordinates
        self.move = targetMove
        self.targetTile = self.board[targetMove[0]][targetMove[1]]
        self.piecesList = self.piece.player.pieces


class Piece:
    def __init__(self):
        self.alreadyMoved = False
        self.coordinates = None
        self.engine = None
        self.board = None
        self.player = None
        self.enemy = None
        self.pieceColor = None
        self.availableMoves = []
        self.removingPiece = None

    @staticmethod
    def is_inside(toX, toY):
        return 0 <= toX < 8 and 0 <= toY < 8

    def gen_sliding_move(self, dirX, dirY):
        """
        Calculating available moves of sliding pieces
        :param dirX: the given direction on X axis
        :param dirY: the given direction on Y axis
        """
        for i in range(1, 8):
            X = self.coordinates[0] + (i * dirX)
            Y = self.coordinates[1] + (i * dirY)

            if self.is_inside(X, Y):
                if self.board[X][Y] in self.player.pieces:
                    break

                self.availableMoves.append((X, Y))

                if self.board[X][Y] in self.enemy.pieces:
                    break

    def make_move(self, move):
        """
        Set the (x, y) square of piece
        Saves the current game to can be restored
        :param move: Tuple with integer x, y coordinates of piece
        """
        self.engine.pieceStepsList.append(LastPieceStep(self.board, self, move))
        self.removingPiece = None
        x, y = self.coordinates
        self.board[x][y] = "-"

        x, y = move
        self.engine.targetTile = self.engine.pieceStepsList[-1].targetTile
        self.board[x][y] = self.engine.pieceStepsList[-1].piece
        self.set_coords(x, y)
        if self.engine.targetTile != "-":
            self.removingPiece = self.engine.targetTile
            self.enemy.pieces.remove(self.engine.targetTile)

        if self.coordinates == self.engine.kingSquare and y in [1, 5]:
            self.engine.do_castling()

        self.engine.set_king_square(self.get_piece_color())

    def computer_move(self):
        """

        :return: With the best piece and its best move based on the minimax algorithm
        """
        #start_time = time.time()
        bestPieceWithMove = self.engine.ai.minimax(self.enemy, self.engine.ai.depth, False, -9999, 9999)
        #print(f"--- {time.time() - start_time} seconds ---")

        if bestPieceWithMove[1][0] is None:
            randomPiece = None
            randomMove = None
            while randomPiece is None:
                randomPiece = random.choice(self.player.pieces)
                if not randomPiece.availableMoves:
                    randomPiece = None
                if randomPiece is not None:
                    randomMove = random.choice(randomPiece.availableMoves)
            bestPieceWithMove = randomPiece, randomMove
            compPiece = bestPieceWithMove[0]
            compMove = bestPieceWithMove[1]
        else:
            compPiece = bestPieceWithMove[1][0]
            compMove = bestPieceWithMove[1][1]

        compPiece.make_move(compMove)

        return compPiece, compMove

    # getters, setters
    def set_piece_color(self, color):
        self.pieceColor = color

    def set_engine(self, engine):
        self.engine = engine
        self.board = self.engine.board

        self.player = self.engine.player1 if self.get_piece_color() == 'b' else self.engine.player2
        self.enemy = self.engine.player2 if self.player == self.engine.player1 else self.engine.player1

    def set_layout(self, layout):
        self.pieceLayout = layout

    def get_piece_color(self):
        return self.pieceColor

    def set_coords(self, x, y):
        self.coordinates = (x, y)

    def is_already_moved(self, moved):
        self.alreadyMoved = moved



