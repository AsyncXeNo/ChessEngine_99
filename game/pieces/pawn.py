from my_logging import get_logger
from game.piece import Piece


logger = get_logger(__name__)


class Pawn(Piece):
    def __init__(self, color, square):
        super().__init__(color, square)

        self.symbol = 'p'
        self.moved = False if (self.square.rank == 7 and not self.color) or (self.square.rank == 2 and self.color) else True
        self.moving_offsets = [(0, 1)] if self.color else [(0, -1)]
        self.capture_offsets = [(-1, 1), (1, 1)] if self.color else [(-1, -1), (1, -1)]
        self.capture_range = 1

    def can_promote(self):
        for square in self.get_valid_squares():
            if square.rank in [1, 8]: return True
        return False

    def get_move_range(self):
        return 1 if self.moved else 2

    def get_moves(self):
        squares = []

        current = list(self.square.pos)

        for offset in self.capture_offsets:
            new = current.copy()
            for _ in range(self.capture_range):
                new[0] += offset[0]
                new[1] += offset[1]
                if new[0] not in range(1, 9) or new[1] not in range(1, 9): break
                sq = self.square.board.get_square_by_pos(new[0], new[1])
                if self.square.board.en_passant_square:
                    if sq == self.square.board.en_passant_square: squares.append(sq)
                if sq.piece:
                    if sq.piece.color != self.color:
                        squares.append(sq)
                else: break

        for offset in self.moving_offsets:
            new = current.copy()
            for _ in range(self.get_move_range()):
                new[0] += offset[0]
                new[1] += offset[1]
                if new[0] not in range(1, 9) or new[1] not in range(1, 9): break
                sq = self.square.board.get_square_by_pos(new[0], new[1])
                if sq.piece: break
                else: squares.append(sq)

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
        final = {}

        for square in candidates:
            result = self.run_test(square)

            def move(sq, promote_to=None):
                if self.square.board.en_passant_square and sq == self.square.board.en_passant_square:
                    self.square.board.get_square_by_pos(sq.file, self.square.rank).clear()
                    self.square.board.en_passant_square = None
                elif self.square.rank - sq.rank in [2, -2]:
                    rank = 3 if self.square.rank == 2 else 6
                    self.square.board.en_passant_square = self.square.board.get_square_by_pos(self.square.file, rank)
                else:
                    self.square.board.en_passant_square = None
                self.move(sq, promote_to)

            if result == "PASSED": final[square.pos] = (move, square)

        return final

    def move(self, square, promote_to=None):
        self.square.board.half_moves = 0
        self.square.board.move = 1 if self.color == 0 else 0
        if self.color == 0: self.square.board.full_moves += 1
        if square.rank in [1, 8]:
            if not promote_to: raise Exception('Need to provide a promotion class.')
            promoted = promote_to(self.color, self.square)
            square.set_piece(self)
            square.set_piece(promoted)
        else:
            square.set_piece(self)
