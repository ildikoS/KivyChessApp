from kivy.uix.behaviors import DragBehavior
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image

from gameEngine import positions_from_FEN, Player


# def generate_moves(startX, startY):
#    #tuples = [(-1, -1), (-1, 0), (0, -1), (1, 1), (1, 0), (0, 1), (-1, 1), (1, -1)]
#    availableMoves = []
#
#    for i in range(-1, 1):
#        for j in range(-1, 1):
#            targetX, targetY = startX + i, startY + j
#            if board[targetX][targetY] == empty or board[targetX][targetY] == any(enemy.pieces):
#                availableMoves.append((targetX, targetY))


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
        for i in range(8):
            for j in range(8):
                currPiece = self.board[i][j]
                if currPiece != '-':
                    pColor = 'w' if currPiece.islower() else 'b'
                    #self.board[i][j] = get_piece(currPiece.lower())
                    #self.board[i][j].set_piece_color(pColor)

                    self.board[i][j] = f'{pColor}|{currPiece}'

                    #self.blacks.append(self.board[i][j]) \
                    #    if self.board[i][j].get_piece_color() == 'b' else self.whites.append(self.board[i][j])
        print(self.board)
    player1 = Player(blacks)
    player2 = Player(whites)


tile_size = 70


class DragPiece(DragBehavior, Image):
    def __init__(self, **kwargs):
        super(DragPiece, self).__init__(**kwargs)
        self.board = None
        self.engine = None
        self.downX, self.downY = None, None
        self.pieceColor = None

    def set_engine(self, engine):
        self.engine = engine
        self.board = self.engine.board

    def on_touch_up(self, touch):
        super(DragPiece, self).on_touch_up(touch)

        tx, ty = round(self.get_center_x()), round(self.get_center_y())
        centerX = (tx // tile_size) * tile_size + (tile_size // 2)
        centerY = (ty // tile_size) * tile_size + (tile_size // 2)
        self.set_center_x(centerX)
        self.set_center_y(centerY)



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

    def set_piece_color(self, color):
        self.pieceColor = color

    def get_piece_color(self):
        return self.pieceColor

    #availableMoves = []

    #def generate_moves(self, startX, startY):
    #    # tuples = [(-1, -1), (-1, 0), (0, -1), (1, 1), (1, 0), (0, 1), (-1, 1), (1, -1)]
    #    self.availableMoves = []
#
    #    print(self.board)
    #    for i in range(-1, 1):
    #        for j in range(-1, 1):
    #            targetX, targetY = startX + i, startY + j
    #            #if self.board[targetX][targetY] == '-': #or self.board[targetX][targetY] == any(self.engine.player2.pieces):
    #            self.availableMoves.append((targetX, targetY))


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
                #if self.board[targetX][targetY] == '-' or self.board[targetX][targetY] == any(self.engine.player2.pieces):
                if 0 <= targetX < 8 and 0 <= targetY < 8 and self.board[targetX][targetY] == '-':
                    self.availableMoves.append((targetX, targetY))


class Queen(DragPiece):
    def __str__(self):
        return "queen"

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

    def generate_moves(self, startX, startY):
        # tuples = [(-1, -1), (-1, 0), (0, -1), (1, 1), (1, 0), (0, 1), (-1, 1), (1, -1)]
        availableMoves = []

        pass


class Knight(DragPiece):
    def __str__(self):
        return "knight"

    def generate_moves(self, startX, startY):
        # tuples = [(-1, -1), (-1, 0), (0, -1), (1, 1), (1, 0), (0, 1), (-1, 1), (1, -1)]
        availableMoves = []

        pass


class Rook(DragPiece):
    def __str__(self):
        return "rook"

    def generate_moves(self, startX, startY):
        # tuples = [(-1, -1), (-1, 0), (0, -1), (1, 1), (1, 0), (0, 1), (-1, 1), (1, -1)]
        availableMoves = []

        pass


class Pawn(DragPiece):
    def __str__(self):
        return "pawn"

    #def generate_moves(self, startX, startY):
    #    # tuples = [(-1, -1), (-1, 0), (0, -1), (1, 1), (1, 0), (0, 1), (-1, 1), (1, -1)]
    #    availableMoves = []

        """
        toMove = 1 if alreadyMoved else 2

        for i in range(toMove):
            if self.get_piece_color() == 'w':
                targetY = startY + toMove
                if board[startX-1][startY+1] == any(enemy.pieces):
                    targetX = startX-1
                    availableMoves.append((targetX, startY+1))
                if board[startX+1][startY+1] == any(enemy.pieces):
                    targetX = startX+1
                    availableMoves.append((targetX, startY+1))

            if board[startX][targetY] == empty:
                availableMoves.append((targetX, targetY))"""
