''' Node implementation for MonteCarlo Tree Search '''

import math
import random
import time
import json

from board import Board
from piece import BLACK_PIECE, WHITE_PIECE, KING_REPR
from functions import *

MONTECARLO_ITERATION_ESTIMATION = 200
CONFIDENCE_QUANTILE = 2.575
MAX_TIME = 15

class Node():
    ''' Class Node Implementation '''
    def __init__(self, board, parent = None):
        ''' Constructor method for Node class '''
        self.board = board
        self.parent = parent
        self.win_record = [0,0,0] # TIES, PLAYER1 WINS, PLAYER2 WINS
        self.unexplored_successors = board.get_succesors()
        self.explored_successors = {}
        self.times_visited = 0


    def __str__(self):
        return f'Win record: {self.win_record}, times visited: {self.times_visited}, Board: {self.board.get_representation()}, Parent: {self.parent is not None}'

    def is_terminal_node(self):
        ''' Method to get if the node is terminal (0 children) or not '''
        if len(self.board.get_succesors()) == 0:
            return True
        return False


    def calculate_node_uct(self, uct_function = function1):
        ''' Method that calculates uct value for the node '''
        if self.parent.board.side_to_move == WHITE_PIECE:
            return uct_function(self.win_record, self.parent.times_visited, self.times_visited, WHITE_PIECE)
        return uct_function(self.win_record, self.parent.times_visited, self.times_visited, BLACK_PIECE)


    def select_node(self):
        ''' Method that implements step 1 of MCTS: iterative implementation to improve efficiency '''
        selected_node = self
        while not selected_node.is_terminal_node() and len(selected_node.unexplored_successors) == 0:
            succesor_nodes = list(selected_node.explored_successors.values())
            max_uct_value = -9999
            max_uct_node = None
            for child_node in succesor_nodes:
                child_uct = child_node.calculate_node_uct()
                if child_uct > max_uct_value:
                    max_uct_node = child_node
                    max_uct_value = child_uct
            selected_node = max_uct_node

        return selected_node


    def expand_node(self):
        ''' Method that implements step 2 of MCTS: random choice to improve efficiency '''
        if self.is_terminal_node() or self.board.is_goal():
            return self
        movement =  random.choice(self.unexplored_successors)
        new_board = self.board.perform_movement(movement)
        new_node = Node(new_board, self)
        self.unexplored_successors.remove(movement)
        self.explored_successors[movement] = new_node
        return new_node 


    def simulation(self):
        ''' Method that implements step 3 of MCTS '''
        total_movements = 0

        current_board = Board(json.loads(self.board.get_json()))
        while total_movements < MONTECARLO_ITERATION_ESTIMATION and current_board.is_goal() is None:
            movement = random.choice(current_board.get_succesors())
            current_board = current_board.perform_movement(movement)
            total_movements += 1

        value = current_board.is_goal()
        if value is None:
            return TIE_POSITION, total_movements
        if value == WHITE_PIECE:
            return WHITE_WINNER_POSITION, total_movements
        return BLACK_WINNER_POSITION, total_movements


    def backpropagation(self, value):
        ''' Method that implements step 4 of MCTS '''
        current_node = self
        while current_node:
            current_node.win_record[value] += 1
            current_node.times_visited += 1
            current_node = current_node.parent


    def MCTS(self, uct_function = function1):
        ''' Method that implements MCTS '''
        time_left = MAX_TIME
        while time_left > 0:
            start_time = time.time()

            selected_node = self.select_node()
            new_node = selected_node.expand_node()
            value = new_node.simulation()[0]
            new_node.backpropagation(value)

            time_left -= time.time() - start_time

        best_movement = None
        best_value = -9999
        for movement, child_node in self.explored_successors.items():
            child_node_uct =  child_node.calculate_node_uct(uct_function)
            print(f'{movement}:{child_node}: {child_node_uct}')
            if child_node_uct > best_value:
                best_value = child_node_uct
                best_movement = movement
        print('BEST: ' + str(best_movement))
        print(self)
        print('----------')
        return best_movement


    @staticmethod
    def estimate_simulation_iterations(node, repetitions):
        ''' Method to estimate with 95% confidence interval the number of iterations '''
        values = []
        i, j = 0, 0
        mean, variance = 0, 0

        while i < repetitions:
            num_iterations = node.simulation()[1]
            values.append(num_iterations)
            mean = mean + num_iterations
            i = i + 1
            print('ITERATION ' + str(i) + ': ' + str(num_iterations))
        mean = mean / repetitions

        while j < repetitions:
            variance = variance + ((values[j] - mean) ** 2)
            j = j + 1
        variance = variance / repetitions

        delta_ci = CONFIDENCE_QUANTILE * math.sqrt(variance / repetitions)
        return mean, [(mean - delta_ci), (mean + delta_ci)]


    def random_selection(self):
        '''Method for random child selections'''
        return random.choice(self.board.get_succesors())
