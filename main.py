from kivy.clock import Clock
from kivy.config import Config
from kivy.app import App
from kivy.graphics.svg import Window
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen

from gameEngine import GameEngine

# Configurate window settings
Window.clearcolor = (0.16, 0.12, 0.09, 0.7)
Window.size = (720, 860)
#Config.set('graphics', 'width', '720')
#Config.set('graphics', 'height', '860')


# Config.set('graphics', 'resizable', '0')


class ChessBoardUI:
    tile_size = 80

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gameEng = GameEngine()
        self.board = None  # self.gameEng.board
        self.layout = FloatLayout() #self.gameEng.layout
        self.offset = 0

        self.draw_board()
        self.draw_pieces()

        # self.on_start()
    def draw_board(self):
        for i in range(8):
            for j in range(8):
                color = 'square brown dark' if (i + j) % 2 == 0 else 'square brown light'
                self.layout.add_widget(Image(source=f'128h/{color}_png_128px.png',
                                             pos=(self.offset + self.tile_size * i, self.offset + self.tile_size * j),
                                             size_hint=(None, None),
                                             size=(self.tile_size, self.tile_size)))

    def draw_pieces(self):
        self.gameEng.createBoard()
        self.board = self.gameEng.board

        for i in range(8):
            for j in range(8):
                if self.board[i][j] != '-':
                    currPiece = self.board[i][j]
                    currPiece.source = f'128h/{currPiece.get_piece_color()}_{currPiece}_png_128px.png'
                    currPiece.pos = (self.offset + self.tile_size * i, self.offset + self.tile_size * j)

                    currPiece.set_engine(self.gameEng, self.layout)

                    self.layout.add_widget(currPiece)

    def new_game(self):
        print(self.layout)
        self.layout.clear_widgets()
        self.gameEng = GameEngine()
        self.draw_board()
        self.board = None
        #self.layout = self.gameEng.layout
        print(self.layout)
        self.draw_pieces()
        print(self.board)


class NewGameButton(Button):
    def __init__(self, cb):
        super(NewGameButton, self).__init__()
        self.chessboard = cb

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            print('down')
            self.chessboard.new_game()

        return super(NewGameButton, self).on_touch_down(touch)


class MainScreen(Screen):
    pass


class GameScreen(Screen):
    pass


class ChessApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen())
        gm = GameScreen()
        chessBoard = ChessBoardUI()

        layout2 = FloatLayout()
        layout2.add_widget(NewGameButton(chessBoard))
        layout2.add_widget(chessBoard.layout)

        gm.add_widget(layout2)
        sm.add_widget(gm)
        
        return sm


if __name__ == "__main__":
    ChessApp().run()
