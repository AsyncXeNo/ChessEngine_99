from my_logging import get_logger
from game.piece import Piece


logger = get_logger(__name__)


class Knight(Piece):
    def __init__(self, color, square):
        super().__init__(color, square)

        self.symbol = 'n'
        self.offsets = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]
        self.range = 1
