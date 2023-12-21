#!/usr/bin/python3
# -*- coding: utf-8; mode: python -*-
'''Clase dedicada a la creación de bots que jueguen, sin interfaz gráfica'''


from piece import *
from board import Board
from protocol import *
from node import Node
from time import sleep


class Bot(object):
    '''Clase del bot'''

    def __init__(self, bot_color, bot_socket):
        self.bot_color = bot_color
        self.bot_socket = bot_socket


    def run(self):
        '''Ejecución del bot'''

        init_fen, server = self.bot_socket.recvfrom(1024)
        server_end = server

        board = Board()
        board.build(init_fen.decode())

        first_white = True
        first_black = True
        needs_to_wait = False

        continue_game = True
        while continue_game:
            if self.bot_color is WHITE_PIECE and first_white:
                result, server = self.bot_socket.recvfrom(1024)
            elif self.bot_color is BLACK_PIECE and first_black:
                new_board, server = self.bot_socket.recvfrom(1024)

                if new_board.decode() == REPLY_TIE:
                    result, server = self.bot_socket.recvfrom(1024)
                if new_board.decode()[0:4] == MSG_GAME_FINISHED:
                    final_board = new_board[5:]

                    if len(final_board.decode()) > 3:
                        new_fen = final_board.decode()
                        board.build(new_fen)

                    continue_game = False
                elif new_board.decode()[0:4] == REPLY_TIE:
                    result, server = self.bot_socket.recvfrom(1024)
                else:
                    new_fen = new_board.decode()
                    board.build(new_fen)

                    result, server = self.bot_socket.recvfrom(1024)


            if needs_to_wait:
                new_board, server = self.bot_socket.recvfrom(1024)
                needs_to_wait = False

                if new_board.decode() == REPLY_TIE:
                    new_board, server = self.bot_socket.recvfrom(1024)
                elif new_board.decode()[0:4] == MSG_GAME_FINISHED:
                    final_board = new_board[5:]

                    if len(final_board.decode()) > 3:
                        new_fen = final_board.decode()
                        board.build(new_fen)

                    continue_game = False
                else:
                    new_board, server = self.bot_socket.recvfrom(1024)

                    if new_board.decode() == REPLY_TIE:
                        new_board, server = self.bot_socket.recvfrom(1024)

                    if not new_board.decode()[0:4] == MSG_GAME_FINISHED:
                        new_fen = new_board.decode()
                        board.build(new_fen)

                        result, server = self.bot_socket.recvfrom(1024)
                    else:
                        final_fen = new_board[5:].decode()

                        if len(final_fen) > 3:
                            board.build(new_fen)

                        continue_game = False

            if first_white or first_black:
                sleep(0.5)

            if continue_game:
                bot_node = Node(board)
                movement_rep = bot_node.MCTS()
                self.bot_socket.sendto((REPLY_CORRECT_MOVE + \
                    movement_rep).encode(),server_end)

                result_move, server = self.bot_socket.recvfrom(1024)
                needs_to_wait = True

                first_white = False
                first_black = False
