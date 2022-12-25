import itertools


class Player:

    def __init__(self, playerPieces, color):
        self.pieces = playerPieces
        self.color = color
        self.numberOfWins = 0

    def get_pieces_with_moves_list(self, board):
        piecesWithMoves = []
        for i, j in itertools.product(range(8), range(8)):
            if board[i][j] != "-" and board[i][j].get_piece_color() == self.color:
                piece = board[i][j]
                board[i][j].engine.legal_moves(piece, piece.enemy)
                piecesWithMoves.extend((piece, move) for move in piece.availableMoves)
        return piecesWithMoves

    def set_score(self, score):
        self.numberOfWins = score
