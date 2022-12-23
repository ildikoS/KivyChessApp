import random

tile_size = 80

mainFEN = 'rnbkqbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBKQBNR/ w KQkq - 0 1'

practiseFENs = [
    #'8/RB6/3p4/3P1pBk/7P/Pq6/p1Rp3n/3K2n1/ w - - 0 1',
    '2R4n/2Kpk3/7B/3P1pN1/p7/pB6/P1P2Q2/7b/ w - - 0 1',
    #'2R5/6P1/1bP1npp1/2k2P2/1q6/2p5/2p2P2/N1K3B1/ w - - 0 1',
    #'r2k4/6P1/1bP1npp1/5P2/1q6/2p5/2p2P2/N1K3B1/ w - - 0 1'
]

def get_random_FEN():
    return random.choice(practiseFENs)
