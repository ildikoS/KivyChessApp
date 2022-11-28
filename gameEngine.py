from kivy.uix.floatlayout import FloatLayout

import piece


class Player:
    def __init__(self, pieces):
        self.pieces = pieces


def get_piece(char):
    if char == 'k': return piece.King()
    if char == 'q': return piece.Queen()
    if char == 'b': return piece.Bishop()
    if char == 'n': return piece.Knight()
    if char == 'r': return piece.Rook()
    if char == 'p': return piece.Pawn()


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


class GameEngine:
    initialFEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR/ w KQkq - 0 1'
    board = positions_from_FEN(initialFEN)
    blacks = []
    whites = []
    whiteTurn = True
    inf = 999999

    def __init__(self):
        self.kingSquare = None
        self.player1 = None
        self.player2 = None
        self.layout = FloatLayout()

    def createBoard(self):
        for i in range(8):
            for j in range(8):
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
        for enemyPiece in enemy.pieces:
            if enemyPiece.coordinates == playerPiece.coordinates:
                print("---------")
                print(f"{enemyPiece} was removed")
                print("---------")
                enemy.pieces.remove(enemyPiece)
                self.layout.remove_widget(enemyPiece)
                return True
        return False

    def is_checked(self, playerPiece, enemy):
        original_pos = playerPiece.coordinates
        playerPiece.generate_moves()

        for move in playerPiece.availableMoves:
            self.make_move(move, playerPiece)
            for enemyPiece in enemy.pieces:
                enemyPiece.generate_moves()
                if self.kingSquare in enemyPiece.availableMoves:
                    print(f"{enemyPiece} - {enemyPiece.availableMoves}")
                    playerPiece.availableMoves.remove(move)
                    continue
            self.make_move(original_pos, playerPiece)

    def make_move(self, move, argPiece):
        """
        Set the (x, y) square of piece
        :param move: Tuple with number x, y coordinates
        :param argPiece: Piece which wanted to be moved to the square
        """
        x, y = argPiece.coordinates
        self.board[x][y] = "-"
        x, y = move
        self.board[x][y] = argPiece
        argPiece.set_coords(x, y)
        self.get_king_square(argPiece.get_piece_color())

    def get_king_square(self, pieceColor):
        for i in range(8):
            for j in range(8):
                if type(self.board[i][j]) == piece.King and self.board[i][j].get_piece_color() == pieceColor:
                    self.kingSquare = (i, j)
                    #print(f"FOUND KING {self.kingSquare}")
                    break

    def minimax(self, depth, maxPlayer):
        if depth == 0:
            return self.evaluate()

        maxEvaluation = -self.inf
        if maxPlayer:
            for move in moves:
                self.make_move()
                currEvaluation = self.minimax(depth - 1)
                if currEvaluation > maxEvaluation:
                    maxEvaluation = max(currEvaluation, maxEvaluation)
                self.unmake_move()
            return maxEvaluation
        else:
            minEvaluation = self.inf
            for move in moves:
                self.make_move()
                currEvaluation = self.minimax(depth - 1)
                if currEvaluation < minEvaluation:
                    minEvaluation = max(currEvaluation, maxEvaluation)
                self.unmake_move()
            return minEvaluation

    def negamax(self, depth):
        if depth == 0:
            return self.evaluate()

        maxEvaluation = -self.inf
        for move in moves:
            self.make_move(move)
            currEvaluation = -self.negamax(depth - 1)
            if currEvaluation > maxEvaluation:
                maxEvaluation = max(currEvaluation, maxEvaluation)
            self.unmake_move()

        return maxEvaluation

    def evaluate(self):
        whiteScore = self.count_pieces("w")
        blackScore = self.count_pieces("b")

        print(whiteScore)
        print(blackScore)

        evaluation = whiteScore - blackScore
        # evaluation = materialWeight * (whiteScore - blackScore)

        whoToMove = 1 if self.whiteTurn else -1
        return evaluation * whoToMove

    def count_pieces(self, color):
        pawnValue = 10
        knightValue = 30
        bishopValue = 30
        rookValue = 50
        queenValue = 90
        kingValue = 900

        piece_dict = {
            piece.Pawn: pawnValue,
            piece.Knight: knightValue,
            piece.Bishop: bishopValue,
            piece.Rook: rookValue,
            piece.Queen: queenValue,
            piece.King: kingValue
        }

        valueCount = 0
        for pieceKey, pieceValue in piece_dict.items():
            valueCount += self.get_count(pieceKey, color) * pieceValue

        return valueCount

    def get_count(self, key, color):
        #print(sum([len([e for e in rows if type(e) == key and e.get_piece_color() == color]) for rows in self.board]))
        return sum([len([e for e in rows if type(e) == key and e.get_piece_color() == color]) for rows in self.board])
