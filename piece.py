from kivy.graphics import Color, Ellipse
from kivy.uix.behaviors import DragBehavior
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image

from gameEngine import positions_from_FEN, Player


def get_piece(char):
    if char == 'k': return King()
    if char == 'q': return Queen()
    if char == 'b': return Bishop()
    if char == 'n': return Knight()
    if char == 'r': return Rook()
    if char == 'p': return Pawn()


class GameEngine:
    initialFEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR/ w KQkq - 0 1'
    board = positions_from_FEN(initialFEN)
    blacks = []
    whites = []

    def __init__(self):
        self.player1 = None
        self.player2 = None

        self.layout = FloatLayout()

        for i in range(8):
            for j in range(8):
                currPiece = self.board[i][j]
                if currPiece != '-':
                    pColor = 'w' if currPiece.islower() else 'b'
                    # self.board[i][j] = get_piece(currPiece.lower())
                    # self.board[i][j].set_piece_color(pColor)

                    self.board[i][j] = f'{pColor}|{currPiece}'

                    self.blacks.append(self.board[i][j]) \
                        if pColor == 'b' else self.whites.append(self.board[i][j])
        print(self.board)
        self.player1 = Player(self.blacks)
        self.player2 = Player(self.whites)


tile_size = 70


class DragPiece(DragBehavior, Image):
    def __init__(self, **kwargs):
        super(DragPiece, self).__init__(**kwargs)
        self.ellipses = []
        self.player = None
        self.board = None
        self.engine = None
        self.downX, self.downY = None, None
        self.pieceColor = None
        self.availableMoves = []

    def set_engine(self, engine):
        self.engine = engine
        self.board = self.engine.board

        self.player = self.engine.player1 if self.get_piece_color() == 'b' else self.engine.player2
        self.enemy = self.engine.player2 if self.player == self.engine.player1 else self.engine.player1

        self.pieceLayout = self.engine.layout

    def on_touch_up(self, touch):
        super(DragPiece, self).on_touch_up(touch)

        tx, ty = round(self.get_center_x()), round(self.get_center_y())
        centerX = (tx // tile_size)
        centerY = (ty // tile_size)
        uiTile = (tile_size // 2)
        if (centerX, centerY) in self.availableMoves:
            self.set_center_x(centerX * tile_size + uiTile)
            self.set_center_y(centerY * tile_size + uiTile)
        else:
            self.set_center_x((self.downX // tile_size) * tile_size + uiTile)
            self.set_center_y((self.downY // tile_size) * tile_size + uiTile)

        if self.collide_point(*touch.pos):
            self.board[self.downX // tile_size][self.downY // tile_size] = '-'
            self.board[centerX][centerY] = self
            print(self.board)

        for ellipse in self.ellipses:
            print(ellipse)
            print(self.canvas.children)
            self.canvas.children.remove(ellipse)
        self.canvas.ask_update()

        # for idx, enemyPiece in enumerate(self.engine.player1.pieces):
        #    if self.collide_point(*touch.pos) \
        #            and self.collide_point(enemyPiece.get_center_x(), enemyPiece.get_center_y()):
        #        print(f"{enemyPiece} was removed")
        #        print("---------")
        #        self.engine.player1.pieces.remove(enemyPiece)
        #        self.layout.remove_widget(enemyPiece)

    #
    # if self.collide_point(*touch.pos):
    #    if centerX != self.downX or centerY != self.downY:
    #        print("moved away from prev pos")
    #        # enemy = player1 if enemy == player2 else player2
    #    print(f"centerX={centerX} and downX={self.downX}")
    #    print(f"centerY={centerY} and downY={self.downY}")

    def on_touch_down(self, touch):
        super(DragPiece, self).on_touch_down(touch)

        self.downX, self.downY = round(self.get_center_x()), round(self.get_center_y())
        if self.collide_point(*touch.pos):
            self.generate_moves(self.downX // tile_size, self.downY // tile_size)
            print(self.availableMoves)

        for move in self.availableMoves:
            with self.canvas:
                Color(0.1, 0.8, 0.1, 0.4)
                ellipse = Ellipse(pos=(move[0]*tile_size, move[1]*tile_size), size=(tile_size, tile_size))
                self.pieceLayout.add_widget(ellipse)

    def isInside(self, x, y):
        return 0 <= x < 8 and 0 <= y < 8

    def genSlidingMove(self, X, Y):
        if self.isInside(X, Y) and self.board[X][Y] not in self.player.pieces:
            self.availableMoves.append((X, Y))
        #return self.board[X][Y] in self.enemy.pieces

    def set_piece_color(self, color):
        self.pieceColor = color

    def get_piece_color(self):
        return self.pieceColor


# class Piece(Image):
#    def __init__(self, **kwargs):
#        super(Piece, self).__init__(**kwargs)
# self.color = None

# def setColor(self, color):
#    self.color = color

# def position(self, x, y):
#    self.x = x
#    self.y = y


class King(DragPiece):
    def __str__(self):
        return "king"

    def generate_moves(self, startX, startY):
        # tuples = [(-1, -1), (-1, 0), (0, -1), (1, 1), (1, 0), (0, 1), (-1, 1), (1, -1)]
        self.availableMoves = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                targetX, targetY = startX + i, startY + j
                if self.isInside(targetX, targetY) and self.board[targetX][targetY] not in self.player.pieces:
                    self.availableMoves.append((targetX, targetY))
                    # print(self.board[targetY][targetX])


class Queen(DragPiece):
    def __str__(self):
        return "queen"

    def generate_moves(self, startX, startY):

        self.availableMoves = []


class Knight(DragPiece):
    def __str__(self):
        return "knight"

    def generate_moves(self, startX, startY):
        tuples = [(-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (1, -2), (-1, 2), (1, 2)]

        self.availableMoves = []
        for x, y in tuples:
            targetX, targetY = startX + x, startY + y
            if self.isInside(targetX, targetY) and self.board[targetX][targetY] not in self.player.pieces:
                self.availableMoves.append((targetX, targetY))
                # print(self.board[targetY][targetX])


class Bishop(DragPiece): #futó
    def __str__(self):
        return "bishop"

    def generate_moves(self, startX, startY):
        self.availableMoves = []

        for i in range(8):
            self.genSlidingMove(startX + i, startY + i)
            self.genSlidingMove(startX + i, startY - i)

            self.genSlidingMove(startX - i, startY + i)
            self.genSlidingMove(startX - i, startY - i)


class Rook(DragPiece): #bástya
    def __str__(self):
        return "rook"

    def generate_moves(self, startX, startY):
        self.availableMoves = []

        for i in range(8):
            self.genSlidingMove(startX + i, startY)
            self.genSlidingMove(startX, startY + i)

            self.genSlidingMove(startX - i, startY)
            self.genSlidingMove(startX, startY - i)


class Pawn(DragPiece):
    def __str__(self):
        return "pawn"

    def generate_moves(self, startX, startY):
        # tuples = [(-1, -1), (-1, 0), (0, -1), (1, 1), (1, 0), (0, 1), (-1, 1), (1, -1)]
        self.availableMoves = []

        toMove = 2  # if alreadyMoved else 3

        for i in range(toMove):
            if self.get_piece_color() == 'w':
                targetY = startY + toMove
                targetX = startX
                if self.board[startX - 1][startY + 1] in self.enemy.pieces:
                    targetX -= 1
                    self.availableMoves.append((targetX, startY + 1))
                if self.board[startX + 1][startY + 1] in self.enemy.pieces:
                    targetX += 1
                    self.availableMoves.append((targetX, startY + 1))

                if self.board[startX][targetY] == '-':
                    self.availableMoves.append((targetX, targetY))
                print(self.board[startX][targetY])  # IT SHOULD BE FIXED  !!!!!!!!!!!!!!!!!!!!!!!!!!!!
