import itertools

from kivy.properties import StringProperty
from kivy.uix.behaviors import DragBehavior
from kivy.uix.image import Image
from kivy.uix.popup import Popup

from piece import Piece

tile_size = 80


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

        #if self.grabbed:
        #    #print(self.get_center_x())
        #    #print(round(self.get_center_x()))
        #    print(round(self.get_center_x()) // tile_size)
        #    #print((round(self.get_center_x()) // tile_size) + 35)
        #    print((round(self.get_center_x()) // (tile_size+self.offset)))

        if (centerX, centerY) in self.availableMoves and not self.engine.isGameOver: #and self.get_piece_color() == "w":
            if self.grabbed:
                self.set_center(self, centerX, centerY)

                # TODO: Refactoring
                self.engine.whiteTurn = True

                #self.engine.careTaker.save()
                #self.careTaker.save()
                self.engine.make_move((centerX, centerY), self)
                #print(f"LÉPÉST CSINÁLT GGGGGGG: {self.engine.pieceStepsList}")
                #print(self.engine.pieceStepsList[0].board)
                #print(self.engine.board)
                #print("address of a:", id(self.engine.pieceStepsList[0].board))
                #print("addrss of b", id(self.engine.board))

                self.change_pawn_to_queen(centerX, centerY)

                removingPiece = self.engine.removingPiece
                if removingPiece is not None:
                    self.pieceLayout.remove_widget(removingPiece)
                #print(self.engine.evaluate())

                self.is_already_moved(True)

                if self.engine.is_checkmate(self.enemy):
                    self.engine.isGameOver = True
                    print(f"CHECK MATE, winner is: {self.get_piece_color()}")
                    popup = GameEndPopup()
                    winner = "Fehér Játékos (Te)" if self.get_piece_color() == "w" else "Fekete Játékos (Gép)"
                    popup.text = f"Nyertes: {winner}"
                    popup.open()


                # print(len(self.enemy.pieces))
                # self.engine.unmake_move()
                # print(len(self.enemy.pieces))
                if not self.engine.isGameOver:
                    computerMove = self.computer_move()
                    computerMove[0].is_already_moved(True)
                    computerMove[0].change_pawn_to_queen(computerMove[1][0], computerMove[1][1])
                    self.set_center(computerMove[0], computerMove[1][0], computerMove[1][1])

                # if self.get_piece_color() == "b" else False
                #print(randMove[0].engine.evaluate())
                self.engine.whiteTurn = False
        else:
            self.set_center(self, self.coordinates[0], self.coordinates[1])

        if self.grabbed:
            self.grabbed = False

        for outline in self.outlines:
            self.pieceLayout.remove_widget(outline)

    def on_touch_down(self, touch):
        super(DragPiece, self).on_touch_down(touch)

        if self.collide_point(*touch.pos) and not self.engine.isGameOver: #and self.get_piece_color() == "w":
            self.generate_moves()
            #print(self.availableMoves)
            self.engine.legal_moves(self, self.enemy)
            #print(self.availableMoves)
            self.grabbed = True
            self.drawAvailablePositions()

    def drawAvailablePositions(self):
        for move in self.availableMoves:
            uiOutline = Image(source='128h/outline_circ.png',
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


class GameEndPopup(Popup):
    text = StringProperty('')
