from kivy.graphics import Color, Rectangle
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

        for i in range(8):
            for j in range(8):
                currPiece = self.board[i][j]
                if currPiece != '-':
                    pColor = 'w' if currPiece.islower() else 'b'
                    #self.board[i][j] = get_piece(currPiece.lower())
                    #self.board[i][j].set_piece_color(pColor)

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
        self.player = None
        self.board = None
        self.engine = None
        self.downX, self.downY = None, None
        self.pieceColor = None

    def set_engine(self, engine):
        self.engine = engine
        self.board = self.engine.board

        self.player = self.engine.player1 if self.get_piece_color() == 'b' else self.engine.player2
        self.enemy = self.engine.player2 if self.player == self.engine.player1 else self.engine.player1

    def on_touch_up(self, touch):
        super(DragPiece, self).on_touch_up(touch)

        tx, ty = round(self.get_center_x()), round(self.get_center_y())
        centerX = (tx // tile_size)
        centerY = (ty // tile_size)
        uiTile = (tile_size // 2)
        self.set_center_x(centerX * tile_size + uiTile)
        self.set_center_y(centerY * tile_size + uiTile)

        if self.collide_point(*touch.pos):
            self.board[self.downX//tile_size][self.downY//tile_size] = '-'
            self.board[centerX][centerY] = self
            print(self.board)


        #for idx, enemyPiece in enumerate(self.engine.player1.pieces):
        #    if self.collide_point(*touch.pos) \
        #            and self.collide_point(enemyPiece.get_center_x(), enemyPiece.get_center_y()):
        #        print(f"{enemyPiece} was removed")
        #        print("---------")
        #        self.engine.player1.pieces.remove(enemyPiece)
        #        self.layout.remove_widget(enemyPiece)
#
        #if self.collide_point(*touch.pos):
        #    if centerX != self.downX or centerY != self.downY:
        #        print("moved away from prev pos")
        #        # enemy = player1 if enemy == player2 else player2
        #    print(f"centerX={centerX} and downX={self.downX}")
        #    print(f"centerY={centerY} and downY={self.downY}")

    def on_touch_down(self, touch):
        super(DragPiece, self).on_touch_down(touch)

        self.downX, self.downY = round(self.get_center_x()), round(self.get_center_y())
        if self.collide_point(*touch.pos):
            self.generate_moves(self.downX//tile_size, self.downY//tile_size)
            print(self.availableMoves)

            for move in self.availableMoves:
                with self.canvas.before:
                    Color(0.1, 0.8, 0.1, 0.4)
                    Rectangle(pos=(move[0]*tile_size, move[1]*tile_size),
                              size=(tile_size, tile_size))

    def isInside(self, x, y):
        return 0 <= x < 8 and 0 <= y < 8

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

    availableMoves = []

    def generate_moves(self, startX, startY):
        # tuples = [(-1, -1), (-1, 0), (0, -1), (1, 1), (1, 0), (0, 1), (-1, 1), (1, -1)]
        self.availableMoves = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                targetX, targetY = startX + i, startY + j
                if self.isInside(targetX, targetY) and self.board[targetX][targetY] not in self.player.pieces:
                    self.availableMoves.append((targetX, targetY))
                    #print(self.board[targetY][targetX])


class Queen(DragPiece):
    def __str__(self):
        return "queen"

    availableMoves = []

    def generate_moves(self, startX, startY):
        # tuples = [(-1, -1), (-1, 0), (0, -1), (1, 1), (1, 0), (0, 1), (-1, 1), (1, -1)]
        availableMoves = []

        pass

        """for i in range(-1, 1):
            for j in range(-1, 1):
                targetX, targetY = startX + i, startY + j
                if self.board[targetX][targetY] == empty or board[targetX][targetY] == any(enemy.pieces):
                    availableMoves.append((targetX, targetY))"""


class Bishop(DragPiece):
    def __str__(self):
        return "bishop"

    availableMoves = []

    def generate_moves(self, startX, startY):
        # tuples = [(-1, -1), (-1, 0), (0, -1), (1, 1), (1, 0), (0, 1), (-1, 1), (1, -1)]
        availableMoves = []

        pass


class Knight(DragPiece):
    def __str__(self):
        return "knight"

    availableMoves = []

    def generate_moves(self, startX, startY):
        tuples = [(-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (1, -2), (-1, 2), (1, 2)]

        self.availableMoves = []
        for x, y in tuples:
            targetX, targetY = startX + x, startY + y
            if self.isInside(targetX, targetY) and self.board[targetX][targetY] not in self.player.pieces:
                self.availableMoves.append((targetX, targetY))
                # print(self.board[targetY][targetX])


class Rook(DragPiece):
    def __str__(self):
        return "rook"

    availableMoves = []

    def generate_moves(self, startX, startY):
        # tuples = [(-1, -1), (-1, 0), (0, -1), (1, 1), (1, 0), (0, 1), (-1, 1), (1, -1)]
        availableMoves = []

        pass


class Pawn(DragPiece):
    def __str__(self):
        return "pawn"

    availableMoves = []

    def generate_moves(self, startX, startY):
        # tuples = [(-1, -1), (-1, 0), (0, -1), (1, 1), (1, 0), (0, 1), (-1, 1), (1, -1)]
        self.availableMoves = []

        toMove = 2 #if alreadyMoved else 3

        for i in range(toMove):
            if self.get_piece_color() == 'w':
                targetY = startY + toMove
                targetX = startX
                if self.board[startX-1][startY+1] in self.enemy.pieces:
                    targetX -= 1
                    self.availableMoves.append((targetX, startY+1))
                if self.board[startX+1][startY+1] in self.enemy.pieces:
                    targetX += 1
                    self.availableMoves.append((targetX, startY+1))

                if self.board[startX][targetY] == '-':
                    self.availableMoves.append((targetX, targetY))
                print(self.board[startX][targetY]) #IT SHOULD BE FIXED  !!!!!!!!!!!!!!!!!!!!!!!!!!!!