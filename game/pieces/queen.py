from my_logging import get_logger
from game.piece import Piece


logger = get_logger(__name__)


class Queen(Piece):
    def __init__(self, color, square):
        super().__init__(color, square)

        self.symbol = 'q'
        self.offsets = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)]
        self.range = 7
