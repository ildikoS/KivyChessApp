import random

import pieces


class AI:
    inf = 99999

    def __init__(self, board):
        self.depth = 3
        self.board = board

    def minimax(self, player, depth, maxPlayer, alpha, beta):
        bestPieceWithMove = None, None

        if depth == 0:
            return self.evaluate(), bestPieceWithMove

        if maxPlayer:
            maxEvaluation = -self.inf
            for currPiece, move in self.move_ordering(player):
                currPiece.make_move(move)
                currEvaluation = self.minimax(currPiece.enemy, depth - 1, False, alpha, beta)
                currValue = currEvaluation[0]
                if currValue > maxEvaluation:
                    maxEvaluation = max(maxEvaluation, currValue)
                    bestPieceWithMove = currPiece, move
                currPiece.engine.unmake_move()

                alpha = max(alpha, currValue)
                if beta <= alpha:
                    break
            return maxEvaluation, bestPieceWithMove
        else:
            minEvaluation = self.inf
            for currPiece, move in self.move_ordering(player):
                currPiece.make_move(move)
                currEvaluation = self.minimax(currPiece.enemy, depth - 1, True, alpha, beta)
                currValue = currEvaluation[0]
                if currValue < minEvaluation:
                    minEvaluation = min(minEvaluation, currValue)
                    bestPieceWithMove = currPiece, move
                currPiece.engine.unmake_move()

                beta = min(beta, currValue)
                if beta <= alpha:
                    break
            return minEvaluation, bestPieceWithMove

    def move_ordering(self, player):
        """
        Set pieces in order
        :param player:
        :return: ordered list of pieces with moves
        """
        moveScores = []
        constVal = 13
        piecesWithMoves = player.get_pieces_with_moves_list(self.board)

        for piece, move in piecesWithMoves:
            score = 0
            toX, toY = move
            capturePiece = self.board[toX][toY]
            if capturePiece != "-":
                score = constVal * self.get_piece_value(type(capturePiece)) - self.get_piece_value(type(piece))

            if piece.engine.is_checkmate(piece.enemy):
                score += 2000

            moveScores.append(score)

        if piecesWithMoves:
            piecesWithMoves, moveScores = zip(*sorted(zip(piecesWithMoves, moveScores), key=lambda x: x[1], reverse=True))

        return piecesWithMoves

    def evaluate(self):
        whiteScore = self.count_pieces("w")
        blackScore = self.count_pieces("b")

        return whiteScore - blackScore

    def count_pieces(self, color):
        piecesTypes = [pieces.Pawn, pieces.Knight, pieces.Bishop, pieces.Rook, pieces.Queen, pieces.King]
        return sum(self.get_count(pieceType, color) * self.get_piece_value(pieceType) for pieceType in piecesTypes)

    def get_count(self, key, color):
        return sum(len([e for e in rows if type(e) == key and e.get_piece_color() == color]) for rows in self.board)

    def set_depth(self, depth):
        self.depth = depth

    @staticmethod
    def get_piece_value(pieceType):
        if pieceType == pieces.Pawn: return 10
        if pieceType == pieces.Knight: return 30
        if pieceType == pieces.Bishop: return 30
        if pieceType == pieces.Rook: return 50
        if pieceType == pieces.Queen: return 100
        if pieceType == pieces.King: return 1000
