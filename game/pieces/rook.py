from my_logging import get_logger
from game.piece import Piece


logger = get_logger(__name__)


class Rook(Piece):
    def __init__(self, color, square):
        super().__init__(color, square)

        self.symbol = 'r'
        self.offsets = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        self.range = 7

    def move(self, square):
        if self.square.file == 1 and self.square.rank == 8:
            list(filter(lambda piece: piece.symbol == 'k' and piece.color == 0, self.square.board.get_pieces()))[0].castle_q = False
        if self.square.file == 8 and self.square.rank == 8:
            list(filter(lambda piece: piece.symbol == 'k' and piece.color == 0, self.square.board.get_pieces()))[0].castle_k = False
        if self.square.file == 1 and self.square.rank == 1:
            list(filter(lambda piece: piece.symbol == 'k' and piece.color == 1, self.square.board.get_pieces()))[0].castle_q = False
        if self.square.file == 8 and self.square.rank == 1:
            list(filter(lambda piece: piece.symbol == 'k' and piece.color == 1, self.square.board.get_pieces()))[0].castle_k = False
        super().move(square)
