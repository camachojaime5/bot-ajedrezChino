#!/usr/bin/python3
# -*- coding: utf-8; mode: python -*-

import socket
import threading
from custom_bot import CustomBot
from tkinter import *
from protocol import *
from piece import WHITE_PIECE, BLACK_PIECE


GAME_SERVER_END = ('',9999)

RANDOM_STRATEGY = 0
MCTS_2W4L1T = 1
MCTS_EXPOUCT = 2
MCTS_W = 3
MCTS_4W = 4
MCTS_GREEDY = 5
MCTS_EXPO = 6


# CAMBIAR ESTA ESTRATEGIA
TEST_STRATEGY = MCTS_EXPOUCT


class TestBotVsBot(object):
    '''Test de bot vs bot'''

    def run(self):
        '''Ejecuta el test'''
        board = None
        color = None

        bot1_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        bot1_socket.sendto((REQUEST_ADD_GAME + 'Partida1' + PROTOCOL_SEPARATOR + \
            'BOT1').encode(), GAME_SERVER_END)
        result, server = bot1_socket.recvfrom(1024)

        bot2_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        bot2_socket.sendto((REQUEST_ADD_PLAYER_TO_GAME + \
            'Partida1' + PROTOCOL_SEPARATOR + 'BOT2').encode(),GAME_SERVER_END)
        result, server = bot2_socket.recvfrom(1024)

        game_bot1 = CustomBot(WHITE_PIECE, bot1_socket, RANDOM_STRATEGY)
        thr = threading.Thread(target=game_bot1.run, args=tuple())
        thr.start()

        game_bot2 = CustomBot(BLACK_PIECE, bot2_socket, TEST_STRATEGY)
        board, color = game_bot2.run()
        thr.join()

        return board, color
