import time
import socket
import threading

from my_logging import get_logger
from game.board import Board
from game.constants import BASE_FEN
from game.chess_utils import generate_id


HEADER = 256
FORMAT = 'utf-8'

DISCONNECT_MESSAGE = '!DISCONNECT'

PORT = 5678
SERVER = ''
ADDRESS = (SERVER, PORT)

logger = get_logger(__name__)

games = {}
conns = {}
hold = None


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDRESS)

    logger.info('Starting server...')
    runserver(server)


def handle_client(conn, address):
    logger.info(f'{address} connected.')

    connected = True
    while connected:
        time.sleep(0.5)
        board = Board(games[conns[conn]][2])
        if board.move == games[conns[conn]].index(conn):
            msg = conn.recv(HEADER).decode(FORMAT)
        else: continue
        logger.info(f'Message received from {address}.')
        if msg:
            if msg == DISCONNECT_MESSAGE:
                connected = False

            else:
                split = msg.split(' ')

                game_id = split.pop(0)
                fen = ' '.join(split)

                games[game_id][2] = fen

                index = 1 if games[conns[conn]].index(conn) == 0 else 0

                conn.send(fen.encode(FORMAT))

                if games[conns[conn]][index]:
                    games[conns[conn]][index].send(fen.encode(FORMAT))

            logger.info(f'[{address}] {msg}')

    conn.close()


def runserver(server):
    global hold

    server.listen()
    logger.info(f'Server is listening on {SERVER}')

    while True:
        conn, address = server.accept()

        if not hold:
            game_id = generate_id()
            games[game_id] = [conn, None, BASE_FEN]
            conns[conn] = game_id
            msg = f'{game_id} 0 {games[game_id][2]}'.encode(FORMAT)
            # msg_length = str(len(msg)).encode(FORMAT)
            # conn.send(msg_length)
            conn.send(msg)
            hold = game_id

        elif hold:
            games[hold][1] = conn
            conns[conn] = hold
            msg = f'{hold} 1 {games[hold][2]}'.encode(FORMAT)
            # msg_length = str(len(msg)).encode(FORMAT)
            # conn.send(msg_length)
            conn.send(msg)
            hold = None

        first_msg = conn.recv(64)
        logger.info(f'{address}: {first_msg.decode(FORMAT)}')
        thread = threading.Thread(target=handle_client, args=(conn, address))
        thread.start()
        logger.info(f'Active connections: {threading.active_count() - 1}')


if __name__ == '__main__':
    main()
