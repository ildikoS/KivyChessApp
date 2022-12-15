import itertools

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image

from memento import CareTaker
from gameEngine import GameEngine


class ChessBoardUI:
    tile_size = 80

    def __init__(self, inputFEN, **kwargs):
        super().__init__(**kwargs)
        self.inputFEN = inputFEN
        self.gameEng = GameEngine(inputFEN)
        self.layout = FloatLayout()
        self.boardLayout = FloatLayout()
        self.pieceLayout = FloatLayout() #self.gameEng.layout
        self.offset = 0

        self.draw_board()
        self.create_pieces()
        self.layout.add_widget(self.boardLayout)
        self.layout.add_widget(self.pieceLayout)

    def draw_board(self):
        for i, j in itertools.product(range(8), range(8)):
            color = 'square brown dark' if (i + j) % 2 == 0 else 'square brown light'
            self.boardLayout.add_widget(Image(source=f'imgs/tiles/{color}_png_shadow_128px.png',
                                         pos=(self.offset + self.tile_size * i, self.offset + self.tile_size * j),
                                         size_hint=(None, None),
                                         size=(self.tile_size, self.tile_size)))

    def create_pieces(self):
        self.gameEng.createBoard()

        for i, j in itertools.product(range(8), range(8)):
            if self.gameEng.board[i][j] != '-':
                currPiece = self.gameEng.board[i][j]
                currPiece.source = f'imgs/pieces/{currPiece.get_piece_color()}_{currPiece}_png_shadow_128px.png'
                currPiece.pos = (self.offset + self.tile_size * i, self.offset + self.tile_size * j)
                currPiece.set_engine(self.gameEng, self.pieceLayout)

                self.pieceLayout.add_widget(currPiece)

    def redraw_pieces(self):
        self.pieceLayout.clear_widgets()
        for i, j in itertools.product(range(8), range(8)):
            currPiece = self.gameEng.board[i][j]
            if self.gameEng.board[i][j] != '-':
                currPiece.source = f'imgs/pieces/{currPiece.get_piece_color()}_{currPiece}_png_shadow_128px.png'
                self.pieceLayout.add_widget(currPiece)

    def new_game(self):
        self.pieceLayout.clear_widgets()
        self.gameEng = GameEngine(self.inputFEN)
        self.draw_board()
        self.create_pieces()

    def set_all_piece_center(self):
        for i, j in itertools.product(range(8), range(8)):
            if self.gameEng.board[i][j] != '-':
                self.gameEng.board[i][j].set_center(self.gameEng.board[i][j], self.gameEng.board[i][j].coordinates[0],
                                            self.gameEng.board[i][j].coordinates[1])
