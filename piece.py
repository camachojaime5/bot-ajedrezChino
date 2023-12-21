'''Class designed for pieces implementation'''


import copy


BLACK_PIECE = "b"
WHITE_PIECE = "w"


NUM_ROOKS = 2
NUM_HORSES = 2
NUM_ELEPHANTS = 2
NUM_CANNONS = 2
NUM_PAWNS = 5
NUM_ADVISORS = 2
NUM_KINGS = 1


ROOK_REPR = 'r'
HORSE_REPR = 'h'
ELEPHANT_REPR = 'e'
CANNON_REPR = 'c'
PAWN_REPR = 'p'
ADVISOR_REPR = 'a'
KING_REPR = 'k'


FORWARDS_MOVEMENT = '+'
BACKWARDS_MOVEMENT = '-'
LATERAL_MOVEMENT = '='


class Piece(object):
    '''Generic class for pieces'''

    def __init__(self, color, position):
        ''' Constructor method for the piece class '''
        self.color = color
        self.position = position


    def __str__(self):
        ''' Piece String representation method '''
        return self.get_representation()


    def __eq__(self, new_piece):
        ''' Piece comparison method '''
        if self.position == new_piece.position and \
            self.color == new_piece.color and \
            type(self) == type(new_piece):
            return True
        else:
            return False


    def __ne__(self, new_piece):
        ''' Piece different comparison method '''
        return not self == new_piece


    def get_representation(self):
        '''Generic getter method for piece representation'''


    def get_possible_movements(self, board):
        '''Generic getter method for possible piece movements'''


    def remove_generic_incorrect_movements(self, movements, board):
        '''Removes impossible movements given a list of them and the board'''
        new_movements = []
        for mov in movements:
            if mov[0] >= 0 and mov[0] <= 9 and mov[1] >= 0 and mov[1] <= 8 and \
                mov != self.position:
                new_movements.append(mov)
        movements = new_movements

        pieces = board.board[self.color]
        for piece in pieces:
            if piece.position in movements:
                movements.remove(piece.position)
        return movements


    def is_in_enemy_side(self, position=None):
        ''' Method to check if the piece is in the enemy side or not '''
        if position:
            if self.color == WHITE_PIECE:
                if position[0] >= 0 and position[0] <= 4:
                    return True
                else:
                    return False
            else:
                if position[0] >= 5 and position[0] <= 9:
                    return True
                else:
                    return False
        else:
            if self.color == WHITE_PIECE:
                if self.position[0] >= 0 and self.position[0] <= 4:
                    return True
                else:
                    return False
            else:
                if self.position[0] >= 5 and self.position[0] <= 9:
                    return True
                else:
                    return False


    def is_in_self_side(self):
        ''' Method to check if the piece is in its own side or not '''
        return not self.is_in_enemy_side()


    def get_movement_representation(self, board, position):
        ''' Method to represent the movement of a piece '''
        # 1st field of movement string
        piece_moved = self.get_representation().upper()
        # 2nd field of movement string
        if self.color == WHITE_PIECE:
            column_moved = 9 -  self.position[1]
        else:
            column_moved = self.position[1] + 1
        # 3rd field of movement string
        if self.color == WHITE_PIECE:
            if self.position[0] > position[0]:
                type_movement = FORWARDS_MOVEMENT
            elif self.position[0] < position[0]:
                type_movement = BACKWARDS_MOVEMENT
            else:
                type_movement = LATERAL_MOVEMENT
        else:
            if self.position[0] < position[0]:
                type_movement = FORWARDS_MOVEMENT
            elif self.position[0] > position[0]:
                type_movement = BACKWARDS_MOVEMENT
            else:
                type_movement = LATERAL_MOVEMENT
        # 4th field of movement string
        if str(piece_moved).lower() in [ELEPHANT_REPR, ADVISOR_REPR, HORSE_REPR] \
            or type_movement == LATERAL_MOVEMENT:
            if self.color == BLACK_PIECE:
                new_pos = position[1] + 1
            else:
                new_pos = 9 - position[1]
        else:
            new_pos = abs(self.position[0] - position[0])

        tandem, tandem_pos = self.check_tandem(
            board
        )

        piece_moved, column_moved = self.represent_tandem(
            tandem,
            tandem_pos,
            piece_moved,
            column_moved
        )

        piece_moved = self.check_different_column_pawn_tandem(board, piece_moved, tandem)

        return '%s %s %s %s' % (
            piece_moved,
            column_moved,
            type_movement,
            new_pos
        )


    def check_tandem(self, board):
        ''' Method to check for tandem movements '''
        tandem = 1 # Initially only 1 piece
        tandem_pos = 0
        for new_piece in board.board[self.color]:
            if new_piece != self and type(new_piece) == type(self) \
                and new_piece.position[1] == self.position[1]:
                tandem += 1
                if self.color == WHITE_PIECE:
                    if self.position[0] < new_piece.position[0]:
                        tandem_pos += 1
                else:
                    if self.position[0] > new_piece.position[0]:
                        tandem_pos += 1
            if tandem > 1 and type(self) != Pawn:
                break
        return (tandem, tandem_pos)


    def represent_tandem(self, tandem, tandem_pos, piece_moved, column_moved):
        if tandem == 2:
            if tandem_pos == 0:
                column_moved = BACKWARDS_MOVEMENT
            else:
                column_moved = FORWARDS_MOVEMENT
        elif tandem == 3:
            if tandem_pos == 0:
                column_moved = BACKWARDS_MOVEMENT
            elif tandem_pos == 2:
                column_moved = FORWARDS_MOVEMENT
        elif tandem == 4:
            if tandem_pos == 0:
                column_moved = BACKWARDS_MOVEMENT
                piece_moved = BACKWARDS_MOVEMENT
            elif tandem_pos == 1:
                column_moved = BACKWARDS_MOVEMENT
            elif tandem_pos == 2:
                column_moved = FORWARDS_MOVEMENT
            elif tandem_pos == 3:
                column_moved = FORWARDS_MOVEMENT
                piece_moved = FORWARDS_MOVEMENT
        elif tandem == 5:
            if tandem_pos == 0:
                column_moved = BACKWARDS_MOVEMENT
                piece_moved = BACKWARDS_MOVEMENT
            elif tandem_pos == 1:
                column_moved = BACKWARDS_MOVEMENT
            elif tandem_pos == 3:
                column_moved = FORWARDS_MOVEMENT
            elif tandem_pos == 4:
                column_moved = FORWARDS_MOVEMENT
                piece_moved = FORWARDS_MOVEMENT
        return (piece_moved, column_moved)


    def remove_out_of_palace_movements(self, movements):
        new_movements = []

        for movement in movements:
            if self.color == BLACK_PIECE:
                if movement[0] >= 0 and movement[0] <= 2 and \
                    movement[1] >= 3 and movement[1] <= 5:
                    new_movements.append(movement)
            else:
                if movement[0] >= 7 and movement[0] <= 9 and \
                    movement[1] >= 3 and movement[1] <= 5:
                    new_movements.append(movement) 

        return new_movements


    def front_piece(self, movements, board):
        accountant = 0
        in_Front = False
        pieces = board.board[WHITE_PIECE] + board.board[BLACK_PIECE]
        king_pos_B0 = 0
        king_pos_B1 = 4
        king_pos_W0 = 9
        king_pos_W1 = 4
        for new_piece in pieces:
            if new_piece.get_representation() == 'K':
                king_pos_W0 = new_piece.position[0]
                king_pos_W1 = new_piece.position[1]
            if new_piece.get_representation() == 'k':
                king_pos_B0 = new_piece.position[0]
                king_pos_B1 = new_piece.position[1]

        for new_piece in pieces:
            if self.position[1] == king_pos_B1 and self.position[1] == king_pos_W1:

                if new_piece.position[1] == king_pos_W1 and new_piece.position[1] == king_pos_B1:
                    if new_piece.get_representation() != 'k' and \
                        new_piece.get_representation() != 'K':
                        if new_piece.position[0] > king_pos_B0 and \
                            new_piece.position[0] < king_pos_W0:
                            in_Front = True
                            accountant += 1
                        else:
                            in_Front = False

        copy_mov = copy.deepcopy(movements)
        if accountant == 1:
            for new_piece in pieces:
                if new_piece.position[1] == king_pos_W1 and \
                    new_piece.position[1] == king_pos_B1:
                    if new_piece.get_representation() != 'k' and \
                        new_piece.get_representation() != 'K':
                        if new_piece.position[0] > king_pos_B0 and \
                            new_piece.position[0] < king_pos_W0:
                            for mov in movements:
                                if mov[1] > new_piece.position[1] or mov[1] < new_piece.position[1]:
                                    copy_mov.remove(mov)
        return copy_mov


    def left_right3(self, movements, board):
        in_Front = False
        left_front_piece = False
        right_front_piece = False
        pieces = board.board[WHITE_PIECE] + board.board[BLACK_PIECE]
        for new_piece in pieces:
            if new_piece.get_representation() == 'K':
                king_pos_W0 = new_piece.position[0]
                king_pos_W1 = new_piece.position[1]
            if new_piece.get_representation() == 'k':
                king_pos_B0 = new_piece.position[0]
                king_pos_B1 = new_piece.position[1]
        if self.get_representation() == 'K':
            for new_piece in pieces:
                if new_piece.get_representation() == 'k':
                    if new_piece.position[1] - self.position[1] == -1:
                        for n_piece in pieces:
                            if n_piece.position[1] == new_piece.position[1] and \
                                (n_piece.position[0] > king_pos_B0 and \
                                    n_piece.position[0] < king_pos_W0):
                                left_front_piece = True
                                break
                        if not left_front_piece:
                            movements.remove((self.position[0], new_piece.position[1]))
                            break
                        else:
                            break

                    if new_piece.position[1] - self.position[1] == 1:
                        for n_piece in pieces:
                            if n_piece.position[1] == new_piece.position[1] and \
                                (n_piece.position[0] > king_pos_B0 and \
                                n_piece.position[0] < king_pos_W0):
                                right_front_piece = True
                                break
                        if not right_front_piece:
                            movements.remove((self.position[0], new_piece.position[1]))
                            break
                        else:
                            break

        if self.get_representation() == 'k':
            for new_piece in pieces:
                if new_piece.get_representation() == 'K':
                    if new_piece.position[1] - self.position[1] == -1:
                        for n_piece in pieces:
                            if n_piece.position[1] == new_piece.position[1] and \
                                (n_piece.position[0] > king_pos_B0 and \
                                n_piece.position[0] < king_pos_W0):
                                left_front_piece = True
                                break
                        if not left_front_piece:
                            movements.remove((self.position[0], new_piece.position[1]))
                            break
                        else:
                            break

                    if new_piece.position[1] - self.position[1] == 1:
                        for n_piece in pieces:
                            if n_piece.position[1] == new_piece.position[1] and \
                                (n_piece.position[0] > king_pos_B0 and \
                                n_piece.position[0] < king_pos_W0):
                                right_front_piece = True
                                break
                        if not right_front_piece:
                            movements.remove((self.position[0], new_piece.position[1]))
                            break
                        else:
                            break

        return movements


    def eaten_by(self, movements ,board):
        all_movements = []
        piece_in_front = True
        pieces = board.board[WHITE_PIECE] + board.board[BLACK_PIECE]
        all_movements.append(Rook.get_possible_movements(self, board))
        all_movements.append(Cannon.get_possible_movements(self, board))
        #allMovements.append(Horse.get_possible_movements(self, board))
        for movement in all_movements:
            for new_movement in movements:
                if movement == new_movement:
                    movements.remove(movement)
                break
        return movements


    def check_different_column_pawn_tandem(self, board, piece_moved, tandem):
        if type(self) != Pawn or tandem not in [2,3]:
            return piece_moved
        pawn_locations = {}

        for row in range(0, 10):
            pawn_locations[row] = 0

        for new_piece in board.board[self.color]:
            pawn_locations[new_piece.position[1]] += 1

        for row in range(0,10):
            if pawn_locations[row] in [2,3]:
                if self.color == BLACK_PIECE:
                    piece_moved = self.position[1] + 1
                else:
                    piece_moved = 9 - self.position[1]
        return piece_moved


    def perform_movement(self, board, position):
        '''Actually performs the movement of a piece'''
        movement = self.get_movement_representation(board, position)
        self.position = position

        if self.color == WHITE_PIECE:
            pieces = board.board[BLACK_PIECE]
            board.side_to_move = BLACK_PIECE
        else:
            pieces = board.board[WHITE_PIECE]
            board.side_to_move = WHITE_PIECE

        for piece in pieces:
            if piece.position == self.position:
                board.board[piece.color].remove(piece)

        board.fullmove_counter = int(board.fullmove_counter) + 1
        board.halfmove_counter = int(0) # NOT IMPLEMENTED

        return board, movement

    def get_four_limits(self, board):
        '''Returns the nearest pieces to a given one in the four directions'''
        left_limit = -1
        up_limit = -1
        down_limit = 10
        right_limit = 9

        pieces = board.board[WHITE_PIECE] + board.board[BLACK_PIECE]
        for piece in pieces:
            if piece.position[0] == self.position[0] and \
                piece.position[1] > left_limit and \
                piece.position[1] < self.position[1]:
                #Encuentra la pieza más cercana hacia la izquierda
                left_limit = piece.position[1]
            if piece.position[0] == self.position[0] and \
                piece.position[1] < right_limit and \
                piece.position[1] > self.position[1]:
                #Encuentra la pieza más cercana hacia la derecha
                right_limit = piece.position[1]
            if piece.position[1] == self.position[1] and \
                piece.position[0] > up_limit and \
                piece.position[0] < self.position[0]:
                #Encuentra la pieza más cercana hacia arriba
                up_limit = piece.position[0]
            if piece.position[1] == self.position[1] and \
                piece.position[0] < down_limit and \
                piece.position[0] > self.position[0]:
                #Encuentra la pieza más cercana hacia debajo
                down_limit = piece.position[0]

        return up_limit, right_limit, down_limit, left_limit


