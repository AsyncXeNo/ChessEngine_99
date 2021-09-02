from game.constants import COLOR_TO_NUM, FILE_TO_NUM, SYMBOL_TO_PIECE


def setup(board, fen):
    fields = fen.split(' ')

    piece_placement = fields[0]
    move = fields[1]
    castling = fields[2]
    en_passant_target = fields[3]
    half_moves = fields[4]
    full_moves = fields[5]

    board.move = COLOR_TO_NUM[move]
    board.en_passant_square = None if en_passant_target == '-' else board.get_square_by_pos(FILE_TO_NUM[en_passant_target[0]], int(en_passant_target[1]))
    board.half_moves = int(half_moves)
    board.full_moves = int(full_moves)

    white_castle_k = True if 'K' in castling else False
    white_castle_q = True if 'Q' in castling else False
    black_castle_k = True if 'k' in castling else False
    black_castle_q = True if 'q' in castling else False

    # Assign pieces and stuff

    file = 1
    rank = 8

    for symbol in piece_placement:
        if symbol.isnumeric(): file += int(symbol)
        elif symbol == '/':
            rank -= 1
            file = 1
        else:
            color = 1 if symbol.isupper() else 0
            piece = SYMBOL_TO_PIECE[symbol.lower()]
            square = board.get_square_by_pos(file, rank)

            if symbol.lower() == 'k':
                if color == 1: square.set_piece(piece(color, square, white_castle_k, white_castle_q))
                if color == 0: square.set_piece(piece(color, square, black_castle_k, black_castle_q))

            else: square.set_piece(piece(color, square))

            file += 1
