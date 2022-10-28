from kivy.config import Config
from kivy.app import App
from kivy.uix.behaviors import DragBehavior
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image

Config.set('graphics', 'width', '560')
Config.set('graphics', 'height', '560')
Config.set('graphics', 'resizable', '0')

tile_size = 70
layout = FloatLayout()

class Piece:
    def __init__(self):
        self.color = None

    def setColor(self, color):
        self.color = color

    #def position(self, x, y):
    #    self.x = x
    #    self.y = y

class Player:
    def __init__(self, pieces):
        self.pieces = pieces


blacks = []
whites = []
pieces = list()
player1 = Player(blacks)
player2 = Player(whites)
enemy = player1


class DragPiece(DragBehavior, Image):
    def __init__(self, **kwargs):
        super(DragPiece, self).__init__(**kwargs)
        self.downX, self.downY = None, None

    def __str__(self):
        return self.source

    def on_touch_up(self, touch):
        super(DragPiece, self).on_touch_up(touch)

        tx, ty = round(self.get_center_x()), round(self.get_center_y())
        centerX = (tx // tile_size) * tile_size + (tile_size // 2)
        centerY = (ty // tile_size) * tile_size + (tile_size // 2)
        self.set_center_x(centerX)
        self.set_center_y(centerY)

        for idx, piece in enumerate(enemy.pieces):
            if self.collide_point(*touch.pos) and self.collide_point(piece.get_center_x(), piece.get_center_y()):
                print(f"{piece} was removed")
                print("---------")
                enemy.pieces.remove(piece)
                layout.remove_widget(piece)

        if self.collide_point(*touch.pos):
            if centerX != self.downX or centerY != self.downY:
                print("moved away from prev pos")
                #enemy = player1 if enemy == player2 else player2
            print(f"centerX={centerX} and downX={self.downX}")
            print(f"centerY={centerY} and downY={self.downY}")

    def on_touch_down(self, touch):
        super(DragPiece, self).on_touch_down(touch)
        self.downX, self.downY = round(self.get_center_x()), round(self.get_center_y())


def positions_from_FEN(fenStr):
    board = []
    innerBoard = []
    for char in fenStr.split()[0]:
        if char == '/':
            board.append(innerBoard)
            innerBoard = []
        elif char.isdigit():
            innerBoard.extend('-' * int(char))
        else:
            innerBoard.append(char)

    print(board)
    return board


piecesDict = {
    'k': "king", #King()
    'q': "queen",
    'b': "bishop",
    'n': "knight",
    'r': "rook",
    'p': "pawn"
}

class ChessBoard():
    initialFEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR/ w KQkq - 0 1'
    board = positions_from_FEN(initialFEN)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = layout

        """drawing board with pieces"""
        for i in range(8):
            for j in range(8):
                color = 'square brown light' if (i + j) % 2 == 0 else 'square brown dark'
                layout.add_widget(Image(source=f'128h/{color}_png_128px.png',
                                        pos=(tile_size*j, tile_size*i),
                                        size_hint=(0.125, 0.125)))
        self.drawPieces()

    def drawPieces(self):
        for i in range(8):
            for j in range(8):
                pieceColor = 'b'
                if self.board[i][j].islower():
                    pieceColor = 'w'
                piece = piecesDict.get(self.board[i][j].lower())

                if self.board[i][j] != '-':
                    src = f'128h/{pieceColor}_{piece}_png_128px.png'
                    pieceInstance = DragPiece(source=src, pos=(tile_size*j, tile_size*i))
                    layout.add_widget(pieceInstance)

                if pieceColor == 'b':
                    blacks.append(pieceInstance)
                else:
                    whites.append(pieceInstance)

                pieces.append(pieceInstance)


class ChessApp(App):
    def build(self):
        return ChessBoard().layout


if __name__ == "__main__":
    ChessApp().run()
