from my_logging import get_logger
from game.piece import Piece


logger = get_logger(__name__)


class King(Piece):
    def __init__(self, color, square, castle_k, castle_q):
        super().__init__(color, square)

        self.symbol = 'k'
        self.castle_k = castle_k
        self.castle_q = castle_q
        self.offsets = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)]
        self.castle_k_offset = (2, 0)
        self.castle_q_offset = (-3, 0)
        self.range = 1

    def in_check(self, square):
        enemies = list(filter(lambda piece: piece.color != self.color, self.square.board.get_pieces()))
        for enemy in enemies:
            for sq in enemy.get_moves():
                if square == sq: return True
        return False

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

        # DOESN'T CHECK FOR CASTLING BECAUSE IT IS MORE COMPLICATED AND WILL BE CHECKED DIRECTLY IN get_valid_moves()

    def get_valid_squares(self):
        final = super().get_valid_squares()

        if self.castle_k:
            sq1 = self.square.board.get_square_by_pos(self.square.file + 1, self.square.rank)
            sq2 = self.square.board.get_square_by_pos(self.square.file + 2, self.square.rank)

            if not sq1.piece and not sq2.piece:
                if not self.in_check(sq1) and not self.in_check(sq2): final.append(sq2)

        if self.castle_q:
            sq1 = self.square.board.get_square_by_pos(self.square.file - 1, self.square.rank)
            sq2 = self.square.board.get_square_by_pos(self.square.file - 2, self.square.rank)

            if not sq1.piece and not sq2.piece:
                if not self.in_check(sq1) and not self.in_check(sq2): final.append(sq2)

        return final

    def get_valid_moves(self):
        final = super().get_valid_moves()

        if self.castle_k:
            sq1 = self.square.board.get_square_by_pos(self.square.file + 1, self.square.rank)
            sq2 = self.square.board.get_square_by_pos(self.square.file + 2, self.square.rank)
            k_rook = self.square.board.get_square_by_pos(self.square.file + 3, self.square.rank)

            def move():
                self.move(sq2)
                k_rook.move(sq1)

            if not sq1.piece and not sq2.piece:
                if not self.in_check(sq1) and not self.in_check(sq2): final.append(move)

        if self.castle_q:
            sq1 = self.square.board.get_square_by_pos(self.square.file - 1, self.square.rank)
            sq2 = self.square.board.get_square_by_pos(self.square.file - 2, self.square.rank)
            q_rook = self.square.board.get_square_by_pos(self.square.file - 4, self.square.rank)

            def move():
                self.move(sq2)
                q_rook.move(sq1)

            if not sq1.piece and not sq2.piece:
                if not self.in_check(sq1) and not self.in_check(sq2): final.append(move)

        return final

    def move(self, square):
        self.castle_k = False
        self.castle_q = False
        super().move(square)
