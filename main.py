from kivy.clock import Clock
from kivy.config import Config
from kivy.app import App
from kivy.uix.image import Image

from gameEngine import GameEngine

# Configurate window settings
Config.set('graphics', 'width', '560')
Config.set('graphics', 'height', '560')
Config.set('graphics', 'resizable', '0')


class ChessBoardUI:
    tile_size = 70

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gameEng = GameEngine()
        self.board = None  # self.gameEng.board
        self.layout = self.gameEng.layout

        for i in range(8):
            for j in range(8):
                color = 'square brown dark' if (i + j) % 2 == 0 else 'square brown light'
                self.layout.add_widget(Image(source=f'128h/{color}_png_128px.png',
                                             pos=(self.tile_size * i, self.tile_size * j),
                                             size_hint=(0.125, 0.125)))
        self.draw_pieces()

        #self.on_start()

    def draw_pieces(self):
        self.gameEng.createBoard()
        self.board = self.gameEng.board

        for i in range(8):
            for j in range(8):
                if self.board[i][j] != '-':
                    currPiece = self.board[i][j]
                    currPiece.source = f'128h/{currPiece.get_piece_color()}_{currPiece}_png_128px.png'
                    currPiece.pos = (self.tile_size * i, self.tile_size * j)

                    currPiece.set_engine(self.gameEng)

                    self.layout.add_widget(currPiece)

    def new_game(self):
        self.gameEng = GameEngine()
        self.board = None  # self.gameEng.board
        self.layout = self.gameEng.layout
        self.draw_pieces()

    def on_start(self):
        Clock.schedule_interval(self.callback, 0.5)

    def callback(self):
        print(self)
        #if self.gameEng.is_checkmate(self.gameEng.player1) or self.gameEng.is_checkmate(self.gameEng.player1):
        #    self.gameEng = GameEngine()
        #    self.board = None  # self.gameEng.board
        #    self.layout = self.gameEng.layout
        #    self.draw_pieces()

    Clock.schedule_interval(callback, 0.5)


class ChessApp(App):
    def build(self):
        chessBoard = ChessBoardUI()

        #chessBoard.on_start()
        #Clock.schedule_interval(chessBoard.callback, 0.5)

        return chessBoard.layout


if __name__ == "__main__":
    ChessApp().run()
