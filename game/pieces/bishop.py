from my_logging import get_logger
from game.piece import Piece


logger = get_logger(__name__)


class Bishop(Piece):
    def __init__(self, color, square):
        super().__init__(color, square)

        self.symbol = 'b'
        self.offsets = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
        self.range = 7
