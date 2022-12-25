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

    #def make_move(self, move, argPiece):
    #    """
    #    Set the (x, y) square of piece
    #    :param move: Tuple with number x, y coordinates
    #    :param argPiece: Piece which wanted to be moved to the square
    #    """
    #    self.pieceStepsList.append(LastPieceStep(self.board, argPiece, move))
    #    self.removingPiece = None
    #    x, y = argPiece.coordinates
    #    self.board[x][y] = "-"
#
    #    x, y = self.pieceStepsList[-1].move
    #    self.targetTile = self.pieceStepsList[-1].targetTile
    #    self.board[x][y] = self.pieceStepsList[-1].piece
    #    argPiece.set_coords(x, y)
    #    if self.targetTile != "-":
    #        self.removingPiece = self.targetTile
    #        argPiece.enemy.pieces.remove(self.targetTile)
#
    #    #print(argPiece.enemy.pieces)
#
    #    if argPiece.coordinates == self.kingSquare and y in [1, 5]:
    #        self.do_castling()
#
    #    self.set_king_square(argPiece.get_piece_color())

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

    #def get_pieces_with_moves_list(self, player):
    #    piecesWithMoves = []
    #    color = player.pieces[0].get_piece_color()
    #    for i, j in itertools.product(range(8), range(8)):
    #        if self.board[i][j] != "-" and self.board[i][j].get_piece_color() == color:
    #            piece = self.board[i][j]
    #            self.legal_moves(piece, piece.enemy)
    #            piecesWithMoves.extend((piece, move) for move in piece.availableMoves)
    #    return piecesWithMoves

   # def minimax(self, player, depth, maxPlayer, alpha, beta):
   #     """
#
   #     :param beta:
   #     :param alpha:
   #     :param player:
   #     :param depth:
   #     :param maxPlayer:
   #     :return:
   #     """
   #     # TODO: refactor cause of nontype
   #     #orderedList = self.move_ordering(player)
   #     bestPieceWithMove = None, None
#
   #     if depth == 0:
   #         return self.evaluate(), bestPieceWithMove
#
   #     if maxPlayer:
   #         maxEvaluation = -self.inf
   #         #for currPiece in player.pieces:
   #         #    self.legal_moves(currPiece, currPiece.enemy)
   #         for currPiece, move in self.move_ordering(player):
   #         #    for move in currPiece.availableMoves:
   #                 currPiece.make_move(move)
   #                 currEvaluation = self.minimax(currPiece.enemy, depth - 1, False, alpha, beta)
   #                 currValue = currEvaluation[0]
   #                 if currValue > maxEvaluation:
   #                     maxEvaluation = max(maxEvaluation, currValue)
   #                     bestPieceWithMove = currPiece, move
   #                     #if depth == 1:
   #                     #    print("DEPTH 1")
   #                     #    print(currPiece, move, currValue)
   #                     #    print(bestPieceWithMove)
   #                 currPiece.unmake_move()
   #                 alpha = max(alpha, currValue)
   #                 #print(f"ALPHA: {alpha}")
   #                 #print(f"BETA: {beta}")
   #                 if beta <= alpha:
   #                     break
   #         #if beta <= alpha:
   #         #    break
   #         #print("MAXIMUM")
   #         #print(bestPieceWithMove, maxEvaluation)
   #         return maxEvaluation, bestPieceWithMove
   #     else:
   #         minEvaluation = self.inf
   #         #for currPiece in player.pieces:
   #         #    self.legal_moves(currPiece, currPiece.enemy)
   #         for currPiece, move in self.move_ordering(player):
   #         #    for move in currPiece.availableMoves:
   #                 currPiece.make_move(move)
   #                 currEvaluation = self.minimax(currPiece.enemy, depth - 1, True, alpha, beta)
   #                 currValue = currEvaluation[0]
   #                 print("LÉPETT")
   #                 print(currPiece, move, currValue)
   #                 #print(self.board)
   #                 if currValue < minEvaluation:
   #                     minEvaluation = min(minEvaluation, currValue)
   #                     bestPieceWithMove = currPiece, move
   #                     if depth == 3:
   #                         # print(self.board[4][1])
   #                         print("--------------DEPTH 3---------------")
   #                         print(currPiece, move, currValue)
   #                         print(bestPieceWithMove)
   #                     #print(bestPieceWithMove)
#
   #                 currPiece.unmake_move()
   #                     #print(beta)
   #                     #print(alpha)
   #                 beta = min(beta, currValue)
   #                 if beta <= alpha:
   #                     break
   #         #if beta <= alpha:
   #         #    break
   #         #print("------")
   #         #print("MINIMUM")
   #         #print(self.board)
   #         #print(bestPieceWithMove, minEvaluation)
   #         return minEvaluation, bestPieceWithMove
#
   # def move_ordering(self, player):
   #     moveScores = []
   #     constVal = 13
   #     piecesWithMoves = self.get_pieces_with_moves_list(player)
##
   #     for piece, move in piecesWithMoves:
   #         score = 0
   #         capturePiece = self.board[move[0]][move[1]]
   #         if capturePiece != "-":
   #             score = constVal * get_piece_value(type(capturePiece)) - get_piece_value(type(piece))
   #         #print(piece, move, score)
   #         moveScores.append(score)
##
   #     #Sorting
   #     piecesWithMoves, moveScores = zip(*sorted(zip(piecesWithMoves, moveScores), key=lambda x: x[1], reverse=True))
##
   #     return piecesWithMoves
##
   #     #print(sorted(zip(piecesWithMoves, moveScores), key=lambda x: x[1], reverse=True))
#
   # def evaluate(self):
   #     # TODO: refactoring, testing
   #     whiteScore = self.count_pieces("w")
   #     blackScore = self.count_pieces("b")
#
   #     #print(whiteScore)
   #     #print(blackScore)
   #     #print(self.board)
#
   #     return whiteScore - blackScore
#
   # def count_pieces(self, color):
   #     piecesTypes = [pieces.Pawn, pieces.Knight, pieces.Bishop, pieces.Rook, pieces.Queen, pieces.King]
   #     return sum(self.get_count(pieceType, color) * get_piece_value(pieceType) for pieceType in piecesTypes)
#
   # def get_count(self, key, color):
   #     return sum(len([e for e in rows if type(e) == key and e.get_piece_color() == color]) for rows in self.board)
