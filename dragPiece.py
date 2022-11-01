from kivy.uix.behaviors import DragBehavior
from kivy.uix.image import Image

from gameEngine import GameEngine


class DragPiece(DragBehavior, Image):
    def __init__(self, **kwargs):
        super(DragPiece, self).__init__(**kwargs)
        self.downX, self.downY = None, None
        self.pieceColor = None
        self.engine = GameEngine()
        self.layout = self.engine.layout
        print(self.engine.player1.pieces)

    def on_touch_up(self, touch):
        super(DragPiece, self).on_touch_up(touch)

        tx, ty = round(self.get_center_x()), round(self.get_center_y())
        centerX = (tx // tile_size) * tile_size + (tile_size // 2)
        centerY = (ty // tile_size) * tile_size + (tile_size // 2)
        self.set_center_x(centerX)
        self.set_center_y(centerY)

        for idx, enemyPiece in enumerate(enemy.pieces):
            if self.collide_point(*touch.pos) \
                    and self.collide_point(enemyPiece.get_center_x(), enemyPiece.get_center_y()):
                print(f"{enemyPiece} was removed")
                print("---------")
                enemy.pieces.remove(enemyPiece)
                layout.remove_widget(enemyPiece)

        if self.collide_point(*touch.pos):
            if centerX != self.downX or centerY != self.downY:
                print("moved away from prev pos")
                # enemy = player1 if enemy == player2 else player2
            print(f"centerX={centerX} and downX={self.downX}")
            print(f"centerY={centerY} and downY={self.downY}")

    def on_touch_down(self, touch):
        super(DragPiece, self).on_touch_down(touch)

        self.downX, self.downY = round(self.get_center_x()), round(self.get_center_y())

    def set_piece_color(self, color):
        self.pieceColor = color

    def get_piece_color(self):
        return self.pieceColor