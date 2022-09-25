from kivy.app import App
from kivy.graphics import Rectangle, Color
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget


class ChessBoard(GridLayout):
    board = [[0 if (x + y) % 2 == 0 else 1 for x in range(8)] for y in range(8)]
    print(board)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 8
        self.rows = 8

        for i in range(8):
            for j in range(8):
                if self.board[i][j] == 1:
                    self.canvas.add(Color(0.43, 0.26, 0))
                else:
                    self.canvas.add(Color(0.92, 0.85, 0.72))
                self.canvas.add(Rectangle(pos=((70*i)+100, (70*j)+20), size=(70, 70)))


class ChessApp(App):
    def build(self):
        return ChessBoard()


if __name__ == "__main__":
    ChessApp().run()
