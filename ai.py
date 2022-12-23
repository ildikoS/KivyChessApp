import pieces


def get_piece_value(pieceType):
    if pieceType == pieces.Pawn: return 10
    if pieceType == pieces.Knight: return 30
    if pieceType == pieces.Bishop: return 30
    if pieceType == pieces.Rook: return 50
    if pieceType == pieces.Queen: return 100
    if pieceType == pieces.King: return 1000


class AI:
    inf = 99999

    def __init__(self, board):
        self.board = board

    def minimax(self, player, depth, maxPlayer, alpha, beta):
        """

        :param beta:
        :param alpha:
        :param player:
        :param depth:
        :param maxPlayer:
        :return:
        """
        # TODO: refactor cause of nontype
        # orderedList = self.move_ordering(player)
        bestPieceWithMove = None, None

        if depth == 0:
            return self.evaluate(), bestPieceWithMove

        if maxPlayer:
            maxEvaluation = -self.inf
            # for currPiece in player.pieces:
            #    self.legal_moves(currPiece, currPiece.enemy)
            for currPiece, move in self.move_ordering(player):
                #    for move in currPiece.availableMoves:
                currPiece.make_move(move)
                currEvaluation = self.minimax(currPiece.enemy, depth - 1, False, alpha, beta)
                currValue = currEvaluation[0]
                if currValue > maxEvaluation:
                    maxEvaluation = max(maxEvaluation, currValue)
                    bestPieceWithMove = currPiece, move
                    # if depth == 1:
                    #    print("DEPTH 1")
                    #    print(currPiece, move, currValue)
                    #    print(bestPieceWithMove)
                currPiece.engine.unmake_move()
                alpha = max(alpha, currValue)
                # print(f"ALPHA: {alpha}")
                # print(f"BETA: {beta}")
                if beta <= alpha:
                    break
            # if beta <= alpha:
            #    break
            # print("MAXIMUM")
            # print(bestPieceWithMove, maxEvaluation)
            return maxEvaluation, bestPieceWithMove
        else:
            minEvaluation = self.inf
            # for currPiece in player.pieces:
            #    self.legal_moves(currPiece, currPiece.enemy)
            for currPiece, move in self.move_ordering(player):
                #    for move in currPiece.availableMoves:
                currPiece.make_move(move)
                currEvaluation = self.minimax(currPiece.enemy, depth - 1, True, alpha, beta)
                currValue = currEvaluation[0]
                print("LÉPETT")
                print(currPiece, move, currValue)
                # print(self.board)
                if currValue < minEvaluation:
                    minEvaluation = min(minEvaluation, currValue)
                    bestPieceWithMove = currPiece, move
                    if depth == 3:
                        # print(self.board[4][1])
                        print("--------------DEPTH 3---------------")
                        print(currPiece, move, currValue)
                        print(bestPieceWithMove)
                    # print(bestPieceWithMove)

                currPiece.engine.unmake_move()
                # print(beta)
                # print(alpha)
                beta = min(beta, currValue)
                if beta <= alpha:
                    break
            # if beta <= alpha:
            #    break
            # print("------")
            # print("MINIMUM")
            # print(self.board)
            # print(bestPieceWithMove, minEvaluation)
            return minEvaluation, bestPieceWithMove

    def move_ordering(self, player):
        moveScores = []
        constVal = 13
        piecesWithMoves = player.get_pieces_with_moves_list(self.board)
        #
        for piece, move in piecesWithMoves:
            score = 0
            capturePiece = self.board[move[0]][move[1]]
            if capturePiece != "-":
                score = constVal * get_piece_value(type(capturePiece)) - get_piece_value(type(piece))
            # print(piece, move, score)
            moveScores.append(score)
        #
        # Sorting
        piecesWithMoves, moveScores = zip(*sorted(zip(piecesWithMoves, moveScores), key=lambda x: x[1], reverse=True))
        #
        return piecesWithMoves

    #
    # print(sorted(zip(piecesWithMoves, moveScores), key=lambda x: x[1], reverse=True))

    def evaluate(self):
        whiteScore = self.count_pieces("w")
        blackScore = self.count_pieces("b")

        return whiteScore - blackScore

    def count_pieces(self, color):
        piecesTypes = [pieces.Pawn, pieces.Knight, pieces.Bishop, pieces.Rook, pieces.Queen, pieces.King]
        return sum(self.get_count(pieceType, color) * get_piece_value(pieceType) for pieceType in piecesTypes)

    def get_count(self, key, color):
        return sum(len([e for e in rows if type(e) == key and e.get_piece_color() == color]) for rows in self.board)
