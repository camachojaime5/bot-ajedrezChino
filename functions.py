import sys
import math
from piece import WHITE_PIECE


TIE_POSITION = 0
WHITE_WINNER_POSITION = 1
BLACK_WINNER_POSITION = 2

CONSTANT = 2 / math.sqrt(2)


def function1(record, n_parent, n, color):
    ''' (2*wins  - 4 * losses + ties) / n + 2 * Cp * sqrt(ln(n_parent) / n) '''
    if color == WHITE_PIECE:
        return ((2 * record[WHITE_WINNER_POSITION] - 4 * record[BLACK_WINNER_POSITION] + record[TIE_POSITION]) / n) \
                + CONSTANT * math.sqrt(math.log(n_parent) / n)
    return ((2 * record[BLACK_WINNER_POSITION] - 4 * record[WHITE_WINNER_POSITION] + record[TIE_POSITION]) / n) \
                + CONSTANT * math.sqrt(math.log(n_parent) / n)

def function2(record, n_parent, n, color):
    ''' (e^(wins/total) + 2 * Cp * sqrt(ln(n_parent) / n) '''
    if color == WHITE_PIECE:
        try:
            return ((math.e ** record[WHITE_WINNER_POSITION]) / n) \
                + CONSTANT * math.sqrt(math.log(n_parent) / n)
        except:
            return sys.float_info.max
    try:
        return ((math.e ** record[BLACK_WINNER_POSITION]) / n) \
                + CONSTANT * math.sqrt(math.log(n_parent) / n)
    except:
        return sys.float_info.max

def function3(record, n_parent, n, color):
    ''' wins / n + 2 * Cp * sqrt(ln(n_parent) / n) '''
    if color == WHITE_PIECE:
        return ((record[WHITE_WINNER_POSITION]) / n) \
                + CONSTANT * math.sqrt(math.log(n_parent) / n)
    return ((record[BLACK_WINNER_POSITION] / n)) \
                + CONSTANT * math.sqrt(math.log(n_parent) / n)

def function4(record, n_parent, n, color):
    ''' 4*wins / n + 2 * Cp * sqrt(ln(n_parent) / n) '''
    if color == WHITE_PIECE:
        return ((4 * record[WHITE_WINNER_POSITION]) / n) \
                + CONSTANT * math.sqrt(math.log(n_parent) / n)
    return ((4 * record[BLACK_WINNER_POSITION] / n)) \
                + CONSTANT * math.sqrt(math.log(n_parent) / n)

def function5(record, n_parent, n, color):
    ''' GREEDY 1: wins / n '''
    if color == WHITE_PIECE:
        return record[WHITE_WINNER_POSITION] / n
    return record[BLACK_WINNER_POSITION] / n

def function6(record, n_parent, n, color):
    ''' (e^(wins/total) '''
    if color == WHITE_PIECE:
        try:
            return ((math.e ** record[WHITE_WINNER_POSITION]) / n)
        except:
            return sys.float_info.max
    try:
        return ((math.e ** record[BLACK_WINNER_POSITION]) / n)
    except:
        return sys.float_info.max

