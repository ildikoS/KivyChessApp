from kivy.config import Config
from kivy.app import App
from kivy.uix.behaviors import DragBehavior
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image

import piece

Config.set('graphics', 'width', '560')
Config.set('graphics', 'height', '560')
Config.set('graphics', 'resizable', '0')

tile_size = 70
layout = FloatLayout()


class Player:
    def __init__(self, pieces):
        self.pieces = pieces


blacks = []
whites = []
pieces = list()
player1 = Player(blacks)
player2 = Player(whites)
enemy = player1


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


def get_piece(char):
    if char == 'k': return piece.King()
    if char == 'q': return piece.Queen()
    if char == 'b': return piece.Bishop()
    if char == 'n': return piece.Knight()
    if char == 'r': return piece.Rook()
    if char == 'p': return piece.Pawn()


class ChessBoard:
    initialFEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR/ w KQkq - 0 1'
    board = positions_from_FEN(initialFEN)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = layout

        """drawing board with pieces"""
        for i in range(8):
            for j in range(8):
                color = 'square brown light' if (i + j) % 2 == 0 else 'square brown dark'
                layout.add_widget(Image(source=f'128h/{color}_png_128px.png', pos=(tile_size*j, tile_size*i),
                                        size_hint=(0.125, 0.125)))
        self.draw_pieces()

    def draw_pieces(self):
        for i in range(8):
            for j in range(8):
                filePiece = self.board[i][j]

                if filePiece != '-':
                    currPiece = get_piece(filePiece.lower())
                    pieceColor = 'w' if filePiece.islower() else 'b'
#
                    srcImg = f'128h/{pieceColor}_{currPiece}_png_128px.png'
                    currPiece.source = srcImg
                    currPiece.pos = (tile_size * j, tile_size * i)
                    layout.add_widget(currPiece)

                    blacks.append(currPiece) if pieceColor == 'b' else whites.append(currPiece)
                    pieces.append(currPiece)
        print(blacks)


class ChessApp(App):
    def build(self):
        return ChessBoard().layout


if __name__ == "__main__":
    ChessApp().run()
