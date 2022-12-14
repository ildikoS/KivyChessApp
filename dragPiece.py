from kivy.properties import StringProperty
from kivy.uix.behaviors import DragBehavior
from kivy.uix.image import Image
from kivy.uix.popup import Popup

import attributesconf
from piece import Piece

tile_size = attributesconf.tile_size


class DragPiece(DragBehavior, Image, Piece):
    def __init__(self, **kwargs):
        super(DragPiece, self).__init__(**kwargs)
        self.outlines = []
        self.grabbed = False
        self.offset = 0

    def on_touch_up(self, touch):
        super(DragPiece, self).on_touch_up(touch)

        centerX = round(self.get_center_x()) // tile_size
        centerY = round(self.get_center_y()) // tile_size

        if (centerX, centerY) in self.availableMoves and not self.engine.isGameOver and self.get_piece_color() == "w":
            if self.grabbed:
                self.make_move((centerX, centerY))

                self.change_pawn_to_queen(centerX, centerY)

                removingPiece = self.removingPiece
                if removingPiece is not None:
                    self.pieceLayout.remove_widget(removingPiece)

                self.is_already_moved(True)
                self.check_checkmate()

                if not self.engine.isGameOver:
                    print(self.board)
                    computerMove = self.computer_move()
                    removingPiece = computerMove[0].removingPiece
                    if removingPiece is not None:
                        computerMove[0].pieceLayout.remove_widget(removingPiece)
                    computerMove[0].is_already_moved(True)
                    computerMove[0].change_pawn_to_queen(computerMove[1][0], computerMove[1][1])
                    computerMove[0].check_checkmate()

                self.engine.set_all_piece_center()
        else:
            self.set_center(self, self.coordinates[0], self.coordinates[1])

        if self.grabbed:
            self.grabbed = False

        for outline in self.outlines:
            self.pieceLayout.remove_widget(outline)

    def on_touch_down(self, touch):
        super(DragPiece, self).on_touch_down(touch)

        if self.collide_point(*touch.pos) and not self.engine.isGameOver and self.get_piece_color() == "w":
            self.generate_moves()
            self.engine.legal_moves(self, self.enemy)
            self.grabbed = True
            self.drawAvailablePositions()

    def drawAvailablePositions(self):
        for move in self.availableMoves:
            uiOutline = Image(source='imgs/outline_circ.png',
                              pos=(move[0] * tile_size+self.offset, move[1] * tile_size+self.offset),
                              size_hint=(None, None),
                              size=(tile_size, tile_size))
            self.outlines.append(uiOutline)
            self.pieceLayout.add_widget(uiOutline)

    def set_center(self, piece, centerX, centerY):
        uiTile = (tile_size // 2) + self.offset
        piece.set_center_x(centerX * tile_size + uiTile)
        piece.set_center_y(centerY * tile_size + uiTile)

    def change_pawn_to_queen(self, centerX, centerY):
        pawn_to_queen = self.engine.is_pawn_changed(self)
        if pawn_to_queen is not None:
            self.pieceLayout.add_widget(pawn_to_queen[1])
            self.pieceLayout.remove_widget(pawn_to_queen[0])
            self.set_center(pawn_to_queen[1], centerX, centerY)

    def check_checkmate(self):
        if self.engine.is_checkmate(self.enemy):
            self.engine.isGameOver = True
            print(f"CHECK MATE, winner is: {self.get_piece_color()}")
            popup = GameEndPopup()
            if self.get_piece_color() == "w":
                self.player.numberOfWins += 1
            else:
                self.enemy.numberOfWins += 1
            winner = "Feh??r J??t??kos (??n)" if self.get_piece_color() == "w" else "Fekete J??t??kos (G??p)"
            popup.text = f"Nyertes: {winner}, {self.player.numberOfWins} - {self.enemy.numberOfWins}"
            popup.open()


class GameEndPopup(Popup):
    text = StringProperty('')
