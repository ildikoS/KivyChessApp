from kivy.uix.behaviors import DragBehavior
from kivy.uix.image import Image

from main import tile_size, layout, enemy


def generate_moves(startX, startY):
    #tuples = [(-1, -1), (-1, 0), (0, -1), (1, 1), (1, 0), (0, 1), (-1, 1), (1, -1)]
    availableMoves = []

    for i in range(-1, 1):
        for j in range(-1, 1):
            targetX, targetY = startX + i, startY + j
            if board[targetX][targetY] == empty or board[targetX][targetY] == any(enemy.pieces):
                availableMoves.append((targetX, targetY))


class DragPiece(DragBehavior, Image):
    def __init__(self, **kwargs):
        super(DragPiece, self).__init__(**kwargs)
        self.downX, self.downY = None, None

    def on_touch_up(self, touch):
        super(DragPiece, self).on_touch_up(touch)

        tx, ty = round(self.get_center_x()), round(self.get_center_y())
        centerX = (tx // tile_size) * tile_size + (tile_size // 2)
        centerY = (ty // tile_size) * tile_size + (tile_size // 2)
        if self.collide_point(*touch.pos):
            print(tx // tile_size)
        self.set_center_x(centerX)
        self.set_center_y(centerY)

        for idx, piece in enumerate(enemy.pieces):
            if self.collide_point(*touch.pos) and self.collide_point(piece.get_center_x(), piece.get_center_y()):
                print(f"{piece} was removed")
                print("---------")
                enemy.pieces.remove(piece)
                layout.remove_widget(piece)

        if self.collide_point(*touch.pos):
            if centerX != self.downX or centerY != self.downY:
                print("moved away from prev pos")
                # enemy = player1 if enemy == player2 else player2
            print(f"centerX={centerX} and downX={self.downX}")
            print(f"centerY={centerY} and downY={self.downY}")

    def on_touch_down(self, touch):
        super(DragPiece, self).on_touch_down(touch)

        self.downX, self.downY = round(self.get_center_x()), round(self.get_center_y())


class Piece(Image):
    def __init__(self, **kwargs):
        super(Piece, self).__init__(**kwargs)
        # self.color = None

    # def setColor(self, color):
    #    self.color = color

    # def position(self, x, y):
    #    self.x = x
    #    self.y = y


class King(DragPiece):
    def __str__(self):
        return "king"


class Queen(DragPiece):
    def __str__(self):
        return "queen"


class Bishop(DragPiece):
    def __str__(self):
        return "bishop"


class Knight(DragPiece):
    def __str__(self):
        return "knight"


class Rook(DragPiece):
    def __str__(self):
        return "rook"


class Pawn(DragPiece):
    def __str__(self):
        return "pawn"
