''' Implementation of the chinese chess board '''

import json
import piece
import random
import copy     # Add Jaime
from movement_converter import movement_converter


NUM_FEN_FEATURES = 6
FEN_ROW_SEPARATOR = '/'
UNUSED_FEN_ATTRIBUTE = '-'
MIN_ROW = 0
MAX_ROW = 9
MIN_COLUMN = 0
MAX_COLUMN = 8


def is_a_group2_representation(state):
    try:
        state['jaque']
        return True
    except KeyError:
        return False


def get_state_from_json_group2(json_state):
    try:
        turn = int(json_state['turno'])
    except KeyError:
        raise RuntimeError('Invalid game state')
    board = get_board_with_pieces_from_group2(json_state['tablero'])
    board.fullmove_counter = (turn) - 1
    board.halfmove_clock = 0
    if board.fullmove_counter % 2 == 0:
        board.side_to_move = piece.WHITE_PIECE
    else:
        board.side_to_move = piece.BLACK_PIECE
    return board.board, board.side_to_move, board.halfmove_clock, board.fullmove_counter


def get_board_with_pieces_from_group2(pieces):
    dict_board = {
        piece.WHITE_PIECE : [],
        piece.BLACK_PIECE : []
    }
    for board_piece in pieces:
        if board_piece['Color'] == 'Rojo':
            color = piece.WHITE_PIECE
        else:
            color = piece.BLACK_PIECE
        piece_type = board_piece['tipoPieza']
        if piece_type == 'Torre':
            dict_board[color].append(
                piece.Rook(color, (board_piece['Fila'], board_piece['Columna']))
            )
        elif piece_type == 'Peon':
            dict_board[color].append(
                piece.Pawn(color, (board_piece['Fila'], board_piece['Columna']))
            )
        elif piece_type == 'Guardia':
            dict_board[color].append(
                piece.Advisor(color, (board_piece['Fila'], board_piece['Columna']))
            )
        elif piece_type == 'Elefante':
            dict_board[color].append(
                piece.Elephant(color, (board_piece['Fila'], board_piece['Columna']))
            )
        elif piece_type == 'Caballo':
            dict_board[color].append(
                piece.Horse(color, (board_piece['Fila'], board_piece['Columna']))
            )
        elif piece_type == 'Emperador':
            dict_board[color].append(
                piece.King(color, (board_piece['Fila'], board_piece['Columna']))
            )
        elif piece_type == 'Canion':
            dict_board[color].append(
                piece.Cannon(color, (board_piece['Fila'], board_piece['Columna']))
            )
        else:
            raise RuntimeError('Invalid game state')
    board = Board()
    board.board = dict_board
    return board


def get_state_from_json(json_state):
    ''' Given a json string, returns the corresponding state '''

    try:
        fen_1 = json_state['Piece placement']
        fen_2 = json_state['Side to move']
        fen_3 = json_state['Castling ability']
        fen_4 = json_state['En passant target square']
        fen_5 = json_state['Halfmove clock']
        fen_6 = json_state['Fullmove counter']
    except KeyError:
        raise RuntimeError('Invalid FEN was given')

    return "%s %s %s %s %s %s" % (
            fen_1,
            fen_2,
            fen_3,
            fen_4,
            fen_5,
            fen_6
    )


def check_state_integrity(state):
    ''' Tests the integrity if a given board state '''

    result = True
    fen_features = state.split()
    if len(fen_features) != NUM_FEN_FEATURES:
        result = False
    elif fen_features[1] != piece.BLACK_PIECE and \
        fen_features[1] != piece.WHITE_PIECE:
        result = False
    else:
        try:
            int(fen_features[-2])
            int(fen_features[-1])
        except ValueError:
            result = False
    return result


def check_board_integrity(state):
    ''' Function that checks whether a board has valid information '''
    rows = state.split(FEN_ROW_SEPARATOR)
    if len(rows) != MAX_ROW + 1:
        return False
    for row in rows:
        count = 0
        for character in row:
            if character.isdigit():
                count += int(character)
            else:
                count += 1
        if count != MAX_COLUMN + 1:
            return False
    return True


