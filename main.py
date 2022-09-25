from kivy.app import App
from kivy.uix.widget import Widget


class ChessBoard(Widget):
    cols, rows = 8, 8

    def create_board(self):
        board = [[0 if (x+y) % 2 == 0 else 1 for x in range(self.cols)] for y in range(self.rows)]
        return board


class ChessApp(App):
    def build(self):
        return ChessBoard()


if __name__ == "__main__":
    ChessApp().run()
