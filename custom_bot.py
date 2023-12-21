#!/usr/bin/python3
# -*- coding: utf-8; mode: python -*-
'''Clase dedicada a la creación de bots que jueguen, sin interfaz gráfica'''

from time import sleep


from piece import *
from board import Board
from protocol import *
from node import Node
from functions import *

class CustomBot(object):
    '''Clase del bot'''

    def __init__(self, bot_color, bot_socket, strategy):
        self.bot_color = bot_color
        self.bot_socket = bot_socket
        self.strategy = strategy


    def run(self):
        '''Ejecución del bot'''

        winner_board = None
        winner_color = None

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
                    winner_board = new_fen
                    winner_color = new_board.decode()[4]
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
                        print(new_board)
                        print('WINNER: ' + new_board.decode()[4])

                        winner_board = new_board
                        winner_color = new_board.decode()[4]

            if first_white or first_black:
                sleep(0.5)

            if continue_game:
                bot_node = Node(board)
                if self.strategy == 0:
                    movement_rep = bot_node.random_selection()
                elif self.strategy == 1:
                    movement_rep = bot_node.MCTS(function1)
                elif self.strategy == 2:
                    movement_rep = bot_node.MCTS(function2)
                elif self.strategy == 3:
                    movement_rep = bot_node.MCTS(function3)
                elif self.strategy == 4:
                    movement_rep = bot_node.MCTS(function4)
                elif self.strategy == 5:
                    movement_rep = bot_node.MCTS(function5)
                elif self.strategy == 6:
                    movement_rep = bot_node.MCTS(function6)

                print('BOARD: ' + board.get_representation())
                print('CUSTOM BOT MOVE: ' + movement_rep)
                print('-----------')
                self.bot_socket.sendto((REPLY_CORRECT_MOVE + \
                    movement_rep).encode(),server_end)

                result_move, server = self.bot_socket.recvfrom(1024)
                needs_to_wait = True

                first_white = False
                first_black = False

        return winner_board, winner_color
