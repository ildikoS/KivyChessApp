from memento import CareTaker, Memento

tile_size = 80


class Piece:
    def __init__(self):
        self.alreadyMoved = False
        self.coordinates = None
        self.engine = None
        self.board = None
        self.player = None
        self.enemy = None
        self.pieceColor = None
        self.availableMoves = []

    def isInside(self, x, y):
        return 0 <= x < 8 and 0 <= y < 8

    def genSlidingMove(self, dirX, dirY):
        for i in range(1, 8):
            X = self.coordinates[0] + (i * dirX)
            Y = self.coordinates[1] + (i * dirY)

            if self.isInside(X, Y):
                if self.board[X][Y] in self.player.pieces:
                    break

                self.availableMoves.append((X, Y))

                if self.board[X][Y] in self.enemy.pieces:
                    break

    def computer_move(self):
        """

        :return: With a random move of a random enemy piece
        """
        #print(self.board)
        self.engine.minimax(self.enemy, 2, False, -9999, 9999)
        #print(self.board)

        compPiece = self.engine.bestPieceWithMove[0]
        compMove = self.engine.bestPieceWithMove[1]

        #print(compPiece.availableMoves)
        compPiece.engine.make_move(compMove, compPiece)

        removingPiece = compPiece.engine.removingPiece
        if removingPiece is not None:
            compPiece.pieceLayout.remove_widget(removingPiece)

        return compPiece, compMove

    # getters, setters
    def set_piece_color(self, color):
        self.pieceColor = color

    def set_engine(self, engine, layout):
        self.engine = engine
        self.board = self.engine.board

        self.player = self.engine.player1 if self.get_piece_color() == 'b' else self.engine.player2
        self.enemy = self.engine.player2 if self.player == self.engine.player1 else self.engine.player1

        #self.careTaker = CareTaker(self.engine)

        self.pieceLayout = layout

    def get_piece_color(self):
        return self.pieceColor

    def set_coords(self, x, y):
        self.coordinates = (x, y)

    def is_already_moved(self, moved):
        self.alreadyMoved = moved

    @property
    def memento(self):
        "A `getter` for the characters attributes as a Memento"
        return Memento(
            self,
            self.coordinates,
            self.engine.board
        )

    @memento.setter
    def memento(self, memento):
        self = memento.piece,
        self.coordinates = memento.move
        self.engine.board = memento.board