class Pawn(Piece):
    '''Class for pawn pieces'''

    def get_representation(self):
        '''Method for returning pawn representation'''
        if self.color == BLACK_PIECE:
            return PAWN_REPR

        return PAWN_REPR.upper()

    def get_possible_movements(self, board):
        orientation = 0
        if self.color == BLACK_PIECE:
            orientation = +1
        else:
            orientation = -1

        movements = [(self.position[0] + orientation, self.position[1])]

        if self.is_in_enemy_side():
            movements.append((self.position[0], self.position[1] - 1))
            movements.append((self.position[0], self.position[1] + 1))
        movements = self.front_piece(movements, board)
        movements = self.remove_generic_incorrect_movements(movements, board)

        return movements

class Rook(Piece):
    '''Class for rook pieces'''

    def get_possible_movements(self, board):
        movements = []
        limits = self.get_four_limits(board)

        for i in range(limits[3], limits[1]+1):
            movements.append((self.position[0],i))

        for i in range(limits[0], limits[2]+1):
            movements.append((i, self.position[1]))
        movements = self.front_piece(movements, board)
        return self.remove_generic_incorrect_movements(movements, board)


    def get_representation(self):
        '''Method for returning rook representation'''
        if self.color == BLACK_PIECE:
            return ROOK_REPR

        return ROOK_REPR.upper()


