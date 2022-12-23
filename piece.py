import itertools
import time

tile_size = 80


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

    def isInside(self, x, y):
        return 0 <= x < 8 and 0 <= y < 8

    def genSlidingMove(self, dirX, dirY):
        for i in range(1, 8):
            X = self.coordinates[0] + (i * dirX)
            Y = self.coordinates[1] + (i * dirY)

            if self.isInside(X, Y):
                if self.board[X][Y] in self.player.pieces:
                    break

                self.availableMoves.append((X, Y))

                if self.board[X][Y] in self.enemy.pieces:
                    break

    def make_move(self, move):
        """
        Set the (x, y) square of piece
        :param move: Tuple with number x, y coordinates
        :param argPiece: Piece which wanted to be moved to the square
        """
        self.engine.pieceStepsList.append(LastPieceStep(self.board, self, move))
        self.engine.removingPiece = None
        x, y = self.coordinates
        self.board[x][y] = "-"

        x, y = self.engine.pieceStepsList[-1].move
        self.engine.targetTile = self.engine.pieceStepsList[-1].targetTile
        self.board[x][y] = self.engine.pieceStepsList[-1].piece
        self.set_coords(x, y)
        if self.engine.targetTile != "-":
            self.engine.removingPiece = self.engine.targetTile
            self.enemy.pieces.remove(self.engine.targetTile)

        #print(argPiece.enemy.pieces)

        if self.coordinates == self.engine.kingSquare and y in [1, 5]:
            self.engine.do_castling()

        self.engine.set_king_square(self.get_piece_color())

    #def unmake_move(self):
    #    lastStep = self.engine.pieceStepsList[-1]
    #    lastStep.piece.alreadyMoved = lastStep.alreadyMoved
#
    #    for i, j in itertools.product(range(8), range(8)):
    #        self.board[i][j] = lastStep.board[i][j]
    #        if self.board[i][j] != "-":
    #            lastStep.board[i][j].set_coords(i, j)
#
    #    if lastStep.targetTile != "-":
    #        lastStep.targetTile.player.pieces.append(lastStep.targetTile)
#
    #    self.engine.pieceStepsList.pop(-1)

    def computer_move(self):
        """

        :return: With a random move of a random enemy piece
        """
        start_time = time.time()
        bestPieceWithMove = self.engine.ai.minimax(self.enemy, 3, False, -9999, 9999)
        print(f"--- {time.time() - start_time} seconds ---")
        #print(bestPieceWithMove[0])
        #print(self.board)

        compPiece = bestPieceWithMove[1][0] #self.engine.bestPieceWithMove[0]
        compMove = bestPieceWithMove[1][1] #self.engine.bestPieceWithMove[1]

        #print(compPiece.availableMoves)
        compPiece.make_move(compMove)

        removingPiece = compPiece.engine.removingPiece
        if removingPiece is not None:
            compPiece.pieceLayout.remove_widget(removingPiece)

        return compPiece, compMove

    # getters, setters
    def set_piece_color(self, color):
        self.pieceColor = color

    def set_engine(self, engine, layout):
        self.engine = engine
        self.board = self.engine.board

        self.player = self.engine.player1 if self.get_piece_color() == 'b' else self.engine.player2
        self.enemy = self.engine.player2 if self.player == self.engine.player1 else self.engine.player1

        #self.careTaker = CareTaker(self.engine)

        self.pieceLayout = layout

    def get_piece_color(self):
        return self.pieceColor

    def set_coords(self, x, y):
        self.coordinates = (x, y)

    def is_already_moved(self, moved):
        self.alreadyMoved = moved



