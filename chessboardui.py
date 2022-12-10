import itertools

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image

from gameEngine import GameEngine


class ChessBoardUI:
    tile_size = 80

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gameEng = GameEngine()
        self.layout = FloatLayout() #self.gameEng.layout
        self.board = None  # self.gameEng.board
        self.offset = 0

        self.draw_board()
        self.draw_pieces()

    def draw_board(self):
        for i, j in itertools.product(range(8), range(8)):
            color = 'square brown dark' if (i + j) % 2 == 0 else 'square brown light'
            self.layout.add_widget(Image(source=f'128h/{color}_png_128px.png',
                                         pos=(self.offset + self.tile_size * i, self.offset + self.tile_size * j),
                                         size_hint=(None, None),
                                         size=(self.tile_size, self.tile_size)))

    def draw_pieces(self):
        self.gameEng.createBoard()
        self.board = self.gameEng.board

        for i, j in itertools.product(range(8), range(8)):
            if self.board[i][j] != '-':
                currPiece = self.board[i][j]
                currPiece.source = f'128h/{currPiece.get_piece_color()}_{currPiece}_png_128px.png'
                currPiece.pos = (self.offset + self.tile_size * i, self.offset + self.tile_size * j)

                currPiece.set_engine(self.gameEng, self.layout)

                self.layout.add_widget(currPiece)

    def new_game(self):
        self.layout.clear_widgets()
        self.gameEng = GameEngine()
        self.board = None
        self.draw_board()
        self.draw_pieces()
