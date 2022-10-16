from kivy.config import Config
from kivy.app import App
from kivy.graphics import Rectangle, Color, Callback
from kivy.uix.behaviors import DragBehavior
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget

Config.set('graphics', 'width', '560')
Config.set('graphics', 'height', '560')
#Config.set('graphics', 'resizable', '0')


class Piece:

    def __init__(self):
        self.color = None

    def setColor(self, color):
        self.color = color

    #def position(self, x, y):
    #    self.x = x
    #    self.y = y


def positionsFromFEN(fen_string):
    board = []
    innerBoard = []
    for char in fen_string.split()[0]:
        if char == '/':
            board.append(innerBoard)
            innerBoard = []
        elif char.isdigit():
            innerBoard.extend('-' * int(char))
        else:
            innerBoard.append(char)

    print(board)
    return board

class DarkTile(Widget):
    pass

class LightTile(Widget):
    pass

class DragLabel(DragBehavior, Label):
    def on_touch_up(self, touch):
        super(DragLabel, self).on_touch_up(touch)

        print("touch up")

#class ChessBoard(FloatLayout):
#    layout = GridLayout(cols=8, rows=8)
#    layout2 = GridLayout(cols=8, rows=8)
#    #board = [[0 if (x + y) % 2 == 0 else 1 for x in range(8)] for y in range(8)]
#    initialFEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR/ w KQkq - 0 1'
#    board = positionsFromFEN(initialFEN)
#
#    def __init__(self, **kwargs):
#        super().__init__(**kwargs)
#        cols, rows = 8, 8
#
#        for i in range(cols):
#            for j in range(rows):
#                if (i + j) % 2 == 0:
#                    self.layout.add_widget(LightTile())
#                else:
#                    self.layout.add_widget(DarkTile())
#                #Rectangle(pos=(tileSize * i, tileSize * j), size=(tileSize, tileSize))
#                if self.board[i][j] != '-':
#                    self.layout2.add_widget(DragLabel(text=self.board[i][j]))
#                else:
#                    self.layout2.add_widget(Label())

class ChessBoard(GridLayout):
    initialFEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR/ w KQkq - 0 1'
    board = positionsFromFEN(initialFEN)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols, self.rows = 8, 8

        #for i in range(8):
        #    for j in range(8):
        #        self.add_widget(DarkTile(pos=(70*i, 70*j))
        #                        if (i + j) % 2 == 0 else LightTile(pos=(70*i, 70*j))) #pos=(70*i, 70*j)
        for i in range(8):
            for j in range(8):
                with self.canvas.before:
                    Color(0.92, 0.85, 0.72) if (i + j) % 2 == 0 else Color(0.43, 0.26, 0)
                    Rectangle(pos=(70*i, 70*j), size=(self.width, self.height))

                self.add_widget(DragLabel(text=self.board[i][j])
                                if self.board[i][j] != '-' else Label())


class ChessApp(App):
    def build(self):
        return ChessBoard()


if __name__ == "__main__":
    ChessApp().run()
