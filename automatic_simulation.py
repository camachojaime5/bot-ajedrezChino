#!/usr/bin/python3
# -*- coding: utf-8; mode: python -*-


from test_botvsbot import TestBotVsBot
from piece import BLACK_PIECE


ITERATIONS = 30


current_wins = 0
current_losses = 0
current_turns = 0
current_iterations = 0


for i in range(ITERATIONS):
    test = TestBotVsBot()

    try:
        board, color = test.run()
    except Exception as e:
        print(e)
        print('ERROR. Saltando simulación...')
    else:
        print('--------------')
        print('TABLERO FINAL: ' + str(board))
        print('GANADOR: ' + str(color))

        if color == BLACK_PIECE:
            current_wins += 1
        else:
            current_losses += 1

        current_turns += int(board.split()[5])
        current_iterations += 1

        print('-------------------')
        print('FINAL DE ITERACIÓN ' + str(current_iterations))
        print('ITERACIONES: ' + str(current_iterations))
        print('TURNOS: ' + str(current_turns))
        print('TURNOS POR PARTIDA: ' + str(int(current_turns/current_iterations)))
        print('VICTORIAS: ' + str(current_wins))
        print('DERROTAS: ' + str(current_losses))
        print('-------------------')

print('TOTAL')
print('ITERACIONES: ' + str(current_iterations))
print('TURNOS: ' + str(current_turns))
print('TURNOS POR PARTIDA: ' + str(int(current_turns/ITERATIONS)))
print('VICTORIAS: ' + str(current_wins))
print('DERROTAS: ' + str(current_losses))
print('----------------------------------------------')
