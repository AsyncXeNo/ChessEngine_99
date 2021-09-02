from game.pieces import rook, bishop, knight, queen, king, pawn


BASE_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

NUM_TO_FILE = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h'}
FILE_TO_NUM = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}

NUM_TO_COLOR = {1: 'w', 0: 'b'}
COLOR_TO_NUM = {'w': 1, 'b': 0}

SYMBOL_TO_PIECE = {
    'p': pawn.Pawn,
    'r': rook.Rook,
    'n': knight.Knight,
    'b': bishop.Bishop,
    'q': queen.Queen,
    'k': king.King
}