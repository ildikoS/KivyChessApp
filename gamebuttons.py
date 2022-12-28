from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup


class ReStepButton(Button):
    def __init__(self, cb):
        super(ReStepButton, self).__init__()
        self.chessboard = cb

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y) and len(self.chessboard.gameEng.pieceStepsList) != 0:
            self.chessboard.gameEng.unmake_move()
            self.chessboard.gameEng.unmake_move()

            self.chessboard.gameEng.fill_piece_list()

            self.chessboard.redraw_pieces()
            self.chessboard.gameEng.set_all_piece_center()

        return super(ReStepButton, self).on_touch_down(touch)


class NewGameButton(Button):
    def __init__(self, cb):
        super(NewGameButton, self).__init__()
        self.chessboard = cb

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            self.chessboard.new_game()

        return super(NewGameButton, self).on_touch_down(touch)


class SettingsButton(Button):
    def __init__(self, cb):
        super(SettingsButton, self).__init__()
        self.chessboard = cb

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            layout = FloatLayout()
            popup = SettingsPopup()
            layout.add_widget(EasyModeButton(self.chessboard, popup))
            layout.add_widget(HardModeButton(self.chessboard, popup))

            popup.add_widget(layout)
            popup.open()

        return super(SettingsButton, self).on_touch_down(touch)


class SettingsPopup(Popup):
    pass


class EasyModeButton(Button):
    def __init__(self, cb, popup):
        super(EasyModeButton, self).__init__()
        self.chessboard = cb
        self.popup = popup

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            self.chessboard.gameEng.ai.set_depth(2)
            self.popup.dismiss()
            print(self.chessboard.gameEng.ai.depth)

        return super(EasyModeButton, self).on_touch_down(touch)


class HardModeButton(Button):
    def __init__(self, cb, popup):
        super(HardModeButton, self).__init__()
        self.chessboard = cb
        self.popup = popup

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            self.chessboard.gameEng.ai.set_depth(3)
            self.popup.dismiss()
            print(self.chessboard.gameEng.ai.depth)

        return super(HardModeButton, self).on_touch_down(touch)