class Horse(Piece):
    '''Class for horse pieces'''

    def get_representation(self):
        '''Method for returning horse representation'''
        if self.color == BLACK_PIECE:
            return HORSE_REPR

        return HORSE_REPR.upper()

    def get_possible_movements(self, board):
        '''Method for returning horse possible movements'''
        movements = []

        movements.append((self.position[0]-2, self.position[1]-1))
        movements.append((self.position[0]-2, self.position[1]+1))
        movements.append((self.position[0]-1, self.position[1]-2))
        movements.append((self.position[0]-1, self.position[1]+2))
        movements.append((self.position[0]+1, self.position[1]-2))
        movements.append((self.position[0]+1, self.position[1]+2))
        movements.append((self.position[0]+2, self.position[1]-1))
        movements.append((self.position[0]+2, self.position[1]+1))

        movements = self.remove_horse_incorrect_movements(movements, board)
        movements = self.front_piece(movements, board)
        return self.remove_generic_incorrect_movements(movements, board)

    def remove_horse_incorrect_movements(self, movements, board):
        '''Removes positions where horse is unable to jump due to the presence
        of an obstacle'''
        possible_obstacles = board.board[WHITE_PIECE] + board.board[BLACK_PIECE]
        for current_obstacle in possible_obstacles:
            if current_obstacle.position == (self.position[0]-1,self.position[1]):
                if (self.position[0]-2,self.position[1]-1) in movements:
                    movements.remove((self.position[0]-2,self.position[1]-1))
                if (self.position[0]-2,self.position[1]+1) in movements:
                    movements.remove((self.position[0]-2,self.position[1]+1))
            elif current_obstacle.position == (self.position[0]+1,self.position[1]):
                if (self.position[0]+2,self.position[1]-1) in movements:
                    movements.remove((self.position[0]+2,self.position[1]-1))
                if (self.position[0]+2,self.position[1]+1) in movements:
                    movements.remove((self.position[0]+2,self.position[1]+1))
            elif current_obstacle.position == (self.position[0],self.position[1]-1):
                if (self.position[0]-1,self.position[1]-2) in movements:
                    movements.remove((self.position[0]-1,self.position[1]-2))
                if (self.position[0]+1,self.position[1]-2) in movements:
                    movements.remove((self.position[0]+1,self.position[1]-2))
            elif current_obstacle.position == (self.position[0],self.position[1]+1):
                if (self.position[0]-1,self.position[1]+2) in movements:
                    movements.remove((self.position[0]-1,self.position[1]+2))
                if (self.position[0]+1,self.position[1]+2) in movements:
                    movements.remove((self.position[0]+1,self.position[1]+2))
        return movements


