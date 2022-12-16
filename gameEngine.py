import itertools
import pieces


class Player:
    def __init__(self, playerPieces):
        self.pieces = playerPieces


def get_piece(char):
    if char == 'k': return pieces.King()
    if char == 'q': return pieces.Queen()
    if char == 'b': return pieces.Bishop()
    if char == 'n': return pieces.Knight()
    if char == 'r': return pieces.Rook()
    if char == 'p': return pieces.Pawn()


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


class PieceStep:
    def __init__(self, board, piece, targetMove):
        self.board = [x[:] for x in board]
        self.piece = piece
        self.alreadyMoved = self.piece.alreadyMoved
        self.coordinates = piece.coordinates
        self.move = targetMove
        self.targetTile = self.board[targetMove[0]][targetMove[1]]
        self.piecesList = self.piece.player.pieces


class GameEngine:
    inf = 999999

    def __init__(self, inputFEN):
        self.pieceStepsList = []
        self.board = positions_from_FEN(inputFEN)
        self.blacks = []
        self.whites = []
        self.whiteTurn = True
        self.bestPieceWithMove = None
        self.removingPiece = None
        self.originalPieceCoords = None
        self.targetTileCoords = None
        self.targetTile = None
        self.originalPiece = None
        self.kingSquare = None
        self.player1 = None
        self.player2 = None
        self.isGameOver = False

    def createBoard(self):
        for i, j in itertools.product(range(8), range(8)):
            currPiece = self.board[i][j]
            if currPiece != '-':
                self.board[i][j] = get_piece(currPiece.lower())
                self.board[i][j].set_piece_color('w' if currPiece.islower() else 'b')
                self.board[i][j].set_coords(i, j)

                self.blacks.append(self.board[i][j]) \
                    if self.board[i][j].get_piece_color() == 'b' else self.whites.append(self.board[i][j])
        self.player1 = Player(self.blacks)
        self.player2 = Player(self.whites)

        return self.board

    def checkCollision(self, enemy, playerPiece):
        """
        Check if 2 pieces are collided or not
        :param enemy: The other player
        :param playerPiece: Current player's piece
        :return: with enemyPiece if found collided piece, otherwise False
        """
        for enemyPiece in enemy.pieces:
            if enemyPiece.coordinates == playerPiece.coordinates:
                print("---------")
                print(f"{enemyPiece} was removed")
                print("---------")
                return enemyPiece
        return False

    def legal_moves(self, playerPiece, enemy):
        playerPiece.generate_moves()
        invalid_moves = set()

        self.can_castling(playerPiece)
        for move in playerPiece.availableMoves:
            self.make_move(move, playerPiece)
            for enemyPiece in enemy.pieces:
                enemyPiece.generate_moves()
                if self.kingSquare in enemyPiece.availableMoves:
                    invalid_moves.add(move)
            self.unmake_move()

        for inv_move in invalid_moves:
            playerPiece.availableMoves.remove(inv_move)

    def is_checkmate(self, player):
        for myPiece in player.pieces:
            self.legal_moves(myPiece, myPiece.enemy)
            if myPiece.availableMoves:
                return False
        return True

    def is_pawn_changed(self, piece):
        if type(piece) == pieces.Pawn:
            if piece.get_piece_color() == 'w' and piece.coordinates[0] == 7:
                return self.change_pawn(piece, 'w')
            elif piece.get_piece_color() == 'b' and piece.coordinates[0] == 0:
                return self.change_pawn(piece, 'b')
        return None

    def change_pawn(self, pawn, color):
        prevPiece = pawn
        coordinates = pawn.coordinates
        layout = pawn.pieceLayout
        piece = pieces.Queen()
        piece.source = f'imgs/pieces/{color}_queen_png_shadow_128px.png'
        piece.set_piece_color(color)
        piece.set_engine(self, layout)
        piece.set_coords(coordinates[0], coordinates[1])
        self.board[coordinates[0]][coordinates[1]] = piece
        piece.player.pieces.append(piece)
        return prevPiece, piece

    def can_castling(self, playerPiece):
        self.set_king_square(playerPiece.get_piece_color())
        kingX, kingY = self.kingSquare
        king = self.board[kingX][kingY]
        if not king.alreadyMoved:
            bottomRook = self.board[kingX][0]

            if type(bottomRook) == pieces.Rook and not bottomRook.alreadyMoved and self.board[kingX][kingY - 1] == "-" \
                    and self.board[kingX][kingY - 2] == "-":
                king.availableMoves.append((kingX, kingY - 2))
            overRook = self.board[kingX][7]
            if type(overRook) == pieces.Rook and not overRook.alreadyMoved and self.board[kingX][kingY + 1] == "-" \
                    and self.board[kingX][kingY + 2] == "-" and self.board[kingX][kingY + 3] == "-":
                king.availableMoves.append((kingX, kingY + 2))

    def do_castling(self):
        print("castling")
        kingX, kingY = self.kingSquare
        rook = None

        if type(self.board[kingX][0]) == pieces.Rook:
            if kingY == 1:
                print(self.board[kingX][0])
                self.set_rook_pos(kingX, 0, (kingX, kingY + 1))
            elif kingY == 5:
                print(self.board[kingX][0])
                self.set_rook_pos(kingX, 7, (kingX, kingY - 1))

        print(f"BOTTOMROOK: {rook}")

        # self.board[kingX][kingY+1] = bottomRook
        # print(f"king feletti hely: {self.board[kingX][kingY + 1]}")
        # self.board[kingX][kingY+1].set_coords(kingX, kingY + 1)

    def set_rook_pos(self, kingX, rookY, newPos):
        rook = self.board[kingX][rookY]
        self.board[kingX][rookY] = "-"
        rookX, rookY = newPos
        self.board[rookX][rookY] = rook
        self.board[rookX][rookY].set_coords(rookX, rookY)
        self.board[rookX][rookY].set_center(self.board[rookX][rookY], rookX, rookY)

    def make_move(self, move, argPiece):
        """
        Set the (x, y) square of piece
        :param move: Tuple with number x, y coordinates
        :param argPiece: Piece which wanted to be moved to the square
        """
        self.pieceStepsList.append(PieceStep(self.board, argPiece, move))
        self.removingPiece = None
        x, y = argPiece.coordinates
        self.board[x][y] = "-"

        x, y = self.pieceStepsList[-1].move
        self.targetTile = self.pieceStepsList[-1].targetTile
        self.board[x][y] = self.pieceStepsList[-1].piece
        argPiece.set_coords(x, y)
        if self.targetTile != "-":
            self.removingPiece = self.targetTile
            argPiece.enemy.pieces.remove(self.targetTile)

        if argPiece.coordinates == self.kingSquare and y in [1, 5]:
            self.do_castling()

        self.set_king_square(argPiece.get_piece_color())

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
                    # print(f"FOUND KING {self.kingSquare}")
                    break

    def minimax(self, player, depth, maxPlayer, alpha, beta):
        """

        :param beta:
        :param alpha:
        :param player:
        :param depth:
        :param maxPlayer:
        :return:
        """
        #TODO: refactor cause of nontype
        bestPieceWithMove = None, None

        if depth == 0:
            return self.evaluate(not maxPlayer), bestPieceWithMove

        #self.whiteTurn = not self.whiteTurn

        if maxPlayer:
            maxEvaluation = -self.inf
            for currPiece in player.pieces:
                self.legal_moves(currPiece, currPiece.enemy)
                for move in currPiece.availableMoves:
                    self.make_move(move, currPiece)
                   # print(f"{currPiece.get_piece_color()} lepett")
                    currEvaluation = self.minimax(currPiece.enemy, depth - 1, False, alpha, beta)
                    currValue = currEvaluation[0]
                    if currValue > maxEvaluation:
                        maxEvaluation = max(currValue, maxEvaluation)
                        bestPieceWithMove = currPiece, move
                    self.unmake_move()
                    alpha = max(alpha, currValue)
                    #if beta <= alpha:
                    #    break
            #print("MAXIMUM")
            #print(bestPieceWithMove, maxEvaluation)
            return maxEvaluation, bestPieceWithMove
        else:
            minEvaluation = self.inf
            for currPiece in player.pieces:
                self.legal_moves(currPiece, currPiece.enemy)
                for move in currPiece.availableMoves:
                    self.make_move(move, currPiece)
                   # print(f"{currPiece.get_piece_color()} lepett")
                    currEvaluation = self.minimax(currPiece.enemy, depth - 1, True, alpha, beta)
                    currValue = currEvaluation[0]
                    print(move, currPiece, currValue)
                    if currValue < minEvaluation:
                        minEvaluation = min(currValue, minEvaluation)
                        bestPieceWithMove = currPiece, move
                    self.unmake_move()
                    beta = min(beta, currValue)
                    #if beta <= alpha:
                    #    break
            #print("MINIMUM")
            #print(bestPieceWithMove, minEvaluation)
            return minEvaluation, bestPieceWithMove

    def move_ordering(self):
        pass

    def evaluate(self, maxPlayer):
        #TODO: refactoring, testing
        whiteScore = self.count_pieces("w")
        blackScore = self.count_pieces("b")

        #evaluation = whiteScore - blackScore
        #whoToMove = 1 if maxPlayer else -1
        #print(maxPlayer)

        return whiteScore - blackScore #* whoToMove

    def count_pieces(self, color):
        pawnValue = 10
        knightValue = 30
        bishopValue = 30
        rookValue = 50
        queenValue = 90
        kingValue = 900

        piece_dict = {
            pieces.Pawn: pawnValue,
            pieces.Knight: knightValue,
            pieces.Bishop: bishopValue,
            pieces.Rook: rookValue,
            pieces.Queen: queenValue,
            pieces.King: kingValue
        }

        # valueCount = 0
        # for pieceKey, pieceValue in piece_dict.items():
        #    valueCount += self.get_count(pieceKey, color) * pieceValue
        # return valueCount

        return sum(self.get_count(pieceKey, color) * pieceValue for pieceKey, pieceValue in piece_dict.items())

    def get_count(self, key, color):
        return sum(len([e for e in rows if type(e) == key and e.get_piece_color() == color]) for rows in self.board)
