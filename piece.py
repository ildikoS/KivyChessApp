import copy
import random

from kivy.properties import StringProperty
from kivy.uix.behaviors import DragBehavior
from kivy.uix.image import Image
from kivy.uix.label import Label
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


class DragPiece(DragBehavior, Image, Piece):
    def __init__(self, **kwargs):
        super(DragPiece, self).__init__(**kwargs)
        self.outlines = []
        self.grabbed = False
        self.offset = 0

    def on_touch_up(self, touch):
        super(DragPiece, self).on_touch_up(touch)

        centerX = round(self.get_center_x()) // tile_size
        centerY = round(self.get_center_y()) // tile_size

        #if self.grabbed:
        #    #print(self.get_center_x())
        #    #print(round(self.get_center_x()))
        #    print(round(self.get_center_x()) // tile_size)
        #    #print((round(self.get_center_x()) // tile_size) + 35)
        #    print((round(self.get_center_x()) // (tile_size+self.offset)))

        if (centerX, centerY) in self.availableMoves and not self.engine.isGameOver: #and self.get_piece_color() == "w":
            if self.grabbed:

                # TODO: Refactoring

                prevBoard = self.engine.board
                print(f"{self} MAIN1 made move: {self.engine.prevBoard}")
                self.engine.make_move((centerX, centerY), self)
                self.set_center(self, centerX, centerY)

                self.engine.prevBoard = prevBoard
                print(f"{self} MAIN2 made move: {self.engine.prevBoard}")

                removingPiece = self.engine.removingPiece
                if removingPiece is not None:
                    self.pieceLayout.remove_widget(removingPiece)
                #print(self.engine.evaluate())

                self.is_already_moved(True)

                if self.engine.is_checkmate(self.enemy):
                    self.engine.isGameOver = True
                    print(f"CHECK MATE, winner is: {self.get_piece_color()}")
                    popup = GameEndPopup()
                    winner = "Fehér Játékos (Te)" if self.get_piece_color() == "w" else "Fekete Játékos (Gép)"
                    popup.text = f"Nyertes: {winner}"
                    popup.open()


                # print(len(self.enemy.pieces))
                # self.engine.unmake_move()
                # print(len(self.enemy.pieces))

                self.engine.whiteTurn = True

                computerMove = self.computer_move()
                computerMove[0].is_already_moved(True)
                self.set_center(computerMove[0], computerMove[1][0], computerMove[1][1])

                # if self.get_piece_color() == "b" else False
                #print(randMove[0].engine.evaluate())
                self.engine.whiteTurn = False
        else:
            self.set_center(self, self.coordinates[0], self.coordinates[1])

        if self.grabbed:
            self.grabbed = False

        for outline in self.outlines:
            self.pieceLayout.remove_widget(outline)

    def on_touch_down(self, touch):
        super(DragPiece, self).on_touch_down(touch)

        if self.collide_point(*touch.pos) and not self.engine.isGameOver: #and self.get_piece_color() == "w":
            self.generate_moves()
            #print(self.availableMoves)
            self.engine.legal_moves(self, self.enemy)
            #print(self.availableMoves)
            self.grabbed = True
            self.drawAvailablePositions()

    def drawAvailablePositions(self):
        for move in self.availableMoves:
            uiOutline = Image(source='128h/outline_circ.png',
                              pos=(move[0] * tile_size+self.offset, move[1] * tile_size+self.offset),
                              size_hint=(None, None),
                              size=(tile_size, tile_size))
            self.outlines.append(uiOutline)
            self.pieceLayout.add_widget(uiOutline)

    def set_center(self, piece, centerX, centerY):
        uiTile = (tile_size // 2) + self.offset
        piece.set_center_x(centerX * tile_size + uiTile)
        piece.set_center_y(centerY * tile_size + uiTile)


class GameEndPopup(Popup):
    text = StringProperty('')


class King(DragPiece):
    def __str__(self):
        return "king"

    def generate_moves(self):
        self.availableMoves = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                targetX, targetY = self.coordinates[0] + i, self.coordinates[1] + j
                if self.isInside(targetX, targetY) and self.board[targetX][targetY] not in self.player.pieces:
                    self.availableMoves.append((targetX, targetY))

        # Castling
        # if not self.alreadyMoved and self.board[startX][startY+2] == "-":
        #    self.availableMoves.append((startX, startY+2))


class Queen(DragPiece):
    def __str__(self):
        return "queen"

    def generate_moves(self):
        self.availableMoves = []

        self.genSlidingMove(1, 1)
        self.genSlidingMove(1, -1)

        self.genSlidingMove(-1, 1)
        self.genSlidingMove(-1, -1)

        self.genSlidingMove(1, 0)
        self.genSlidingMove(0, 1)

        self.genSlidingMove(-1, 0)
        self.genSlidingMove(0, -1)


class Knight(DragPiece):
    def __str__(self):
        return "knight"

    def generate_moves(self):
        tuples = [(-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (1, -2), (-1, 2), (1, 2)]

        self.availableMoves = []
        for x, y in tuples:
            targetX, targetY = self.coordinates[0] + x, self.coordinates[1] + y
            if self.isInside(targetX, targetY) and self.board[targetX][targetY] not in self.player.pieces:
                self.availableMoves.append((targetX, targetY))


class Bishop(DragPiece):  # futó
    def __str__(self):
        return "bishop"

    def generate_moves(self):
        self.availableMoves = []

        self.genSlidingMove(1, 1)
        self.genSlidingMove(1, -1)

        self.genSlidingMove(-1, 1)
        self.genSlidingMove(-1, -1)


class Rook(DragPiece):  # bástya
    def __str__(self):
        return "rook"

    def generate_moves(self):
        self.availableMoves = []

        self.genSlidingMove(1, 0)
        self.genSlidingMove(0, 1)

        self.genSlidingMove(-1, 0)
        self.genSlidingMove(0, -1)


class Pawn(DragPiece):
    def __str__(self):
        return "pawn"

    def generate_moves(self):
        self.availableMoves = []
        startX = self.coordinates[0]
        startY = self.coordinates[1]

        toMove = 2 if self.alreadyMoved else 3

        for i in range(1, toMove):
            if self.get_piece_color() == 'w':
                self.genCrossMove(startX + 1, startY + 1)
                self.genCrossMove(startX + 1, startY - 1)

                if self.board[startX + i][startY] != '-':
                    break
                self.availableMoves.append((startX + i, startY))
            else:
                self.genCrossMove(startX - 1, startY + 1)
                self.genCrossMove(startX - 1, startY - 1)

                if self.board[startX - i][startY] != '-':
                    break
                self.availableMoves.append((startX - i, startY))

    def genCrossMove(self, targetX, targetY):
        if self.isInside(targetX, targetY) and self.board[targetX][targetY] in self.enemy.pieces:
            self.availableMoves.append((targetX, targetY))