def check_pieces_integrity(state):
    ''' Method to check whether we have the piece'''
    rows = state.split(FEN_ROW_SEPARATOR)
    piece_counter = {
        piece.ROOK_REPR : 0,
        piece.HORSE_REPR : 0,
        piece.ELEPHANT_REPR : 0,
        piece.CANNON_REPR : 0,
        piece.PAWN_REPR : 0,
        piece.ADVISOR_REPR : 0,
        piece.KING_REPR : 0,
        piece.ROOK_REPR.upper() : 0,
        piece.HORSE_REPR.upper() : 0,
        piece.ELEPHANT_REPR.upper() : 0,
        piece.CANNON_REPR.upper() : 0,
        piece.PAWN_REPR.upper() : 0,
        piece.ADVISOR_REPR.upper() : 0,
        piece.KING_REPR.upper() : 0,
    }
    for row in rows:
        for character in row:
            if character.lower() == piece.ROOK_REPR:
                piece_counter[character] += 1
            elif character.lower() == piece.HORSE_REPR:
                piece_counter[character] += 1
            elif character.lower() == piece.ELEPHANT_REPR:
                piece_counter[character] += 1
            elif character.lower() == piece.CANNON_REPR:
                piece_counter[character] += 1
            elif character.lower() == piece.PAWN_REPR:
                piece_counter[character] += 1
            elif character.lower() == piece.ADVISOR_REPR:
                piece_counter[character] += 1
            elif character.lower() == piece.KING_REPR:
                piece_counter[character] += 1
            elif character.isalpha():
                return False

    if piece_counter[piece.ROOK_REPR] > piece.NUM_ROOKS or \
       piece_counter[piece.HORSE_REPR] > piece.NUM_HORSES or \
       piece_counter[piece.ELEPHANT_REPR] > piece.NUM_ELEPHANTS or \
       piece_counter[piece.CANNON_REPR] > piece.NUM_CANNONS or \
       piece_counter[piece.PAWN_REPR] > piece.NUM_PAWNS or \
       piece_counter[piece.ADVISOR_REPR] > piece.NUM_ADVISORS or \
       piece_counter[piece.KING_REPR] > piece.NUM_KINGS or \
       piece_counter[piece.ROOK_REPR.upper()] > piece.NUM_ROOKS or \
       piece_counter[piece.HORSE_REPR.upper()] > piece.NUM_HORSES or \
       piece_counter[piece.ELEPHANT_REPR.upper()] > piece.NUM_ELEPHANTS or \
       piece_counter[piece.CANNON_REPR.upper()] > piece.NUM_CANNONS or \
       piece_counter[piece.PAWN_REPR.upper()] > piece.NUM_PAWNS or \
       piece_counter[piece.ADVISOR_REPR.upper()] > piece.NUM_ADVISORS or \
       piece_counter[piece.KING_REPR.upper()] > piece.NUM_KINGS:
        return False
    return True


def get_fen_from_list(list_board):
    ''' Returns the FEN string correspondant to a list '''

    num = 0
    list_result = []
    fen_str = ''

    for i in range(MAX_ROW + 1):
        list_board.insert(i * (MAX_ROW + 1), '/')

    for item in list_board:
        if type(item) == int:
            num += item
        else:
            if num != 0:
                list_result.append(num)
                num = 0
            list_result.append(item)

    if num != 0:
        list_result.append(num)

    list_result.pop(0) # Remove first '/' character

    for fen_char in list_result:
        fen_str = fen_str + str(fen_char)

    return fen_str


def get_colour_from_char(character):
    ''' Returns the color corresponding to a character '''
    if character.isupper():
        return piece.WHITE_PIECE
    else:
        return piece.BLACK_PIECE


