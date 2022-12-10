import itertools
from kivy.properties import StringProperty
from kivy.uix.behaviors import DragBehavior
from kivy.uix.image import Image
from kivy.uix.popup import Popup

tile_size = 80


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

    def computer_move(self):
        """

        :return: With a random move of a random enemy piece
        """
        #randomPiece = random.choice(self.enemy.pieces)
        #randomPiece.generate_moves()
        #print(randomPiece.availableMoves)

        self.engine.minimax(self.enemy, 1, False, -9999, 9999)

        compPiece = self.engine.bestPieceWithMove[0]
        compMove = self.engine.bestPieceWithMove[1]

       #while not randomPiece.availableMoves:
       #    randomPiece = random.choice(self.enemy.pieces)
       #    randomPiece.generate_moves()
       #randomMove = random.choice(randomPiece.availableMoves)
        # print(f"made a move : {randomPiece} moved to {randomMove}")
        print(compPiece.availableMoves)
        compPiece.engine.make_move(compMove, compPiece)

        removingPiece = compPiece.engine.removingPiece
        if removingPiece is not None:
            compPiece.pieceLayout.remove_widget(removingPiece)

        #isCollide = randomPiece.engine.checkCollision(randomPiece.enemy, randomPiece)
        #if isCollide:
        #    randomPiece.engine.layout.remove_widget(isCollide)
            # randomPiece.enemy.pieces.remove(isCollide)

        return compPiece, compMove

    # getters, setters
    def set_piece_color(self, color):
        self.pieceColor = color

    def set_engine(self, engine, layout):
        self.engine = engine
        self.board = self.engine.board

        self.player = self.engine.player1 if self.get_piece_color() == 'b' else self.engine.player2
        self.enemy = self.engine.player2 if self.player == self.engine.player1 else self.engine.player1

        self.pieceLayout = layout

    def get_piece_color(self):
        return self.pieceColor

    def set_coords(self, x, y):
        self.coordinates = (x, y)

    def is_already_moved(self, moved):
        self.alreadyMoved = moved



