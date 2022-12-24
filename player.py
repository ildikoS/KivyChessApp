import itertools


class Player:
    def __init__(self, playerPieces):
        self.pieces = playerPieces

    def get_pieces_with_moves_list(self, board):
        piecesWithMoves = []
        color = self.pieces[0].get_piece_color()
        for i, j in itertools.product(range(8), range(8)):
            if board[i][j] != "-" and board[i][j].get_piece_color() == color:
                piece = board[i][j]
                board[i][j].engine.legal_moves(piece, piece.enemy)
                piecesWithMoves.extend((piece, move) for move in piece.availableMoves)
        return piecesWithMoves