class Board:
    ''' Board class implementation '''

    def __init__(self, state = None):
        ''' Constructor method '''
        self.board = {
            piece.WHITE_PIECE : [],
            piece.BLACK_PIECE : []
        }
        self.side_to_move = None
        self.halfmove_clock = 0
        self.fullmove_counter = 1
        if state:
            if is_a_group2_representation(state):
                params = get_state_from_json_group2(state)
                self.board = params[0]
                self.side_to_move = params[1]
                self.halfmove_clock = params[2]
                self.fullmove_counter = params[3]
            else:
                state = get_state_from_json(state)
                if not check_state_integrity(state):
                    raise RuntimeError("Invalid FEN was given")
                self.build(state)


    def build(self, state):
        ''' Method to build the board given the state '''
        self.board[piece.WHITE_PIECE].clear()
        self.board[piece.BLACK_PIECE].clear()
        board_info = state.split()
        self.side_to_move = board_info[1]
        self.halfmove_clock = board_info[-2]
        self.fullmove_counter = board_info[-1]
        state = board_info[0]
        if not check_board_integrity(state) or not check_pieces_integrity(state):
            raise RuntimeError("Invalid game state")
        rows = state.split(FEN_ROW_SEPARATOR)
        for i in range(len(rows)):
            fen_num_counter = 0
            for j in range(len(rows[i])):
                character = rows[i][j]
                if character.isalpha():
                    if character.lower() == piece.ROOK_REPR:
                        new_piece = piece.Rook(
                            get_colour_from_char(character),
                            position = (i, j + fen_num_counter)
                        )
                    if character.lower() == piece.HORSE_REPR:
                        new_piece = piece.Horse(
                            get_colour_from_char(character),
                            position = (i, j + fen_num_counter)
                        )
                    if character.lower() == piece.CANNON_REPR:
                        new_piece = piece.Cannon(
                            get_colour_from_char(character),
                            position = (i, j + fen_num_counter)
                        )
                    if character.lower() == piece.ELEPHANT_REPR:
                        new_piece = piece.Elephant(
                            get_colour_from_char(character),
                            position = (i, j + fen_num_counter)
                        )
                    if character.lower() == piece.PAWN_REPR:
                        new_piece = piece.Pawn(
                            get_colour_from_char(character),
                            position = (i, j + fen_num_counter)
                        )
                    if character.lower() == piece.ADVISOR_REPR:
                        new_piece = piece.Advisor(
                            get_colour_from_char(character),
                            position = (i, j + fen_num_counter)
                        )
                    if character.lower() == piece.KING_REPR:
                        new_piece = piece.King(
                            get_colour_from_char(character),
                            position = (i, j + fen_num_counter)
                        )
                    if new_piece.color == piece.BLACK_PIECE:
                        self.board[piece.BLACK_PIECE].append(new_piece)
                    else:
                        self.board[piece.WHITE_PIECE].append(new_piece)
                else:
                    fen_num_counter += int(character) - 1


    def get_piece_placement(self):
        ''' Method to get FEN attribute called <Piece Placement> '''
        list_board = [1,1,1,1,1,1,1,1,1] * (MAX_ROW + 1)
        list_pieces = self.board[piece.BLACK_PIECE] + self.board[piece.WHITE_PIECE]
        for board_piece in list_pieces:
            i, j = board_piece.position
            list_board[MAX_ROW * i + j] = board_piece.get_representation()

        return get_fen_from_list(list_board)

    def get_side_to_move(self):
        ''' Method to get FEN attribute called <Side to move> '''
        return self.side_to_move


    def get_castling_ability(self):
        ''' Method to get FEN attribute called <Castling ability> '''
        return UNUSED_FEN_ATTRIBUTE


    def get_en_passant_target_square(self):
        ''' Method to get FEN attribute called <En passant target square> '''
        return UNUSED_FEN_ATTRIBUTE


    def get_halfmove_clock(self):
        ''' Method to get FEN attribute called <Halfmove clock> '''
        return self.halfmove_clock


    def get_fullmove_counter(self):
        ''' Method to get FEN attribute called <Fullmove counter> '''
        return self.fullmove_counter


    def validar_movimiento(self, board2):
        '''Compara dos tableros para determinar si un movimiento es válido'''
        if int(board2.get_halfmove_clock()) <= 100 and int(self.get_fullmove_counter()) + 1 == \
            board2.get_fullmove_counter(): # Se comprueba movimiento 50 de P2 es legal
            first_changes_counter = 0
            second_changes_counter = 0

            first_changed_piece = None
            second_changed_piece = None
            extra_changed_piece = None

            is_another = False

            new_pieces = board2.board[piece.WHITE_PIECE] + board2.board[piece.BLACK_PIECE]
            old_pieces = self.board[piece.WHITE_PIECE] + self.board[piece.BLACK_PIECE]

            for current_piece in old_pieces:
                if current_piece not in new_pieces:
                    if not is_another:
                        first_changes_counter += 1
                        first_changed_piece = current_piece
                        is_another = True
                    else:
                        extra_changed_piece = current_piece

            for current_piece in new_pieces:
                if current_piece not in old_pieces:
                    second_changes_counter += 1
                    second_changed_piece = current_piece

            if (second_changed_piece.position in \
                first_changed_piece.get_possible_movements(self) or \
                second_changed_piece.position in \
                extra_changed_piece.get_possible_movements(self)) and \
                (first_changes_counter != 1 or second_changes_counter != 2) and \
                ((len(new_pieces) == len(old_pieces) + 1) or \
                (len(old_pieces) == len(new_pieces) + 1)):
                return True
            elif second_changed_piece.position in \
                first_changed_piece.get_possible_movements(self) and \
                first_changes_counter == 1 and second_changes_counter == 1:
                return True

        return False


    def board_difference(self, new_board, color):
        '''Given a new board, finds the piece that has moved, and where
        and represents it'''

        new_pieces = new_board.board[color]
        old_pieces = self.board[color]

        first_changed_piece = None
        second_changed_piece = None

        for current_piece in old_pieces:
            if current_piece not in new_pieces:
                first_changed_piece = current_piece

        for current_piece in new_pieces:
            if current_piece not in old_pieces:
                second_changed_piece = current_piece

        return first_changed_piece.get_movement_representation(self,
            second_changed_piece.position)


    def get_representation(self):
        ''' Method to get string FEN representation of the board '''
        return "%s %s %s %s %s %s" % (
            self.get_piece_placement(),
            self.get_side_to_move(),
            self.get_castling_ability(),
            self.get_en_passant_target_square(),
            self.get_halfmove_clock(),
            self.get_fullmove_counter()
        )


    def get_json(self):
        ''' Method to get the json code of the board '''
        return json.dumps(
            {
                'Piece placement' : self.get_piece_placement(),
                'Side to move' : self.get_side_to_move(),
                'Castling ability' : self.get_castling_ability(),
                'En passant target square' : self.get_en_passant_target_square(),
                'Halfmove clock' : self.get_halfmove_clock(),
                'Fullmove counter' : self.get_fullmove_counter()
            }
        )


    def perform_movement(self, movement_rep):
        '''Given a movement representation, returns a new board with the movement performed'''
        copy_board = copy.deepcopy(self)

        desired_piece, desired_position = movement_converter(copy_board, movement_rep,
            self.get_side_to_move())

        pieces = copy_board.board[piece.WHITE_PIECE] + copy_board.board[piece.BLACK_PIECE]
        for current_piece in pieces:
            if current_piece == desired_piece:
                current_piece.position = desired_position

        my_pieces = copy_board.board[self.get_side_to_move()]

        if self.get_side_to_move() == piece.WHITE_PIECE:
            rival_color = piece.BLACK_PIECE
        else:
            rival_color = piece.WHITE_PIECE

        rival_pieces = copy_board.board[rival_color]

        for my_piece in my_pieces:
            for rival_piece in rival_pieces:
                if my_piece.position == rival_piece.position:
                    copy_board.board[rival_piece.color].remove(rival_piece)

        copy_board.fullmove_counter = int(copy_board.fullmove_counter) + 1

        if copy_board.get_side_to_move() == piece.WHITE_PIECE:
            copy_board.side_to_move = piece.BLACK_PIECE
        else:
            copy_board.side_to_move = piece.WHITE_PIECE

        return copy_board


    def is_goal(self):
        '''Returns the color of the player that wins, or None if a tie'''
        board_rep = self.get_representation()
        black_king = False
        white_king = False

        if piece.KING_REPR in board_rep:
            black_king = True

        if piece.KING_REPR.upper() in board_rep:
            white_king = True

        if black_king and not white_king:
            return piece.BLACK_PIECE
        elif white_king and not black_king:
            return piece.WHITE_PIECE

        return None


    def get_succesors(self):
        '''Returns the successors of a board'''
        successors = []
        pieces = self.board[self.get_side_to_move()]

        for current_piece in pieces:
            positions = current_piece.get_possible_movements(self)

            for pos in positions:
                successors.append(current_piece.get_movement_representation(self, pos))

        return successors
