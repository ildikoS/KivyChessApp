from kivy.uix.button import Button


class ReStepButton(Button):
    def __init__(self, cb):
        super(ReStepButton, self).__init__()
        self.chessboard = cb

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            print('down')
            self.chessboard.gameEng.reset_step()
            print(self.chessboard.board)

        return super(ReStepButton, self).on_touch_down(touch)


class NewGameButton(Button):
    def __init__(self, cb):
        super(NewGameButton, self).__init__()
        self.chessboard = cb

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            self.chessboard.new_game()

        return super(NewGameButton, self).on_touch_down(touch)
