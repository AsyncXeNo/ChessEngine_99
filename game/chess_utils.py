import string
import random
import json

from game.constants import NUM_TO_COLOR, COLOR_TO_NUM, FILE_TO_NUM, SYMBOL_TO_PIECE


def convert_to_fen(board):
    move = NUM_TO_COLOR[board.move]
    castling = ''
    if list(filter(lambda piece: piece.symbol == 'k' and piece.color == 1, board.get_pieces()))[0].castle_k: castling += 'K'
    if list(filter(lambda piece: piece.symbol == 'k' and piece.color == 1, board.get_pieces()))[0].castle_q: castling += 'Q'
    if list(filter(lambda piece: piece.symbol == 'k' and piece.color == 0, board.get_pieces()))[0].castle_k: castling += 'k'
    if list(filter(lambda piece: piece.symbol == 'k' and piece.color == 0, board.get_pieces()))[0].castle_q: castling += 'q'
    en_passant_target_square = '-' if not board.en_passant_square else board.en_passant_square.get_name()
    half_moves = board.half_moves
    full_moves = board.full_moves

    rows = []
    empty = 0
    for rank in range(8, 0, -1):
        row = ''
        for file in range(1, 9):
            square = board.get_square_by_pos(file, rank)
            if not square.piece: empty += 1
            else:
                if empty:
                    row += str(empty)
                    empty = 0
                row += square.piece.symbol if not square.piece.color else square.piece.symbol.upper()
        if empty:
            row += str(empty)
            empty = 0
        rows.append(row)

    piece_placement = '/'.join(rows)

    return ' '.join([piece_placement, move, castling, en_passant_target_square, str(half_moves), str(full_moves)])


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


def generate_id(length=6):
    with open("data/generated_ids.json", "r") as f:
        generated = json.load(f)

    gen = "".join(random.choices(string.ascii_uppercase, k=length))
    while gen in generated:
        gen = ''.join(random.choices(string.ascii_uppercase, k=length))

    generated.append(gen)

    with open("data/generated_ids.json", "w") as f:
        json.dump(generated, f, indent=4)

    return gen
