''' Module related to chinese chess games '''

import copy
import threading
import uuid
import socket

from piece import WHITE_PIECE, King
from piece import BLACK_PIECE
from persistence import input_json
from board import Board
from protocol import *
from movement_converter import *

DEFAULT_BOARD = 'position1.json'
DEFAULT_HOST = ''
DEFAULT_PORT = 0
DEFAULT_BUFFER = 1024

BOT_NAMES = ['BOT1','BOT2']

class Game():
    ''' Class definition for a chinese chess game '''
    game_id = 1
    def __init__(self, player1 = None, player2 = None, name = None, game_server = None, username1 = None, username2 = None):
        ''' Constructor for game type '''
        self.id = Game.game_id
        self.player1 = player1 # Must be a socket
        self.player2 = player2 # Must be a socket
        self.turn = WHITE_PIECE
        self.board = Board(input_json(DEFAULT_BOARD))
        self.game_lock = threading.Lock()
        self.game_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.game_socket.bind((DEFAULT_HOST, DEFAULT_PORT)) 
        self.player1_tie = False
        self.player2_tie = False
        self.game_server = game_server
        self.username1 = username1
        self.username2 = username2
        if name is None or name == '':
            self.name = uuid.uuid4()
        else:
            self.name = name
        Game.game_id += 1 # The count must increase


    def __str__(self):
        ''' String representation of a game '''
        return self.name


    def __repr__(self):
        ''' String representation of a game '''
        return self.name


    def insert_player(self, player):
        ''' Method to add player to game without race condition '''
        added_player = False
        self.game_lock.acquire()
        if not self.player1:
            self.player1 = player
            added_player = True
        elif not self.player2:
            self.player2 = player
            added_player = True

        self.game_lock.release()
        return added_player


    def handle_tie_messages(self, player, message):
        ''' Method to handle tie messages '''
        code = message[IDENTIFIER_BEGIN : IDENTIFIER_END]
        if code == REQUEST_TIE:
            if player == self.player1:
                self.player1_tie = True
            elif player == self.player2:
                self.player2_tie = True
            if self.player1_tie and self.player2_tie:
                return
            self.game_socket.sendto(REPLY_TIE.encode(), self.player1)
            self.game_socket.sendto(REPLY_TIE.encode(), self.player2)


    def play(self):
        ''' Method to play the game until finished '''
        while not self.is_game_finished():
            self.game_socket.sendto(
                self.board.get_representation().encode(),
                self.player1
            )
            self.game_socket.sendto(
                self.board.get_representation().encode(),
                self.player2
            )
            is_valid_play = False
            while not is_valid_play:
                player = None
                if self.turn == WHITE_PIECE:
                    while player != self.player1:
                        self.game_socket.sendto(REQUEST_CORRECT_MOVE.encode(),self.player1)
                        movement, player = self.game_socket.recvfrom(DEFAULT_BUFFER)
                        movement = movement.decode()
                        self.handle_tie_messages(player, movement)
                        code = movement[IDENTIFIER_BEGIN : IDENTIFIER_END]
                        if code == REQUEST_DEFEAT: # Checks for surrender message from p1 or p2
                            if player == self.player1:
                                winner = BLACK_PIECE
                            else:
                                winner = WHITE_PIECE
                            result = (MSG_GAME_FINISHED + winner).encode()
                            self.game_socket.sendto(result, self.player1)
                            self.game_socket.sendto(result, self.player2)
                            return
                        elif self.player1_tie and self.player2_tie:
                            result = (MSG_GAME_FINISHED + IDENTIFIER_TIE).encode()
                            self.game_socket.sendto(result, self.player1)
                            self.game_socket.sendto(result, self.player2)
                            return
                else:
                    while player != self.player2:
                        self.game_socket.sendto(REQUEST_CORRECT_MOVE.encode(),self.player2)
                        movement, player = self.game_socket.recvfrom(DEFAULT_BUFFER)
                        movement = movement.decode()
                        code = movement[IDENTIFIER_BEGIN : IDENTIFIER_END]
                        self.handle_tie_messages(player, movement)
                        if code == REQUEST_DEFEAT: # Checks for surrender message from p1 or p2
                            if player == self.player1:
                                winner = BLACK_PIECE
                            else:
                                winner = WHITE_PIECE
                            result = (MSG_GAME_FINISHED + winner).encode()
                            self.game_socket.sendto(result, self.player1)
                            self.game_socket.sendto(result, self.player2)
                            return
                        elif self.player1_tie and self.player2_tie:
                            result = (MSG_GAME_FINISHED + IDENTIFIER_TIE).encode()
                            self.game_socket.sendto(result, self.player1)
                            self.game_socket.sendto(result, self.player2)
                            return

                movement_code = movement[IDENTIFIER_BEGIN : IDENTIFIER_END]
                movement = movement[IDENTIFIER_END : ]
                copy_board = copy.deepcopy(self.board)
                if movement_code == REQUEST_TIE:
                    pass
                elif movement_code == REPLY_CORRECT_MOVE:
                    moved_piece, position = movement_converter(self.board, movement,
                        self.board.side_to_move)
                    new_board = moved_piece.perform_movement(self.board, position)[0]
                    if copy_board.validar_movimiento(new_board):
                        self.game_socket.sendto(REPLY_CORRECT_MOVE.encode(), player)
                        is_valid_play = True
                    else:
                        self.game_socket.sendto(ILLEGAL_MOVE.encode(), player)
                else:
                    self.game_socket.sendto(ILLEGAL_MOVE.encode(), player)

            if self.turn == WHITE_PIECE:
                self.turn = BLACK_PIECE
            else:
                self.turn = WHITE_PIECE

        if self.get_winner() is None:
            result = (MSG_GAME_FINISHED + IDENTIFIER_TIE + \
                self.board.get_representation()).encode()
            self.game_server.update_elo(IDENTIFIER_TIE, self.username1,
                self.username1, self.board, WHITE_PIECE)
        else:
            result = (MSG_GAME_FINISHED + self.get_winner() + \
                self.board.get_representation()).encode()
            if self.get_winner() == WHITE_PIECE:
                if not (self.username1 in BOT_NAMES or \
                    self.username2 in BOT_NAMES):
                    self.game_server.update_elo(WHITE_PIECE, self.username1,
                        self.username2, self.board, WHITE_PIECE)
            else:
                if not (self.username1 in BOT_NAMES or \
                    self.username2 in BOT_NAMES):
                    self.game_server.update_elo(BLACK_PIECE, self.username2,
                        self.username1, self.board, BLACK_PIECE)

        self.game_socket.sendto(result, self.player1)
        self.game_socket.sendto(result, self.player2)


    def get_winner(self):
        ''' Method to get the winner of a game '''
        white_king = False
        black_king = False

        for white_piece in self.board.board[WHITE_PIECE]:
            if type(white_piece) == King:
                white_king = True
                break
        for black_piece in self.board.board[BLACK_PIECE]:
            if type(black_piece) == King:
                black_king = True
                break

        if white_king and not black_king:
            return WHITE_PIECE
        if black_king and not white_king:
            return BLACK_PIECE
        return None


    def is_game_finished(self):
        ''' Method to check if game is finished '''
        game_result = self.get_winner()
        if game_result is None:
            return False
        return True
