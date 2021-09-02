import copy

from my_logging import get_logger


logger = get_logger(__name__)


class Piece(object):
    def __init__(self, color, square):
        self.symbol = None
        self.range = None
        self.offsets = None

        self.color = color
        self.square = square

    def get_moves(self):
        squares = []

        current = list(self.square.pos)

        for offset in self.offsets:
            new = current.copy()
            for _ in range(self.range):
                new[0] += offset[0]
                new[1] += offset[1]
                if new[0] not in range(1, 9) or new[1] not in range(1, 9): break
                sq = self.square.board.get_square_by_pos(new[0], new[1])
                if not sq.piece: squares.append(sq)
                else:
                    if sq.piece.color != self.color:
                        squares.append(sq)
                        break
                    else: break

        return squares

    def get_valid_squares(self):
        candidates = self.get_moves()
        final = []

        for square in candidates:
            result = self.run_test(square)
            if result == "PASSED": final.append(square)

        return final

    def get_valid_moves(self):
        candidates = self.get_moves()
        final = []

        for square in candidates:
            result = self.run_test(square)

            def move():
                self.move(square)

            if result == "PASSED": final.append(move)

        return final

    def run_test(self, square):
        test_board = copy.deepcopy(self.square.board)
        test_board.get_square_by_pos(square.file, square.rank).set_piece(test_board.get_square_by_pos(self.square.file, self.square.rank).piece)
        king = list(filter(lambda piece: piece.symbol == 'k' and piece.color == self.color, test_board.get_pieces()))[0]
        if king.in_check(king.square): return "FAILED"
        else: return "PASSED"

    def move(self, square):
        square.set_piece(self)

    def __str__(self):
        return self.symbol.upper() if self.color else self.symbol

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
