import itertools

import pieces
from ai import AI
from player import Player


class GameEngine:
    def __init__(self, inputFEN):
        self.pieceStepsList = []
        self.board = self.positions_from_FEN(inputFEN)
        self.blacks = []
        self.whites = []
        self.removingPiece = None
        self.targetTile = None
        self.kingSquare = None
        self.player1 = None
        self.player2 = None
        self.isGameOver = False
        self.ai = AI(self.board)

    def create_board(self):
        for i, j in itertools.product(range(8), range(8)):
            currPiece = self.board[i][j]
            if currPiece != '-':
                self.board[i][j] = self.get_piece(currPiece.lower())
                self.board[i][j].set_piece_color('w' if currPiece.islower() else 'b')
                self.board[i][j].set_coords(i, j)

                self.blacks.append(self.board[i][j]) \
                    if self.board[i][j].get_piece_color() == 'b' else self.whites.append(self.board[i][j])
        self.player1 = Player(self.blacks, "b")
        self.player2 = Player(self.whites, "w")
        return self.board

    def set_players_score(self, bScore, wScore):
        self.player1.set_score(bScore)
        self.player2.set_score(wScore)

    #def checkCollision(self, enemy, playerPiece):
    #    """
    #    Check if 2 pieces are collided or not
    #    :param enemy: The other player
    #    :param playerPiece: Current player's piece
    #    :return: with enemyPiece if found collided piece, otherwise False
    #    """
    #    for enemyPiece in enemy.pieces:
    #        if enemyPiece.coordinates == playerPiece.coordinates:
    #            print("---------")
    #            print(f"{enemyPiece} was removed")
    #            print("---------")
    #            return enemyPiece
    #    return False

    def legal_moves(self, playerPiece, enemy):
        playerPiece.generate_moves()
        invalidMoves = set()

        self.can_castling(playerPiece)
        for move in playerPiece.availableMoves:
            playerPiece.make_move(move)
            for enemyPiece in enemy.pieces:
                enemyPiece.generate_moves()
                if self.kingSquare in enemyPiece.availableMoves:
                    invalidMoves.add(move)
            self.unmake_move()

        for invMove in invalidMoves:
            playerPiece.availableMoves.remove(invMove)

    def is_checkmate(self, player):
        for myPiece in player.pieces:
            self.legal_moves(myPiece, myPiece.enemy)
            if myPiece.availableMoves:
                return False
        return True

    def is_pawn_changed(self, piece):
        if type(piece) == pieces.Pawn:
            if piece.get_piece_color() == 'w' and piece.coordinates[0] == 7:
                return self.change_pawn(piece)
            elif piece.get_piece_color() == 'b' and piece.coordinates[0] == 0:
                return self.change_pawn(piece)
        return None

    def change_pawn(self, pawn):
        prevPiece = pawn
        pawnX, pawnY = pawn.coordinates
        layout = pawn.pieceLayout
        piece = pieces.Queen()
        piece.set_piece_color(pawn.get_piece_color())
        piece.source = f'imgs/pieces/{piece.get_piece_color()}_queen_png_shadow_128px.png'
        piece.set_engine(self, layout)
        piece.set_coords(pawnX, pawnY)
        self.board[pawnX][pawnY] = piece
        piece.player.pieces.append(piece)
        return prevPiece, piece

    def can_castling(self, playerPiece):
        self.set_king_square(playerPiece.get_piece_color())
        kingX, kingY = self.kingSquare
        king = self.board[kingX][kingY]
        if not king.alreadyMoved:
            bottomRook = self.board[kingX][0]
            overRook = self.board[kingX][7]

            if type(bottomRook) == pieces.Rook and not bottomRook.alreadyMoved and self.board[kingX][kingY - 1] == "-" \
                    and self.board[kingX][kingY - 2] == "-":
                king.availableMoves.append((kingX, kingY - 2))

            if type(overRook) == pieces.Rook and not overRook.alreadyMoved and self.board[kingX][kingY + 1] == "-" \
                    and self.board[kingX][kingY + 2] == "-" and self.board[kingX][kingY + 3] == "-":
                king.availableMoves.append((kingX, kingY + 2))

    def do_castling(self):
        kingX, kingY = self.kingSquare

        if type(self.board[kingX][0]) == pieces.Rook:
            if kingY == 1:
                self.set_rook_pos(kingX, 0, (kingX, kingY + 1))
            elif kingY == 5:
                self.set_rook_pos(kingX, 7, (kingX, kingY - 1))

    def set_rook_pos(self, kingX, rookY, newPos):
        rook = self.board[kingX][rookY]
        self.board[kingX][rookY] = "-"
        rookX, rookY = newPos
        self.board[rookX][rookY] = rook
        self.board[rookX][rookY].set_coords(rookX, rookY)

    def unmake_move(self):
        lastStep = self.pieceStepsList[-1]
        lastStep.piece.alreadyMoved = lastStep.alreadyMoved

        for i, j in itertools.product(range(8), range(8)):
            self.board[i][j] = lastStep.board[i][j]
            if self.board[i][j] != "-":
                lastStep.board[i][j].set_coords(i, j)

        if lastStep.targetTile != "-":
            lastStep.targetTile.player.pieces.append(lastStep.targetTile)

        self.pieceStepsList.pop(-1)

    def fill_piece_list(self):
        self.blacks.clear()
        self.whites.clear()
        for i, j in itertools.product(range(8), range(8)):
            if self.board[i][j] != "-":
                self.blacks.append(self.board[i][j]) \
                    if self.board[i][j].get_piece_color() == 'b' else self.whites.append(self.board[i][j])

    def set_king_square(self, pieceColor):
        for i in range(8):
            for j in range(8):
                if type(self.board[i][j]) == pieces.King and self.board[i][j].get_piece_color() == pieceColor:
                    self.kingSquare = (i, j)
                    break

    @staticmethod
    def get_piece(char):
        if char == 'k': return pieces.King()
        if char == 'q': return pieces.Queen()
        if char == 'b': return pieces.Bishop()
        if char == 'n': return pieces.Knight()
        if char == 'r': return pieces.Rook()
        if char == 'p': return pieces.Pawn()

    @staticmethod
    def positions_from_FEN(fenStr):
        board = []
        innerBoard = []
        for char in fenStr.split()[0]:
            if char == '/':
                board.append(innerBoard)
                innerBoard = []
            elif char.isdigit():
                innerBoard.extend('-' * int(char))
            else:
                innerBoard.append(char)
        return board

