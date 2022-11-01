from kivy.config import Config
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image

from piece import GameEngine

Config.set('graphics', 'width', '560')
Config.set('graphics', 'height', '560')
#Config.set('graphics', 'resizable', '0')


class ChessBoardUI:
    tile_size = 70
    layout = FloatLayout()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gameEng = GameEngine()
        self.board = self.gameEng.board

        """drawing board with pieces"""
        for i in range(8):
            for j in range(8):
                color = 'square brown light' if (i + j) % 2 == 0 else 'square brown dark'
                self.layout.add_widget(Image(source=f'128h/{color}_png_128px.png',
                                        pos=(self.tile_size*j, self.tile_size*i),
                                        size_hint=(0.125, 0.125)))

        self.draw_pieces()

    def draw_pieces(self):
        for i in range(8):
            for j in range(8):
                if self.board[i][j] != '-':
                    currPiece = self.board[i][j]

                    currPiece.source = f'128h/{currPiece.get_piece_color()}_{currPiece}_png_128px.png'
                    currPiece.pos = (self.tile_size * j, self.tile_size * i)

                    self.layout.add_widget(currPiece)


class ChessApp(App):
    def build(self):
        return ChessBoardUI().layout


if __name__ == "__main__":
    ChessApp().run()
