from kivy.config import Config
from kivy.app import App
from kivy.graphics import Rectangle, Color
from kivy.uix.widget import Widget

Config.set('graphics', 'width', '560')
Config.set('graphics', 'height', '560')
Config.set('graphics', 'resizable', '0')


class Piece:

    def __init__(self):
        self.color = None

    def setColor(self, color):
        self.color = color

    #def position(self, x, y):
    #    self.x = x
    #    self.y = y


initialFEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'


def positionsFromFEN(fen_string):
    board = []
    for char in fen_string.split()[0]:
        if char == '/':
            pass
        elif char.isdigit():
            board.append('-' * int(char))
        else:
            board.append(char)

    print(board)


class ChessBoard(Widget):
    #board = [[0 if (x + y) % 2 == 0 else 1 for x in range(8)] for y in range(8)]

    positionsFromFEN(initialFEN)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        cols = 8
        rows = 8
        tileSize = 70

        with self.canvas:
            for i in range(cols):
                for j in range(rows):
                    if (i + j) % 2 == 0:
                        Color(0.43, 0.26, 0)
                    else:
                        Color(0.92, 0.85, 0.72)
                    Rectangle(pos=(tileSize * i, tileSize * j), size=(tileSize, tileSize))


class ChessApp(App):
    def build(self):
        return ChessBoard()


if __name__ == "__main__":
    ChessApp().run()
