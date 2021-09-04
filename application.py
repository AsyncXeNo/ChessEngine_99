import sys
import pygame
import socket
import threading

from game.pieces import queen, rook, knight, bishop
from game.board import Board
from game.chess_utils import convert_to_fen


class Application(object):
    def __init__(self, color, width, height, board):
        pygame.init()

        self.PORT = 5678
        self.SERVER = socket.gethostbyname(socket.gethostname())
        self.ADDRESS = (self.SERVER, self.PORT)

        self.HEADER = 256
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = '!DISCONNECT'

        self.color = color
        self.pov = self.color

        self.sprites = {
            ('p', 0): pygame.transform.scale(pygame.image.load('res/pawn.png'), (64, 64)),
            ('r', 0): pygame.transform.scale(pygame.image.load('res/rook.png'), (64, 64)),
            ('n', 0): pygame.transform.scale(pygame.image.load('res/knight.png'), (64, 64)),
            ('b', 0): pygame.transform.scale(pygame.image.load('res/bishop.png'), (64, 64)),
            ('q', 0): pygame.transform.scale(pygame.image.load('res/queen.png'), (64, 64)),
            ('k', 0): pygame.transform.scale(pygame.image.load('res/king.png'), (64, 64)),
            ('p', 1): pygame.transform.scale(pygame.image.load('res/pawn_w.png'), (64, 64)),
            ('r', 1): pygame.transform.scale(pygame.image.load('res/rook_w.png'), (64, 64)),
            ('n', 1): pygame.transform.scale(pygame.image.load('res/knight_w.png'), (64, 64)),
            ('b', 1): pygame.transform.scale(pygame.image.load('res/bishop_w.png'), (64, 64)),
            ('q', 1): pygame.transform.scale(pygame.image.load('res/queen_w.png'), (64, 64)),
            ('k', 1): pygame.transform.scale(pygame.image.load('res/king_w.png'), (64, 64))
        }

        self.running = True

        self.width = width
        self.height = height

        self.side_panel_width = 200

        self.win = pygame.display.set_mode((self.width+self.side_panel_width, self.height))
        pygame.display.set_caption('Chess')

        self.FPS = 12
        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font(None, 32)

        self.board = board
        self.selected = None
        self.promotion_prompt = False

        self.connected = True
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.game_id = None

        self.run()

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.connected = False
                self.running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if pos[0] > self.width: continue
                file, rank = 9 - int((pos[0] // (self.width / 8)) + 1), int((pos[1] // (self.height / 8)) + 1)
                if self.pov: file, rank = 9-file, 9-rank
                square = self.board.get_square_by_pos(file, rank)

                if self.promotion_prompt:
                    if pos[0] < self.width/2:
                        if pos[1] < self.height/2: promote_to = queen.Queen
                        else: promote_to = rook.Rook
                    else:
                        if pos[1] < self.height/2: promote_to = knight.Knight
                        else: promote_to = bishop.Bishop

                    move_func, args = self.selected.get_valid_moves()[self.promotion_prompt.pos]
                    move_func(args, promote_to)
                    self.client.send(f'{self.game_id} {convert_to_fen(self.board)}'.encode(self.FORMAT))
                    self.selected = None
                    self.promotion_prompt = None

                if square.piece:
                    if square.piece.color == self.board.move and square.piece.color == self.color:
                        if self.selected == square.piece: self.selected = None
                        else: self.selected = square.piece
                        continue

                if self.selected:
                    valid_squares = self.selected.get_valid_squares()
                    if square in valid_squares:
                        if self.selected.symbol == 'p' and square.rank in [1, 8]:
                            self.promotion_prompt = square
                            continue
                        move_func, args = self.selected.get_valid_moves()[square.pos]
                        move_func(args)
                        self.client.send(f'{self.game_id} {convert_to_fen(self.board)}'.encode(self.FORMAT))
                        self.selected = None
                    self.selected = None

    def graphics_handler(self):
        self.win.fill((232, 235, 239))

        for file in self.board.squares:
            for square in file:
                # drawing board
                if (square.file + square.rank) % 2 == 0:
                    pygame.draw.rect(
                        self.win,
                        (125, 135, 150),
                        (
                            ((square.file-1)*(self.width/8)),
                            ((8-square.rank)*(self.height/8)),
                            self.width/8,
                            self.height/8
                        )
                    )

        for file in self.board.squares:
            for square in file:
                # do game stuff
                if square.piece:
                    piece_sprite = pygame.transform.scale(self.sprites[(square.piece.symbol, square.piece.color)], (80, 80)) if self.selected == square.piece \
                        else self.sprites[(square.piece.symbol, square.piece.color)]
                    piece_rect = piece_sprite.get_rect()
                    if self.pov == 0:
                        piece_rect.center = (
                            (((9-square.file) - 1) * (self.width / 8)) + self.width / 16,
                            ((8 - (9-square.rank)) * (self.height / 8)) + self.height / 16
                        )
                    else:
                        piece_rect.center = (
                            ((square.file - 1) * (self.width / 8)) + self.width / 16,
                            ((8 - square.rank) * (self.height / 8)) + self.height / 16
                        )
                    self.win.blit(piece_sprite, piece_rect)

        if self.promotion_prompt:
            self.win.fill('grey')

            q = pygame.transform.scale(self.sprites[('q', self.selected.color)], (200, 200))
            q_rect = q.get_rect()
            q_rect.center = (self.width / 4, self.height / 4)
            b = pygame.transform.scale(self.sprites[('b', self.selected.color)], (200, 200))
            b_rect = b.get_rect()
            b_rect.center = (self.width * 3 / 4, self.height * 3 / 4)
            n = pygame.transform.scale(self.sprites[('n', self.selected.color)], (200, 200))
            n_rect = n.get_rect()
            n_rect.center = (self.width * 3 / 4, self.height / 4)
            r = pygame.transform.scale(self.sprites[('r', self.selected.color)], (200, 200))
            r_rect = r.get_rect()
            r_rect.center = (self.width / 4, self.height * 3 / 4)

            self.win.blit(q, q_rect)
            self.win.blit(b, b_rect)
            self.win.blit(n, n_rect)
            self.win.blit(r, r_rect)

        pygame.draw.rect(self.win, (55, 55, 55), (self.width, 0, self.side_panel_width, self.height))

        half_moves_render = self.font.render(f'Half moves: {self.board.half_moves}', False, pygame.Color('black'), None)
        half_moves_render_rect = half_moves_render.get_rect()
        half_moves_render_rect.center = (self.width+(self.side_panel_width/2), self.height/8)

        full_moves_render = self.font.render(f'Full moves: {self.board.full_moves}', False, pygame.Color('black'), None)
        full_moves_render_rect = half_moves_render.get_rect()
        full_moves_render_rect.center = (self.width + (self.side_panel_width / 2), self.height/8 + self.height/16)

        self.win.blit(half_moves_render, half_moves_render_rect)
        self.win.blit(full_moves_render, full_moves_render_rect)
        pygame.display.update()

    def run_client(self):
        self.client.connect(self.ADDRESS)

        while True:
            msg = self.client.recv(self.HEADER).decode(self.FORMAT)
            if msg:
                split = msg.split(' ')
                self.game_id = split.pop(0)
                color = int(split.pop(0))
                self.color = color
                self.pov = color
                self.board = Board(' '.join(split))
                print('Board updated.')
                self.client.send('FIRST MESSAGE'.encode(self.FORMAT))
                break

        while self.connected:
            print('Listening for opp move.')
            msg = self.client.recv(self.HEADER).decode(self.FORMAT)
            if msg:
                self.board = Board(msg)
                print('Board updated.')

        self.client.send('!DISCONNECT'.encode(self.FORMAT))

    # def send_msg(self, msg):
    #     msg = msg.encode(self.FORMAT)
    #     # msg_length = str(len(msg)).encode(self.FORMAT)
    #     # msg_length += b' ' * (self.HEADER - len(msg_length))
    #     # self.client.send(msg_length)
    #     self.client.send(msg.encode(self.FORMAT))

    def run(self):
        server_stuff = threading.Thread(target=self.run_client, args=())
        server_stuff.start()

        while self.running:
            self.event_handler()
            self.graphics_handler()
