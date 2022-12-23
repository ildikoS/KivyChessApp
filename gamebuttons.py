import itertools

from kivy.uix.button import Button


class ReStepButton(Button):
    def __init__(self, cb):
        super(ReStepButton, self).__init__()
        self.chessboard = cb

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            #print('down')

            #print(f"GOMB MEGNYOMÁS ELŐTT: {self.chessboard.gameEng.board}")
            if len(self.chessboard.gameEng.pieceStepsList) != 0:
                self.chessboard.gameEng.unmake_move()
                self.chessboard.gameEng.unmake_move()

                self.chessboard.gameEng.fill_piece_list()

                self.chessboard.redraw_pieces()
                self.chessboard.set_all_piece_center()
            #print(f"GOMB MEGNYOMÁS UTÁN: {self.chessboard.gameEng.board}")

        return super(ReStepButton, self).on_touch_down(touch)


class NewGameButton(Button):
    def __init__(self, cb):
        super(NewGameButton, self).__init__()
        self.chessboard = cb

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            self.chessboard.new_game()

        return super(NewGameButton, self).on_touch_down(touch)