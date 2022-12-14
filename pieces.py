import itertools

from dragPiece import DragPiece


class King(DragPiece):
    def __str__(self):
        return "king"

    def generate_moves(self):
        self.availableMoves = []
        for i, j in itertools.product(range(-1, 2), range(-1, 2)):
            targetX, targetY = self.coordinates[0] + i, self.coordinates[1] + j
            if self.is_inside(targetX, targetY) and self.board[targetX][targetY] not in self.player.pieces:
                self.availableMoves.append((targetX, targetY))


class Queen(DragPiece):
    def __str__(self):
        return "queen"

    def generate_moves(self):
        self.availableMoves = []

        self.gen_sliding_move(1, 1)
        self.gen_sliding_move(1, -1)

        self.gen_sliding_move(-1, 1)
        self.gen_sliding_move(-1, -1)

        self.gen_sliding_move(1, 0)
        self.gen_sliding_move(0, 1)

        self.gen_sliding_move(-1, 0)
        self.gen_sliding_move(0, -1)


class Knight(DragPiece):
    def __str__(self):
        return "knight"

    def generate_moves(self):
        tuples = [(-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (1, -2), (-1, 2), (1, 2)]

        self.availableMoves = []
        for x, y in tuples:
            targetX, targetY = self.coordinates[0] + x, self.coordinates[1] + y
            if self.is_inside(targetX, targetY) and self.board[targetX][targetY] not in self.player.pieces:
                self.availableMoves.append((targetX, targetY))


class Bishop(DragPiece):  # futó
    def __str__(self):
        return "bishop"

    def generate_moves(self):
        self.availableMoves = []

        self.gen_sliding_move(1, 1)
        self.gen_sliding_move(1, -1)

        self.gen_sliding_move(-1, 1)
        self.gen_sliding_move(-1, -1)


class Rook(DragPiece):  # bástya
    def __str__(self):
        return "rook"

    def generate_moves(self):
        self.availableMoves = []

        self.gen_sliding_move(1, 0)
        self.gen_sliding_move(0, 1)

        self.gen_sliding_move(-1, 0)
        self.gen_sliding_move(0, -1)


class Pawn(DragPiece):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.piece_value = 10

    def __str__(self):
        return "pawn"

    def generate_moves(self):
        self.availableMoves = []
        startX = self.coordinates[0]
        startY = self.coordinates[1]

        toMove = 2 if self.alreadyMoved else 3

        if self.get_piece_color() == 'w':
            for i in range(1, toMove):
                if self.is_inside(startX + i, startY):
                    if self.board[startX + i][startY] != '-':
                        break
                    self.availableMoves.append((startX + i, startY))
            self.genCrossMove(startX + 1, startY + 1)
            self.genCrossMove(startX + 1, startY - 1)
        else:
            for i in range(1, toMove):
                if self.is_inside(startX - i, startY):
                    if self.board[startX - i][startY] != '-':
                        break
                    self.availableMoves.append((startX - i, startY))
            self.genCrossMove(startX - 1, startY + 1)
            self.genCrossMove(startX - 1, startY - 1)

    def genCrossMove(self, targetX, targetY):
        if self.is_inside(targetX, targetY) and self.board[targetX][targetY] in self.enemy.pieces:
            self.availableMoves.append((targetX, targetY))
