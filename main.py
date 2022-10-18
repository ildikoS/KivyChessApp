from kivy.config import Config
from kivy.app import App
from kivy.graphics import Rectangle, Color, Line
from kivy.uix.behaviors import DragBehavior
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.widget import Widget

Config.set('graphics', 'width', '560')
Config.set('graphics', 'height', '560')
#Config.set('graphics', 'resizable', '0')

tile_size = 70

class Piece:
    def __init__(self):
        self.color = None

    def setColor(self, color):
        self.color = color

    #def position(self, x, y):
    #    self.x = x
    #    self.y = y


class DragPiece(DragBehavior, Image):
    def on_touch_up(self, touch):
        super(DragPiece, self).on_touch_up(touch)

        tx, ty = round(self.get_center_x()), round(self.get_center_y())
        print(tx)
        print(ty)

        # if tx > ...
        self.set_center_x(round(tx / tile_size) * tile_size - (tile_size // 2))

        # if ty > ...
        self.set_center_y(round(ty / tile_size) * tile_size - (tile_size // 2))

    def on_touch_move(self, touch):
        super(DragPiece, self).on_touch_move(touch)


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


class ChessBoard(GridLayout):
    initialFEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR/ w KQkq - 0 1'
    board = positions_from_FEN(initialFEN)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols, self.rows = 8, 8

        """adding red lines"""
        screen_height = 70*8
        for i in range(screen_height//70):
            with self.canvas:
                Color(1, .1, .1, .9)
                Line(width=2, points=[i*70, 0, i*70, screen_height])
                Line(width=2, points=[0, i*70, screen_height, i*70])

        """drawing board with pieces"""
        for i in range(8):
            for j in range(8):
                with self.canvas.before:
                    Color(0.92, 0.85, 0.72) if (i + j) % 2 == 0 else Color(0.43, 0.26, 0)
                    Rectangle(pos=(70*i, 70*j))

                pieceColor = 'w' if self.board[i][j].islower() else 'b'
                piece = 'king'
                src = f'128h/{pieceColor}_{piece}_png_128px.png'
                self.add_widget(DragPiece(source=src) if self.board[i][j] != '-' else Label())
        #self.add_widget(DragLabel(source='NoShadow/128h/b_king_png_128px.png'))


class ChessApp(App):
    def build(self):
        return ChessBoard()


if __name__ == "__main__":
    ChessApp().run()
