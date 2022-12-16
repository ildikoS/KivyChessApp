from kivy.config import Config
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen


# Configurate window settings
import attributesconf
from chessboardui import ChessBoardUI
from gamebuttons import NewGameButton, ReStepButton

Config.set('graphics', 'width', '640')
Config.set('graphics', 'height', '950')
#Config.set('graphics', 'resizable', '0')


class MainScreen(Screen):
    pass


class GameScreen(Screen):
    pass


class PracticeScreen(Screen):
    pass


def set_layout(layout, board):
    layout.add_widget(NewGameButton(board))
    layout.add_widget(ReStepButton(board))
    layout.add_widget(board.layout)


class ChessApp(App):
    def build(self):
        screenManager = ScreenManager()
        mainLayout = FloatLayout()
        practiceLayout = FloatLayout()

        chessBoard = ChessBoardUI(attributesconf.mainFEN)
        practiceBoard = ChessBoardUI(attributesconf.get_random_FEN())

        set_layout(mainLayout, chessBoard)
        set_layout(practiceLayout, practiceBoard)

        gameScreen = GameScreen()
        practiceScreen = PracticeScreen()
        gameScreen.add_widget(mainLayout)
        practiceScreen.add_widget(practiceLayout)

        screenManager.add_widget(MainScreen())
        screenManager.add_widget(gameScreen)
        screenManager.add_widget(practiceScreen)

        return screenManager


if __name__ == "__main__":
    ChessApp().run()