class Elephant(Piece):
    '''Class for elephant pieces'''

    def get_representation(self):
        '''Method for returning elephant representation'''
        if self.color == BLACK_PIECE:
            return ELEPHANT_REPR

        return ELEPHANT_REPR.upper()

    def remove_enemy_river(self, movements):
        '''Removes positions where elephant is unable to jump due to the river'''
        for move in movements:
            if self.is_in_enemy_side(move):
                movements.remove(move)

        return movements

    def get_possible_movements(self, board):
        '''Method for returning elephant possible movements'''
        movements = []

        up = -2
        left = -2
        down = 2
        right = 2

        movements.append((self.position[0] + up, self.position[1] + left))
        movements.append((self.position[0] + down, self.position[1] + left))
        movements.append((self.position[0] + up, self.position[1] + right))
        movements.append((self.position[0] + down, self.position[1] + right))

        movements = self.remove_enemy_river(movements)
        movements = self.front_piece(movements, board)
        movements = self.remove_generic_incorrect_movements(movements, board)

        return movements


class Advisor(Piece):
    '''Class for advisor pieces'''

    def get_possible_movements(self, board):
        movements = []

        movements.append((self.position[0]+1, self.position[1]+1))
        movements.append((self.position[0]-1, self.position[1]+1))
        movements.append((self.position[0]-1, self.position[1]-1))
        movements.append((self.position[0]+1, self.position[1]-1))

        movements = self.remove_out_of_palace_movements(movements)
        movements = self.front_piece(movements, board)
        return self.remove_generic_incorrect_movements(movements, board)

    def get_representation(self):
        '''Method for returning advisor representation'''
        if self.color == BLACK_PIECE:
            return ADVISOR_REPR

        return ADVISOR_REPR.upper()


