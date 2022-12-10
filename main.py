from kivy.config import Config
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen


# Configurate window settings
from chessboardui import ChessBoardUI
from gamebuttons import NewGameButton, ReStepButton

Config.set('graphics', 'width', '720')
Config.set('graphics', 'height', '860')
# Config.set('graphics', 'resizable', '0')


class MainScreen(Screen):
    pass


class GameScreen(Screen):
    pass


class ChessApp(App):
    def build(self):
        screenManager = ScreenManager()
        mainLayout = FloatLayout()
        chessBoard = ChessBoardUI()

        mainLayout.add_widget(NewGameButton(chessBoard))
        mainLayout.add_widget(ReStepButton(chessBoard))
        mainLayout.add_widget(chessBoard.layout)

        gameScreen = GameScreen()
        screenManager.add_widget(MainScreen())
        gameScreen.add_widget(mainLayout)
        screenManager.add_widget(gameScreen)

        return screenManager


if __name__ == "__main__":
    ChessApp().run()
