#!/usr/bin/python3
# -*- coding: utf-8; mode: python -*-
'''Clase dedicada a la representación gráfica del tablero y sus fichas'''

from time import sleep
from tkinter import messagebox
from piece import *
from board import Board
from tkinter import *
import copy
import pygame
from pygame.locals import *
from protocol import *
from node import Node


GAME_SERVER_END = ('',9999)


WIDTH = 600
HEIGHT = 623

HORIZONTAL_FACTOR = 48.8
VERTICAL_FACTOR = 50
HORIZONTAL_DEVIATION = 0.07
VERTICAL_DEVIATION = 0.05
HITBOX_MARGIN = 20

BUTTON_HORIZONTAL_MARGIN = 40
BUTTON_VERTICAL_MARGIN = 513
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 60

WHITE_COLOR = (255,255,255)
RED_COLOR = (255,0,0)
BLACK_COLOR = (0,0,0)

RED_TURN_STRING = 'Current turn: RED'
BLACK_TURN_STRING = 'Current turn: BLACK'

CAPTION = 'Ajedrez chino'


class Graphic_game(object):
    '''Clase para la representación del juego'''

    def __init__(self, user_socket, user_color, bot = False, vs_bot = False):
        self.name = 'Partida1'
        self.surrender = False
        self.call_tie = False
        self.user_socket = user_socket
        self.user_color = user_color
        self.bot = bot
        self.vs_bot = vs_bot


    def run(self):
        '''Comienza el juego'''
        pygame.init()

        display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
        display_surface.fill(WHITE_COLOR)
        pygame.display.set_caption(CAPTION)

        #Margen X = 23px
        #Margen Y = 20 px
        #Casilla = 50x50
        #Boton = 100x60
        board_img = pygame.image.load(r'imagenes/tablero.png')
        horizontal_bg = pygame.image.load(r'imagenes/backgroundH.jpg')
        vertical_bg = pygame.image.load(r'imagenes/backgroundV.jpg')
        button_show = pygame.image.load(r'imagenes/buttonShow.png')
        button_tie00 = pygame.image.load(r'imagenes/buttonTie00.png')
        button_tie01 = pygame.image.load(r'imagenes/buttonTie01.png')
        button_tie10 = pygame.image.load(r'imagenes/buttonTie10.png')
        button_tie11 = pygame.image.load(r'imagenes/buttonTie11.png')
        button_exit = pygame.image.load(r'imagenes/buttonExit.png')
        button_surrender = pygame.image.load(r'imagenes/buttonSurrender.png')

        images = dict.fromkeys(('a', 'c', 'e', 'h', 'k', 'p', 'r', 'A', 'C', 'E', \
            'H', 'K', 'P', 'R'))
        #Ficha = 40x40
        images['a'] = pygame.image.load(r'imagenes/a-n.png')
        images['c'] = pygame.image.load(r'imagenes/c-n.png')
        images['e'] = pygame.image.load(r'imagenes/e-n.png')
        images['h'] = pygame.image.load(r'imagenes/h-n.png')
        images['k'] = pygame.image.load(r'imagenes/k-n.png')
        images['p'] = pygame.image.load(r'imagenes/p-n.png')
        images['r'] = pygame.image.load(r'imagenes/r-n.png')

        images['A'] = pygame.image.load(r'imagenes/a-r.png')
        images['C'] = pygame.image.load(r'imagenes/c-r.png')
        images['E'] = pygame.image.load(r'imagenes/e-r.png')
        images['H'] = pygame.image.load(r'imagenes/h-r.png')
        images['K'] = pygame.image.load(r'imagenes/k-r.png')
        images['P'] = pygame.image.load(r'imagenes/p-r.png')
        images['R'] = pygame.image.load(r'imagenes/r-r.png')

        # Recibimos el FEN inicial
        init_fen, server = self.user_socket.recvfrom(1024)
        server_end = server

        board_implementation = Board()
        board_implementation.build(init_fen.decode())

        state = init_fen.decode().split()
        board = state[0].split('/')

        highlighted_positions = set()
        selected_piece = None

        current_turn = state[1]
        current_turn_string = RED_TURN_STRING
        current_turn_color = RED_COLOR

        if self.user_color is WHITE_PIECE:
            state_string = 'Your turn!'
            state_color = RED_COLOR
            color_string = 'Your color is: RED'
            color_color = RED_COLOR
        else:
            state_string = 'Waiting for red move...'
            state_color = BLACK_COLOR
            color_string = 'Your color is: BLACK'
            color_color = BLACK_COLOR

        movement_title_string = 'MOVEMENTS'

        movement_labels = []
        movement_strings = []
        performed_movements = []
        movement_counter = 0
        post_movement_counter = 0

        first_white = True
        first_black = True
        needs_to_wait = False
        is_finished = False
        asked_tie = False
        rival_tie = False

        impact_font = pygame.font.SysFont('impact', 21)
        helvetica_font = pygame.font.SysFont('helvetica',12)

        for i in range(26):
            movement_strings.append('')
            movement_labels.append(helvetica_font.render('', 1, BLACK_COLOR))

        #Game Loop
        continue_game = True
        while continue_game:
            display_surface.fill(WHITE_COLOR)
            display_surface.blit(board_img, (0, 0))

            display_surface.blit(horizontal_bg, (0,493))
            display_surface.blit(vertical_bg, (440,0))

            display_surface.blit(button_surrender, (40,513))
            display_surface.blit(button_show, (320,513))
            display_surface.blit(button_exit, (460,513))

            if asked_tie:
                if rival_tie:
                    display_surface.blit(button_tie11, (180,513))
                else:
                    if self.user_color == WHITE_PIECE:
                        display_surface.blit(button_tie10, (180,513))
                    else:
                        display_surface.blit(button_tie01, (180,513))
            else:
                if rival_tie:
                    if self.user_color == WHITE_PIECE:
                        display_surface.blit(button_tie01, (180,513))
                    else:
                        display_surface.blit(button_tie10, (180,513))
                else:
                    display_surface.blit(button_tie00, (180,513))

            turn_label = impact_font.render(current_turn_string, 1, current_turn_color)
            color_label = impact_font.render(color_string, 1, color_color)
            state_label = impact_font.render(state_string, 1, state_color)
            movement_title_label = impact_font.render(movement_title_string, 1, BLACK_COLOR)

            display_surface.blit(turn_label, (450, 10))
            display_surface.blit(color_label, (450, 468))
            display_surface.blit(state_label, (10, 602))
            display_surface.blit(movement_title_label, (472, 45))

            #Inicializa las labels de los movimientos
            for i in range(26):
                movement_labels[i] = helvetica_font.render(movement_strings[i], 1, BLACK_COLOR)
                display_surface.blit(movement_labels[i], (490, 65 + 15 * i))

            pygame.draw.line(display_surface,BLACK_COLOR,(440,35),(600,35))
            pygame.draw.line(display_surface,BLACK_COLOR,(440,458),(600,458))
            pygame.draw.line(display_surface,BLACK_COLOR,(0,493),(600,493),2)
            pygame.draw.line(display_surface,BLACK_COLOR,(440,0),(440,493),2)
            pygame.draw.line(display_surface,BLACK_COLOR,(0,593),(600,593),2)

            self.update_pieces_display(board, images, display_surface)

            if selected_piece is not None and not is_finished:
                movements = selected_piece.get_possible_movements(board_implementation)
                if movements is not None:
                    for mov in movements:
                        self.print_possible_movement(mov, display_surface,
                            highlighted_positions)

            pygame.display.update()

            if self.user_color is WHITE_PIECE and first_white:
                result, server = self.user_socket.recvfrom(1024)
                first_white = False
            elif self.user_color is BLACK_PIECE and first_black:
                new_board, server = self.user_socket.recvfrom(1024)
                first_black = False

                if new_board.decode() == REPLY_TIE:
                    if asked_tie:
                        if self.user_color == WHITE_PIECE:
                            display_surface.blit(button_tie10, (180,513))
                        else:
                            display_surface.blit(button_tie01, (180,513))
                    else:
                        if self.user_color == WHITE_PIECE:
                            display_surface.blit(button_tie01, (180,513))
                            rival_tie = True
                        else:
                            display_surface.blit(button_tie10, (180,513))
                            rival_tie = True
                    pygame.display.update()
                    new_board, server = self.user_socket.recvfrom(1024)

                if new_board.decode()[0:4] == MSG_GAME_FINISHED:
                    if new_board.decode()[4:] == IDENTIFIER_TIE:
                        asked_tie = True
                        rival_tie = True
                        if not self.vs_bot:
                            messagebox.showinfo(message="It's a tie.",
                                title="Finished game")
                        is_finished = True
                        if self.user_color == WHITE_COLOR:
                            current_turn_color = BLACK_COLOR
                        else:
                            current_turn_color = WHITE_COLOR
                        state_string = "It's a tie."
                    elif new_board.decode()[4] == self.user_color:
                        if not self.vs_bot:
                            messagebox.showinfo(message="You win!",
                                title="Finished game")
                        is_finished = True
                        if self.user_color == WHITE_COLOR:
                            current_turn_color = BLACK_COLOR
                        else:
                            current_turn_color = WHITE_COLOR
                        state_string = 'You win!'
                    else :
                        if not self.vs_bot:
                            messagebox.showinfo(message="You lose...",
                                title="Finished game")
                        is_finished = True
                        if self.user_color == WHITE_COLOR:
                            current_turn_color = BLACK_COLOR
                        else:
                            current_turn_color = WHITE_COLOR
                        state_string = 'You lose...'

                    final_board = new_board[5:]

                    if len(final_board.decode()) > 3:
                        copy_board = copy.deepcopy(board_implementation)
                        new_fen = final_board.decode()
                        split_fen = new_fen.split()
                        board = split_fen[0].split('/')
                        board_implementation.build(new_fen)

                        if self.user_color == WHITE_PIECE:
                            new_color = BLACK_PIECE
                        else:
                            new_color = WHITE_PIECE

                        movement_rep = copy_board.board_difference(board_implementation,
                            new_color)
                        performed_movements.append(movement_rep)

                        if movement_counter < 26:
                            if movement_counter % 2 == 0:
                                movement_strings[movement_counter] = \
                                    str(int((movement_counter/2)+1)) \
                                    + '.  ' + movement_rep
                            else:
                                movement_strings[movement_counter] = '    ' + \
                                    movement_rep
                            movement_counter += 1
                        else:
                            for i in range(25):
                                movement_strings[i] = movement_strings[i+1]

                            if post_movement_counter % 2 == 0:
                                movement_strings[25] = \
                                    str(int(((movement_counter + \
                                    post_movement_counter)/2)+1)) \
                                    + '.  ' + movement_rep
                            else:
                                movement_strings[25] = '    ' + movement_rep

                            post_movement_counter += 1
                elif new_board.decode()[0:4] == REPLY_TIE:
                    if asked_tie:
                        if self.user_color == WHITE_PIECE:
                            display_surface.blit(button_tie10, (180,513))
                        else:
                            display_surface.blit(button_tie01, (180,513))
                    else:
                        if self.user_color == WHITE_PIECE:
                            display_surface.blit(button_tie01, (180,513))
                            rival_tie = True
                        else:
                            display_surface.blit(button_tie10, (180,513))
                            rival_tie = True
                    pygame.display.update()
                    result, server = self.user_socket.recvfrom(1024)
                else:
                    copy_board = copy.deepcopy(board_implementation)
                    new_fen = new_board.decode()
                    split_fen = new_fen.split()
                    board = split_fen[0].split('/')

                    board_implementation.build(new_fen)

                    if self.user_color == WHITE_PIECE:
                        new_color = BLACK_PIECE
                    else:
                        new_color = WHITE_PIECE

                    movement_rep = copy_board.board_difference(board_implementation,
                        new_color)
                    performed_movements.append(movement_rep)

                    if movement_counter < 26:
                        if movement_counter % 2 == 0:
                            movement_strings[movement_counter] = \
                                str(int((movement_counter/2)+1)) \
                                + '.  ' + movement_rep
                        else:
                            movement_strings[movement_counter] = '    ' + \
                                movement_rep
                        movement_counter += 1
                    else:
                        for i in range(25):
                            movement_strings[i] = movement_strings[i+1]

                        if post_movement_counter % 2 == 0:
                            movement_strings[25] = \
                                str(int(((movement_counter + \
                                post_movement_counter)/2)+1)) \
                                + '.  ' + movement_rep
                        else:
                            movement_strings[25] = '    ' + movement_rep

                        post_movement_counter += 1

                    if current_turn == WHITE_PIECE:
                        current_turn_string = BLACK_TURN_STRING
                        current_turn_color = BLACK_COLOR
                    else:
                        current_turn_string = RED_TURN_STRING
                        current_turn_color = RED_COLOR
                    current_turn = split_fen[1]

                    state_string = 'Your turn!'
                    result, server = self.user_socket.recvfrom(1024)

            if needs_to_wait:
                new_board, server = self.user_socket.recvfrom(1024)
                needs_to_wait = False

                if new_board.decode() == REPLY_TIE:
                    if asked_tie:
                        if self.user_color == WHITE_PIECE:
                            display_surface.blit(button_tie10, (180,513))
                        else:
                            display_surface.blit(button_tie01, (180,513))
                    else:
                        if self.user_color == WHITE_PIECE:
                            display_surface.blit(button_tie01, (180,513))
                            rival_tie = True
                        else:
                            display_surface.blit(button_tie10, (180,513))
                            rival_tie = True
                    pygame.display.update()
                    new_board, server = self.user_socket.recvfrom(1024)

                if new_board.decode()[0:4] == MSG_GAME_FINISHED:
                    if new_board.decode()[4:] == IDENTIFIER_TIE:
                        asked_tie = True
                        rival_tie = True
                        if not self.vs_bot:
                            messagebox.showinfo(message="It's a tie.",
                                title="Finished game")
                        is_finished = True
                        if self.user_color == WHITE_COLOR:
                            current_turn_color = BLACK_COLOR
                        else:
                            current_turn_color = WHITE_COLOR
                        state_string = "It's a tie."
                    elif new_board.decode()[4] == self.user_color:
                        if not self.vs_bot:
                            messagebox.showinfo(message="You win!", title="Finished game")
                        is_finished = True
                        if self.user_color == WHITE_COLOR:
                            current_turn_color = BLACK_COLOR
                        else:
                            current_turn_color = WHITE_COLOR
                        state_string = 'You win!'
                    else:
                        if not self.vs_bot:
                            messagebox.showinfo(message="You lose...", title="Finished game")
                        is_finished = True
                        if self.user_color == WHITE_COLOR:
                            current_turn_color = BLACK_COLOR
                        else:
                            current_turn_color = WHITE_COLOR
                        state_string = 'You lose...'

                    if self.bot:
                        display_surface.blit(state_label, (10, 602))
                        pygame.display.update()

                    final_board = new_board[5:]

                    if len(final_board.decode()) > 3:
                        copy_board = copy.deepcopy(board_implementation)
                        new_fen = final_board.decode()
                        split_fen = new_fen.split()
                        board = split_fen[0].split('/')
                        board_implementation.build(new_fen)

                        if self.user_color == WHITE_PIECE:
                            new_color = BLACK_PIECE
                        else:
                            new_color = WHITE_PIECE

                        if not self.bot:
                            movement_rep = copy_board.board_difference(board_implementation,
                                new_color)
                            performed_movements.append(movement_rep)

                            if movement_counter < 26:
                                if movement_counter % 2 == 0:
                                    movement_strings[movement_counter] = \
                                        str(int((movement_counter/2)+1)) \
                                        + '.  ' + movement_rep
                                else:
                                    movement_strings[movement_counter] = '    ' + \
                                        movement_rep
                                movement_counter += 1
                            else:
                                for i in range(25):
                                    movement_strings[i] = movement_strings[i+1]

                                if post_movement_counter % 2 == 0:
                                    movement_strings[25] = \
                                        str(int(((movement_counter + \
                                        post_movement_counter)/2)+1)) \
                                        + '.  ' + movement_rep
                                else:
                                    movement_strings[25] = '    ' + movement_rep

                                post_movement_counter += 1
                        else:
                            state_string = 'Exiting in 20 seconds...'
                            display_surface.fill(WHITE_COLOR)
                            display_surface.blit(board_img, (0, 0))

                            display_surface.blit(horizontal_bg, (0,493))
                            display_surface.blit(vertical_bg, (440,0))

                            display_surface.blit(button_surrender, (40,513))
                            display_surface.blit(button_show, (320,513))
                            display_surface.blit(button_exit, (460,513))

                            if asked_tie:
                                if rival_tie:
                                    display_surface.blit(button_tie11, (180,513))
                                else:
                                    if self.user_color == WHITE_PIECE:
                                        display_surface.blit(button_tie10, (180,513))
                                    else:
                                        display_surface.blit(button_tie01, (180,513))
                            else:
                                if rival_tie:
                                    if self.user_color == WHITE_PIECE:
                                        display_surface.blit(button_tie01, (180,513))
                                    else:
                                        display_surface.blit(button_tie10, (180,513))
                                else:
                                    display_surface.blit(button_tie00, (180,513))

                            turn_label = impact_font.render(current_turn_string, 1,
                                current_turn_color)
                            color_label = impact_font.render(color_string, 1, color_color)
                            state_label = impact_font.render(state_string, 1, state_color)
                            movement_title_label = impact_font.render(movement_title_string,
                                1, BLACK_COLOR)

                            display_surface.blit(turn_label, (450, 10))
                            display_surface.blit(color_label, (450, 468))
                            display_surface.blit(state_label, (10, 602))
                            display_surface.blit(movement_title_label, (472, 45))

                            for i in range(26):
                                movement_labels[i] = helvetica_font.render(movement_strings[i],
                                    1, BLACK_COLOR)
                                display_surface.blit(movement_labels[i], (490, 65 + 15 * i))

                            pygame.draw.line(display_surface,BLACK_COLOR,(440,35),(600,35))
                            pygame.draw.line(display_surface,BLACK_COLOR,(440,458),(600,458))
                            pygame.draw.line(display_surface,BLACK_COLOR,(0,493),(600,493),2)
                            pygame.draw.line(display_surface,BLACK_COLOR,(440,0),(440,493),2)
                            pygame.draw.line(display_surface,BLACK_COLOR,(0,593),(600,593),2)

                            self.update_pieces_display(board, images, display_surface)

                            pygame.display.update()

                            sleep(20)
                            continue_game = False
                            pygame.quit()
                elif new_board.decode()[0:4] == REPLY_TIE:
                    if asked_tie:
                        if self.user_color == WHITE_PIECE:
                            display_surface.blit(button_tie10, (180,513))
                        else:
                            display_surface.blit(button_tie01, (180,513))
                    else:
                        if self.user_color == WHITE_PIECE:
                            display_surface.blit(button_tie01, (180,513))
                            rival_tie = True
                        else:
                            display_surface.blit(button_tie10, (180,513))
                            rival_tie = True
                    pygame.display.update()
                    result, server = self.user_socket.recvfrom(1024)
                else:
                    if new_board.decode() == REPLY_CORRECT_MOVE:
                        new_board, server = self.user_socket.recvfrom(1024)

                    if self.bot:
                        new_board, server = self.user_socket.recvfrom(1024)

                    copy_board = copy.deepcopy(board_implementation)
                    new_fen = new_board.decode()
                    split_fen = new_fen.split()
                    board = split_fen[0].split('/')
                    board_implementation.build(new_fen)

                    if self.user_color == WHITE_PIECE:
                        new_color = BLACK_PIECE
                    else:
                        new_color = WHITE_PIECE

                    movement_rep = copy_board.board_difference(board_implementation,
                        new_color)
                    performed_movements.append(movement_rep)

                    if movement_counter < 26:
                        if movement_counter % 2 == 0:
                            movement_strings[movement_counter] = \
                                str(int((movement_counter/2)+1)) \
                                + '.  ' + movement_rep
                        else:
                            movement_strings[movement_counter] = '    ' + \
                                movement_rep
                        movement_counter += 1
                    else:
                        for i in range(25):
                            movement_strings[i] = movement_strings[i+1]

                        if post_movement_counter % 2 == 0:
                            movement_strings[25] = \
                                str(int(((movement_counter + \
                                post_movement_counter)/2)+1)) \
                                + '.  ' + movement_rep
                        else:
                            movement_strings[25] = '    ' + movement_rep

                        post_movement_counter += 1

                    if current_turn == WHITE_PIECE:
                        current_turn_string = BLACK_TURN_STRING
                        current_turn_color = BLACK_COLOR
                    else:
                        current_turn_string = RED_TURN_STRING
                        current_turn_color = RED_COLOR
                    current_turn = split_fen[1]

                    state_string = 'Your turn!'

                    if self.bot:
                        display_surface.fill(WHITE_COLOR)
                        display_surface.blit(board_img, (0, 0))

                        display_surface.blit(horizontal_bg, (0,493))
                        display_surface.blit(vertical_bg, (440,0))

                        display_surface.blit(button_surrender, (40,513))
                        display_surface.blit(button_show, (320,513))
                        display_surface.blit(button_exit, (460,513))

                        if asked_tie:
                            if rival_tie:
                                display_surface.blit(button_tie11, (180,513))
                            else:
                                if self.user_color == WHITE_PIECE:
                                    display_surface.blit(button_tie10, (180,513))
                                else:
                                    display_surface.blit(button_tie01, (180,513))
                        else:
                            if rival_tie:
                                if self.user_color == WHITE_PIECE:
                                    display_surface.blit(button_tie01, (180,513))
                                else:
                                    display_surface.blit(button_tie10, (180,513))
                            else:
                                display_surface.blit(button_tie00, (180,513))

                        turn_label = impact_font.render(current_turn_string, 1,
                            current_turn_color)
                        color_label = impact_font.render(color_string, 1, color_color)
                        state_label = impact_font.render(state_string, 1, state_color)
                        movement_title_label = impact_font.render(movement_title_string,
                            1, BLACK_COLOR)

                        display_surface.blit(turn_label, (450, 10))
                        display_surface.blit(color_label, (450, 468))
                        display_surface.blit(state_label, (10, 602))
                        display_surface.blit(movement_title_label, (472, 45))

                        for i in range(26):
                            movement_labels[i] = helvetica_font.render(movement_strings[i],
                                1, BLACK_COLOR)
                            display_surface.blit(movement_labels[i], (490, 65 + 15 * i))

                        pygame.draw.line(display_surface,BLACK_COLOR,(440,35),(600,35))
                        pygame.draw.line(display_surface,BLACK_COLOR,(440,458),(600,458))
                        pygame.draw.line(display_surface,BLACK_COLOR,(0,493),(600,493),2)
                        pygame.draw.line(display_surface,BLACK_COLOR,(440,0),(440,493),2)
                        pygame.draw.line(display_surface,BLACK_COLOR,(0,593),(600,593),2)

                    result, server = self.user_socket.recvfrom(1024)


            if self.bot and continue_game:
                display_surface.blit(board_img, (0, 0))
                self.update_pieces_display(board, images, display_surface)
                pygame.display.update()

                # Lógica del bot
                bot_node = Node(board_implementation)
                movement_rep = bot_node.MCTS()
                previous_board = copy.deepcopy(board_implementation)
                new_board = previous_board.perform_movement(movement_rep)
                performed_movements.append(movement_rep)

                self.user_socket.sendto((REPLY_CORRECT_MOVE + \
                    movement_rep).encode(),server_end)

                result_move, server = self.user_socket.recvfrom(1024)

                if result_move.decode() == REPLY_TIE:
                    result_move, server = self.user_socket.recvfrom(1024)

                if movement_counter < 26:
                    if movement_counter % 2 == 0:
                        movement_strings[movement_counter] = \
                            str(int((movement_counter/2)+1)) \
                            + '.  ' + movement_rep
                    else:
                        movement_strings[movement_counter] = '    ' + \
                            movement_rep
                    movement_counter += 1
                else:
                    for i in range(25):
                        movement_strings[i] = movement_strings[i+1]

                    if post_movement_counter % 2 == 0:
                        movement_strings[25] = \
                            str(int(((movement_counter + \
                            post_movement_counter)/2)+1)) \
                            + '.  ' + movement_rep
                    else:
                        movement_strings[25] = '    ' + movement_rep

                    post_movement_counter += 1

                if current_turn == WHITE_PIECE:
                    current_turn_string = BLACK_TURN_STRING
                    current_turn_color = BLACK_COLOR
                    current_turn = BLACK_PIECE
                else:
                    current_turn_string = RED_TURN_STRING
                    current_turn_color = RED_COLOR
                    current_turn = WHITE_PIECE

                if self.user_color == WHITE_PIECE:
                    state_string = 'Waiting for black move...'
                else:
                    state_string = 'Waiting for red move...'

                new_fen = new_board.get_representation()
                split_fen = new_fen.split()
                board = split_fen[0].split('/')
                board_implementation.build(new_fen)

                needs_to_wait = True


            if continue_game:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN and not self.bot:
                        mouse_presses = pygame.mouse.get_pressed()

                        if mouse_presses[0]:
                            position = pygame.mouse.get_pos()
                            actual_x = (position[0] - 3)/HORIZONTAL_FACTOR + HORIZONTAL_DEVIATION
                            actual_y = position[1]/VERTICAL_FACTOR + VERTICAL_DEVIATION

                            column = int(actual_x)
                            row = int(actual_y)

                            center = column*HORIZONTAL_FACTOR+20, row*VERTICAL_FACTOR+20

                            if position[0] <= WIDTH-160 and \
                                position[1] <= HEIGHT and \
                                position[0] >= center[0]-HITBOX_MARGIN and \
                                position[0] <= center[0]+HITBOX_MARGIN and \
                                position[1] >= center[1]-HITBOX_MARGIN and \
                                position[1] <= center[1]+HITBOX_MARGIN:
                                clicked_position = (row,column)
                                clicked_piece = self.detect_piece_click(board_implementation,
                                    clicked_position)

                                if clicked_piece is not None and \
                                    clicked_piece.color == current_turn and \
                                    clicked_piece.color == self.user_color:
                                    selected_piece = clicked_piece

                                if clicked_position in highlighted_positions and \
                                    not is_finished:
                                    previous_board = copy.deepcopy(board)
                                    new_board, movement_rep = selected_piece.perform_movement \
                                        (board_implementation, clicked_position)
                                    performed_movements.append(movement_rep)

                                    selected_piece = None
                                    highlighted_positions.clear()

                                    self.user_socket.sendto((REPLY_CORRECT_MOVE + \
                                        movement_rep).encode(),server_end)

                                    result_move, server = self.user_socket.recvfrom(1024)

                                    if result_move.decode() == REPLY_TIE:
                                        result_move, server = self.user_socket.recvfrom(1024)

                                    if result_move != ILLEGAL_MOVE:
                                        #Lógica para imprimir los movimientos
                                        if movement_counter < 26:
                                            if movement_counter % 2 == 0:
                                                movement_strings[movement_counter] = \
                                                    str(int((movement_counter/2)+1)) \
                                                    + '.  ' + movement_rep
                                            else:
                                                movement_strings[movement_counter] = '    ' + \
                                                    movement_rep
                                            movement_counter += 1
                                        else:
                                            for i in range(25):
                                                movement_strings[i] = movement_strings[i+1]

                                            if post_movement_counter % 2 == 0:
                                                movement_strings[25] = \
                                                    str(int(((movement_counter + \
                                                    post_movement_counter)/2)+1)) \
                                                    + '.  ' + movement_rep
                                            else:
                                                movement_strings[25] = '    ' + movement_rep

                                            post_movement_counter += 1

                                        if current_turn == WHITE_PIECE:
                                            current_turn_string = BLACK_TURN_STRING
                                            current_turn_color = BLACK_COLOR
                                            current_turn = BLACK_PIECE
                                        else:
                                            current_turn_string = RED_TURN_STRING
                                            current_turn_color = RED_COLOR
                                            current_turn = WHITE_PIECE

                                        if self.user_color == WHITE_PIECE:
                                            state_string = 'Waiting for black move...'
                                        else:
                                            state_string = 'Waiting for red move...'

                                        new_board, server = self.user_socket.recvfrom(1024)

                                        if new_board.decode()[0:4] == MSG_GAME_FINISHED:
                                            if new_board.decode()[5:] == IDENTIFIER_TIE:
                                                if not self.vs_bot:
                                                    messagebox.showinfo(message="It's a tie.",
                                                        title="Finished game")
                                                is_finished = True
                                                if self.user_color == WHITE_COLOR:
                                                    current_turn_color = BLACK_COLOR
                                                else:
                                                    current_turn_color = WHITE_COLOR
                                                state_string = "It's a tie."
                                            elif new_board.decode()[4] == self.user_color:
                                                if not self.vs_bot:
                                                    messagebox.showinfo(message="You win!",
                                                        title="Finished game")
                                                is_finished = True
                                                if self.user_color == WHITE_COLOR:
                                                    current_turn_color = BLACK_COLOR
                                                else:
                                                    current_turn_color = WHITE_COLOR
                                                state_string = 'You win!'

                                                new_fen = new_board[5:].decode()
                                                split_fen = new_fen.split()
                                                board = split_fen[0].split('/')
                                                board_implementation.build(new_fen)
                                            else:
                                                if not self.vs_bot:
                                                    messagebox.showinfo(message="You lose...",
                                                        title="Finished game")
                                                is_finished = True
                                                if self.user_color == WHITE_COLOR:
                                                    current_turn_color = BLACK_COLOR
                                                else:
                                                    current_turn_color = WHITE_COLOR
                                                state_string = 'You lose...'
                                        elif new_board.decode()[0:4] == REPLY_TIE:
                                            if asked_tie:
                                                if self.user_color == WHITE_PIECE:
                                                    display_surface.blit(button_tie10, (180,513))
                                                else:
                                                    display_surface.blit(button_tie01, (180,513))
                                            else:
                                                if self.user_color == WHITE_PIECE:
                                                    display_surface.blit(button_tie01, (180,513))
                                                    rival_tie = True
                                                else:
                                                    display_surface.blit(button_tie10, (180,513))
                                                    rival_tie = True
                                            pygame.display.update()
                                            result, server = self.user_socket.recvfrom(1024)
                                        else:
                                            new_fen = new_board.decode()
                                            split_fen = new_fen.split()
                                            board = split_fen[0].split('/')
                                            board_implementation.build(new_fen)

                                            needs_to_wait = True
                                    else:
                                        board = previous_board

                            #Lógica del botón de rendirse
                            if position[0] >= BUTTON_HORIZONTAL_MARGIN and \
                                position[0] <= BUTTON_HORIZONTAL_MARGIN + BUTTON_WIDTH and \
                                position[1] >= BUTTON_VERTICAL_MARGIN and \
                                position[1] <= BUTTON_VERTICAL_MARGIN + BUTTON_HEIGHT:
                                if not is_finished:
                                    self.user_socket.sendto(REQUEST_DEFEAT.encode(),server_end)
                                    self.user_socket.recvfrom(1024)
                                    if not self.vs_bot:
                                        messagebox.showinfo(message="You lose...",
                                            title="Finished game")
                                    is_finished = True
                                    if self.user_color == WHITE_COLOR:
                                        current_turn_color = BLACK_COLOR
                                    else:
                                        current_turn_color = WHITE_COLOR
                                    state_string = 'You lose...'

                            #Lógica del botón de acordar tablas
                            if position[0] >= BUTTON_HORIZONTAL_MARGIN * 2 + BUTTON_WIDTH and \
                                position[0] <= BUTTON_HORIZONTAL_MARGIN * 2 + BUTTON_WIDTH * 2 and \
                                position[1] >= BUTTON_VERTICAL_MARGIN and \
                                position[1] <= BUTTON_VERTICAL_MARGIN + BUTTON_HEIGHT:
                                if not is_finished and not asked_tie:
                                    self.user_socket.sendto(REQUEST_TIE.encode(),server_end)
                                    asked_tie = True
                                    result, server = self.user_socket.recvfrom(1024)

                                    if result.decode()[0:4] == REPLY_TIE:
                                        result, server = self.user_socket.recvfrom(1024)
                                    else:
                                        if not self.vs_bot:
                                            messagebox.showinfo(message="It's a tie.",
                                                title="Finished game")
                                        is_finished = True
                                        if self.user_color == WHITE_COLOR:
                                            current_turn_color = BLACK_COLOR
                                        else:
                                            current_turn_color = WHITE_COLOR
                                        state_string = "It's a tie."

                            #Lógica del botón de imprimir movimientos
                            if position[0] >= BUTTON_HORIZONTAL_MARGIN * 3 + BUTTON_WIDTH * 2 and \
                                position[0] <= BUTTON_HORIZONTAL_MARGIN * 3 + BUTTON_WIDTH * 3 and \
                                position[1] >= BUTTON_VERTICAL_MARGIN and \
                                position[1] <= BUTTON_VERTICAL_MARGIN + BUTTON_HEIGHT:
                                if not self.vs_bot:
                                    movement_window = movement_ui(performed_movements)
                                    movement_window.run()

                            #Lógica del botón de salir al menú
                            if position[0] >= BUTTON_HORIZONTAL_MARGIN * 4 + BUTTON_WIDTH * 3 and \
                                position[0] <= BUTTON_HORIZONTAL_MARGIN * 4 + BUTTON_WIDTH * 4 and \
                                position[1] >= BUTTON_VERTICAL_MARGIN and \
                                position[1] <= BUTTON_VERTICAL_MARGIN + BUTTON_HEIGHT:
                                if is_finished:
                                    pygame.quit()
                                    continue_game = False
                                else:
                                    if not self.vs_bot:
                                        messagebox.showinfo(message="You can't exit during \
                                            the match!", title="Unable to exit")

                    if event.type == QUIT:
                        if self.bot:
                            pygame.quit()
                            continue_game = False

                        if not self.vs_bot:
                            if is_finished:
                                pygame.quit()
                                continue_game = False
                            else:
                                messagebox.showinfo(message="You can't exit during the match!",
                                    title="Unable to exit")
                        elif self.vs_bot and is_finished:
                            pygame.quit()
                            continue_game = False


    def print_possible_movement(self, position_img, display_surface, highlighted_positions):
        '''Muestra un movimiento posible, en forma de imagen'''

        possible_movement_img = pygame.image.load(r'imagenes/pm.png')
        display_surface.blit(possible_movement_img,
            (0.5 + position_img[1]*HORIZONTAL_FACTOR,
            position_img[0]*VERTICAL_FACTOR - 2.5))
        highlighted_positions.add((position_img[0],position_img[1]))


    def detect_piece_click(self, board_pie, position_pie):
        '''Devuelve la pieza encontrada en la posición dada'''

        detected_piece = None
        pieces = board_pie.board[WHITE_PIECE] + board_pie.board[BLACK_PIECE]
        for piece in pieces:
            if piece.position == position_pie:
                detected_piece = piece
                break
        return detected_piece


    def update_pieces_display(self, board, images, display_surface):
        '''Actualiza las piezas mostradas gráficamente'''

        j = 0
        for row in board:
            i = 0
            for char in row:
                if char.isnumeric():
                    i += int(char)
                elif char.isalpha():
                    display_surface.blit(images[char], (3 + i*HORIZONTAL_FACTOR,
                        j*VERTICAL_FACTOR))
                    i += 1
            j += 1


class movement_ui(object):
    '''Clase dedicada a la ventana para mostrar la lista de movimientos'''

    def __init__(self, movement_list):
        self.movement_list = movement_list

    def run(self):
        '''Crea la ventana de movimientos'''

        msg = ''

        if len(self.movement_list) > 0:
            for i in range(len(self.movement_list)):
                if i % 2 == 0:
                    msg += str(int(i/2)+1) + '.   ' + self.movement_list[i] + '\n'
                else:
                    msg += '    ' + self.movement_list[i] + '\n'

            messagebox.showinfo(message=msg, title="Movement list")
        else:
            messagebox.showinfo(message="No movements yet!", title="Movement list")
