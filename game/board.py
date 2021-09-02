from my_logging import get_logger
from game.constants import BASE_FEN
from game.square import Square
from game.chess_utils import setup


logger = get_logger(__name__)


class Board(object):
    def __init__(self, fen=BASE_FEN):
        self.fen = fen

        self.squares = [[Square(self, file, rank) for rank in range(1, 9)] for file in range(1, 9)]

        self.move = None
        self.en_passant_square = None
        self.half_moves = None
        self.full_moves = None

        setup(self, self.fen)

    def get_pieces(self):
        pieces = []
        for file in self.squares:
            for square in file:
                if square.piece: pieces.append(square.piece)
        return pieces

    def get_white_pieces(self):
        return list(filter(lambda piece: piece.color, self.get_pieces()))

    def get_black_pieces(self):
        return list(filter(lambda piece: not piece.color, self.get_pieces()))

    def get_square_by_pos(self, file, rank):
        return self.squares[file-1][rank-1]

    def test(self):
        for file in self.squares:
            for square in file:
                if square.piece: logger.info(f'{square} - {square.piece.get_valid_squares()}')

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        logger.debug(f'Set {key} to {value} in {self.__class__.__name__}.')
