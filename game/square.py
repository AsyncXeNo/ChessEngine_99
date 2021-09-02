from my_logging import get_logger
from game.constants import NUM_TO_FILE


logger = get_logger(__name__)


class Square(object):
    def __init__(self, board, file, rank, piece=None):
        self.pos = (file, rank)
        self.board = board
        self.file = file
        self.rank = rank
        self.piece = piece

    def get_name(self):
        return f'{NUM_TO_FILE[self.file]}{self.rank} - {"null" if not self.piece else self.piece}'

    def set_piece(self, piece):
        if self.piece:
            self.piece.square = None
        piece.square.piece = None
        piece.square = self
        self.piece = piece

    def __eq__(self, other):
        return True if self.file == other.file and self.rank == other.rank else False

    def __str__(self):
        return f'{NUM_TO_FILE[self.file]}{self.rank} - {"null" if not self.piece else self.piece}'

    def __repr__(self):
        return f'{NUM_TO_FILE[self.file]}{self.rank} - {"null" if not self.piece else self.piece}'

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        logger.debug(f'Set {key} to {value} in {self.__class__.__name__} on pos {NUM_TO_FILE[self.pos[0]]}{self.pos[1]}.')