class Cannon(Piece):
    '''Class for cannon pieces'''

    def get_representation(self):
        '''Method for returning cannon representation'''
        if self.color == BLACK_PIECE:
            return CANNON_REPR

        return CANNON_REPR.upper()

    def get_possible_movements(self, board):
        '''Method for returning cannon possible movements'''
        movements = []
        limits = self.get_four_limits(board)

        #Añade todas las posiciones de la pieza a la izquierda
        if self.position[1] - limits[3] > 1 or \
            self.position[1] - limits[3] == 1 and limits[3] == 0:
            for i in range(limits[3]+1, self.position[1]):
                movements.append((self.position[0],i))

        #Añade todas las posiciones de la pieza a la derecha
        if limits[1] - self.position[1] > 1 or \
            limits[1] - self.position[1] == 1 and limits[1] == 8:
            for i in range(self.position[1], limits[1]):
                movements.append((self.position[0],i))

        #Añade todas las posiciones de la pieza hacia arriba si son piezas rojas
        #o hacia debajo si son piezas negras
        if self.color == WHITE_PIECE:
            if self.position[0] - limits[0] > 1 or \
                self.position[0] - limits[0] == 1 and limits[0] == 0:
                for i in range(limits[0]+1, self.position[0]):
                    movements.append((i,self.position[1]))
        else:
            if limits[2] - self.position[0] > 1 or \
                limits[2] - self.position[0] == 1 and limits[2] == 9:
                for i in range(self.position[0], limits[2]):
                    movements.append((i,self.position[1]))

        #Comprueban si hay alguna pieza que se pueda comer gracias a dar un salto
        next_up_limit = -1
        next_down_limit = 10
        next_left_limit = -1
        next_right_limit = 9

        pieces = board.board[WHITE_PIECE] + board.board[BLACK_PIECE]
        for piece in pieces:
            if piece.position[0] == self.position[0] and \
                piece.position[1] < limits[3] and \
                piece.position[1] > next_left_limit:
                next_left_limit = piece.position[1]
            if piece.position[0] == self.position[0] and \
                piece.position[1] > limits[1] and \
                piece.position[1] < next_right_limit:
                next_right_limit = piece.position[1]
            if piece.position[1] == self.position[1] and \
                piece.position[0] < limits[0] and \
                piece.position[0] > next_up_limit:
                next_up_limit = piece.position[0]
            if piece.position[1] == self.position[1] and \
                piece.position[0] > limits[2] and \
                piece.position[0] < next_down_limit:
                next_down_limit = piece.position[0]

        if next_up_limit != -1 and self.color == WHITE_PIECE:
            movements.append((next_up_limit,self.position[1]))
        if next_down_limit != 10 and self.color == BLACK_PIECE:
            movements.append((next_down_limit,self.position[1]))
        if next_left_limit != -1:
            movements.append((self.position[0],next_left_limit))
        if next_right_limit != 9:
            movements.append((self.position[0],next_right_limit))

        movements = self.front_piece(movements, board)
        return self.remove_generic_incorrect_movements(movements, board)


class King(Piece):
    '''Class for king pieces'''

    def get_possible_movements(self, board):
        '''Method for returning king possible movements'''
        movements = []
        movements.append((self.position[0] + 1, self.position[1]))
        movements.append((self.position[0], self.position[1] + 1))
        movements.append((self.position[0], self.position[1] - 1))
        movements.append((self.position[0] - 1, self.position[1]))

        movements = self.remove_out_of_palace_movements(movements)
        movements = self.left_right3(movements, board)
        return self.remove_generic_incorrect_movements(movements, board)

    def get_representation(self):
        '''Method for returning king representation'''
        if self.color == BLACK_PIECE:
            return KING_REPR

        return KING_REPR.upper()
