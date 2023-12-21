''' Implementation of a converter for given movements '''


import piece


def movement_converter(board, movement, turn_color):
    '''Converts a given board, movement and turn into the referenced piece and the
    desired position'''
    split_movement = movement.split()
    desired_piece = None
    desired_position = None
    desired_pawn = None

    # Base case
    if split_movement[0].isalpha():
        if split_movement[1].isnumeric():
            pieces = board.board[turn_color]

            max_col, pawn_counter = get_max_pawn_col(board, turn_color)

            # Getting middle pawn in 5 pawn tandem
            if pawn_counter == 5:
                limit = -1

                if turn_color == piece.WHITE_PIECE:
                    destination_column = 8 - max_col
                else:
                    destination_column = max_col

                pieces = board.board[turn_color]
                for current_piece in pieces:
                    if current_piece.position[0] > limit and \
                        current_piece.get_representation().upper() == \
                        piece.PAWN_REPR.upper() and \
                        current_piece.position[1] == destination_column:
                        limit = current_piece.position[0]
                        desired_pawn = current_piece

                new_limit = -1

                for current_piece in pieces:
                    if current_piece.position[0] > new_limit and \
                        current_piece.get_representation().upper() == \
                        piece.PAWN_REPR.upper() and \
                        current_piece.position[1] == destination_column and \
                        current_piece.position[0] < limit:
                        new_limit = current_piece.position[0]
                        desired_pawn = current_piece

                final_limit = -1

                for current_piece in pieces:
                    if current_piece.position[0] > final_limit and \
                        current_piece.get_representation().upper() == \
                        piece.PAWN_REPR.upper() and \
                        current_piece.position[1] == destination_column and \
                        current_piece.position[0] < new_limit:
                        final_limit = current_piece.position[0]
                        desired_pawn = current_piece

            # Getting middle pawn in 3 pawn tandem
            if pawn_counter == 3:
                limit = -1

                if turn_color == piece.WHITE_PIECE:
                    destination_column = 8 - max_col
                else:
                    destination_column = max_col

                pieces = board.board[turn_color]
                for current_piece in pieces:
                    if current_piece.position[0] > limit and \
                        current_piece.get_representation().upper() == \
                        piece.PAWN_REPR.upper() and \
                        current_piece.position[1] == destination_column:
                        limit = current_piece.position[0]
                        desired_pawn = current_piece

                new_limit = -1

                for current_piece in pieces:
                    if current_piece.position[0] > new_limit and \
                        current_piece.get_representation().upper() == \
                        piece.PAWN_REPR.upper() and \
                        current_piece.position[1] == destination_column and \
                        current_piece.position[0] < limit:
                        new_limit = current_piece.position[0]
                        desired_pawn = current_piece

            for current_piece in pieces:
                # Column where we expect to find the piece
                if turn_color == piece.WHITE_PIECE:
                    current_column = 10 - int(split_movement[1]) - 1
                else:
                    current_column = int(split_movement[1]) - 1

                # Check of the current piece
                if current_piece.get_representation().upper() == split_movement[0] and \
                    current_piece.position[1] == current_column:
                    desired_piece = current_piece

                    # Row where the piece is
                    current_row = desired_piece.position[0]

                    # Column where the piece is expected to go
                    if turn_color == piece.WHITE_PIECE:
                        destination_column = 10 - int(split_movement[3]) - 1
                    else:
                        destination_column = int(split_movement[3]) - 1

                    # Middle 3 & 5 pawn tandem
                    if current_piece.get_representation().upper() == piece.PAWN_REPR.upper() and \
                        (pawn_counter == 5 or pawn_counter == 3) and \
                        split_movement[0] == piece.PAWN_REPR.upper():
                        # Middle white 3 & 5 pawn tandem
                        if turn_color == piece.WHITE_PIECE:
                            # Middle forwards white 3 & 5 pawn tandem
                            if split_movement[2] == piece.FORWARDS_MOVEMENT:
                                desired_position = (desired_pawn.position[0] - 1,
                                    desired_pawn.position[1])
                            # Middle sideways white 3 & 5 pawn tandem
                            else:
                                desired_position = (desired_pawn.position[0],
                                    10 - int(split_movement[3]) - 1)
                        # Middle black 3 & 5 pawn tandem
                        else:
                            # Middle forwards black 3 & 5 pawn tandem
                            if split_movement[2] == piece.FORWARDS_MOVEMENT:
                                desired_position = (desired_pawn.position[0] + 1,
                                    desired_pawn.position[1])
                            # Middle sideways black 3 & 5 pawn tandem
                            else:
                                desired_position = (desired_pawn.position[0],
                                    int(split_movement[3]) - 1)
                        desired_piece = desired_pawn
                    # Advisor case
                    elif current_piece.get_representation().upper() == \
                        piece.ADVISOR_REPR.upper() and \
                        split_movement[0] == piece.ADVISOR_REPR.upper():
                        if split_movement[2] == piece.FORWARDS_MOVEMENT:
                            if turn_color == piece.WHITE_PIECE:
                                # White forwards advisor
                                desired_position = (current_row - 1, destination_column)
                            else:
                                # Black forwards advisor
                                desired_position = (current_row + 1, destination_column)
                        else:
                            if turn_color == piece.WHITE_PIECE:
                                # White backwards advisor
                                desired_position = (current_row + 1, destination_column)
                            else:
                                # Black backwards advisor
                                desired_position = (current_row - 1, destination_column)
                    # Elephant case
                    elif current_piece.get_representation().upper() == \
                        piece.ELEPHANT_REPR.upper() and \
                        split_movement[0] == piece.ELEPHANT_REPR.upper():
                        if split_movement[2] == piece.FORWARDS_MOVEMENT:
                            if turn_color == piece.WHITE_PIECE:
                                # White forwards elephant
                                desired_position = (current_row - 2, destination_column)
                            else:
                                # Black forwards elephant
                                desired_position = (current_row + 2, destination_column)
                        else:
                            if turn_color == piece.WHITE_PIECE:
                                # White backwards elephant
                                desired_position = (current_row + 2, destination_column)
                            else:
                                # Black backwards elephant
                                desired_position = (current_row - 2, destination_column)
                    # Horse case
                    elif current_piece.get_representation().upper() == \
                        piece.HORSE_REPR.upper() and \
                        split_movement[0] == piece.HORSE_REPR.upper():
                        if split_movement[2] == piece.FORWARDS_MOVEMENT:
                            if turn_color == piece.WHITE_PIECE:
                                if int(split_movement[3]) == int(split_movement[1]) + 1 or \
                                    int(split_movement[3]) == int(split_movement[1]) - 1:
                                    # White vertical L forwards horse
                                    desired_position = (desired_piece.position[0] - 2, destination_column)
                                else:
                                    # White horizontal L forwards horse
                                    desired_position = (desired_piece.position[0] - 1, destination_column)
                            else:
                                if int(split_movement[3]) == int(split_movement[1]) + 1 or \
                                    int(split_movement[3]) == int(split_movement[1]) - 1:
                                    # Black vertical L forwards horse
                                    desired_position = (desired_piece.position[0] + 2, destination_column)
                                else:
                                    # Black horizontal L forwards horse
                                    desired_position = (desired_piece.position[0] + 1, destination_column)
                        else:
                            if turn_color == piece.WHITE_PIECE:
                                if int(split_movement[3]) == int(split_movement[1]) + 1 or \
                                    int(split_movement[3]) == int(split_movement[1]) - 1:
                                    # White vertical L backwards horse
                                    desired_position = (desired_piece.position[0] + 2, destination_column)
                                else:
                                    # White horizontal L backwards horse
                                    desired_position = (desired_piece.position[0] + 1, destination_column)
                            else:
                                if int(split_movement[3]) == int(split_movement[1]) + 1 or \
                                    int(split_movement[3]) == int(split_movement[1]) - 1:
                                    # Black vertical L backwards horse
                                    desired_position = (desired_piece.position[0] - 2, destination_column)
                                else:
                                    # Black horizontal L backwards horse
                                    desired_position = (desired_piece.position[0] - 1, destination_column)
                    # Generic case
                    elif split_movement[0] == piece.KING_REPR.upper() or \
                        split_movement[0] == piece.ROOK_REPR.upper() or \
                        split_movement[0] == piece.CANNON_REPR.upper() or \
                        (split_movement[0] == piece.PAWN_REPR.upper() and pawn_counter != 3) or \
                        (split_movement[0] == piece.PAWN_REPR.upper() and pawn_counter != 5):
                        if split_movement[2] == piece.FORWARDS_MOVEMENT:
                            if turn_color == piece.WHITE_PIECE:
                                # White forwards piece
                                desired_position = (current_row - int(split_movement[3]),
                                    current_column)
                            else:
                                # Black forwards piece
                                desired_position = (current_row + int(split_movement[3]),
                                    current_column)
                        elif split_movement[2] == piece.BACKWARDS_MOVEMENT:
                            if turn_color == piece.WHITE_PIECE:
                                # White backwards piece
                                desired_position = (current_row + int(split_movement[3]),
                                    current_column)
                            else:
                                # Black backwards piece
                                desired_position = (current_row - int(split_movement[3]),
                                    current_column)
                        # Sideways movement
                        else:
                            desired_position = (current_row, destination_column)
        else:
            # X + case
            if split_movement[1] == piece.FORWARDS_MOVEMENT:
                pieces = board.board[turn_color]
                current_row = 0
                chosen_pawn_white = 10
                chosen_pawn_black = 0

                max_col, pawn_counter = get_max_pawn_col(board, turn_color)

                # Getting middle front pawn in 4 & 5 pawn tandem
                if (pawn_counter == 4 or pawn_counter == 5) and turn_color == piece.WHITE_PIECE and \
                    split_movement[0].upper() == piece.PAWN_REPR.upper():
                    limit = 10
                    destination_column = 8 - max_col

                    pieces = board.board[turn_color]
                    for current_piece in pieces:
                        if current_piece.position[0] < limit and \
                            current_piece.get_representation().upper() == \
                            piece.PAWN_REPR.upper() and \
                            current_piece.position[1] == destination_column:
                            limit = current_piece.position[0]

                    new_limit = 10

                    for current_piece in pieces:
                        if current_piece.position[0] < new_limit and \
                            current_piece.get_representation().upper() == \
                            piece.PAWN_REPR.upper() and \
                            current_piece.position[1] == destination_column and \
                            current_piece.position[0] > limit:
                            new_limit = current_piece.position[0]
                            desired_pawn = current_piece
                elif (pawn_counter == 4 or pawn_counter == 5) and turn_color == piece.BLACK_PIECE and \
                    split_movement[0].upper() == piece.PAWN_REPR.upper():
                    limit = -1
                    destination_column = max_col

                    pieces = board.board[turn_color]
                    for current_piece in pieces:
                        if current_piece.position[0] > limit and \
                            current_piece.get_representation().upper() == \
                            piece.PAWN_REPR.upper() and \
                            current_piece.position[1] == destination_column:
                            limit = current_piece.position[0]

                    new_limit = -1

                    for current_piece in pieces:
                        if current_piece.position[0] > new_limit and \
                            current_piece.get_representation().upper() == \
                            piece.PAWN_REPR.upper() and \
                            current_piece.position[1] == destination_column and \
                            current_piece.position[0] < limit:
                            new_limit = current_piece.position[0]
                            desired_pawn = current_piece
                elif (pawn_counter == 2 or pawn_counter == 3) and turn_color == piece.WHITE_PIECE and \
                    split_movement[0].upper() == piece.PAWN_REPR.upper():
                    limit = 10
                    destination_column = 8 - max_col

                    pieces = board.board[turn_color]
                    for current_piece in pieces:
                        if current_piece.position[0] < limit and \
                            current_piece.get_representation().upper() == \
                            piece.PAWN_REPR.upper() and \
                            current_piece.position[1] == destination_column:
                            limit = current_piece.position[0]
                            desired_pawn = current_piece
                elif (pawn_counter == 2 or pawn_counter == 3) and turn_color == piece.BLACK_PIECE and \
                    split_movement[0].upper() == piece.PAWN_REPR.upper():
                    limit = -1
                    destination_column = max_col

                    pieces = board.board[turn_color]
                    for current_piece in pieces:
                        if current_piece.position[0] > limit and \
                            current_piece.get_representation().upper() == \
                            piece.PAWN_REPR.upper() and \
                            current_piece.position[1] == destination_column:
                            limit = current_piece.position[0]
                            desired_pawn = current_piece

                for current_piece in pieces:
                    if current_piece.get_representation().upper() == split_movement[0].upper():
                        current_column = current_piece.position[1]

                for current_piece in pieces:
                    # Column where the piece is expected to go
                    if turn_color == piece.WHITE_PIECE:
                        destination_column = 10 - int(split_movement[3]) - 1
                    else:
                        destination_column = int(split_movement[3]) - 1

                    if turn_color == piece.WHITE_PIECE:
                        if current_piece.get_representation().upper() == split_movement[0] and \
                            current_piece.position[1] == current_column and \
                            current_piece.position[0] < chosen_pawn_white:
                            desired_piece = current_piece
                            chosen_pawn_white = current_piece.position[0]
                            current_row = current_piece.position[0]
                    else:
                        if current_piece.get_representation().upper() == split_movement[0] and \
                            current_piece.position[1] == current_column and \
                            current_piece.position[0] > chosen_pawn_black:
                            desired_piece = current_piece
                            chosen_pawn_black = current_piece.position[0]
                            current_row = current_piece.position[0]

                    # Middle front 4 & 5 pawn tandem
                    if current_piece.get_representation().upper() == piece.PAWN_REPR.upper() and \
                        pawn_counter > 1 and \
                        split_movement[0] == piece.PAWN_REPR.upper():
                        # Middle front white 4 & 5 pawn tandem
                        if turn_color == piece.WHITE_PIECE:
                            # Middle front forwards white 4 & 5 pawn tandem
                            if split_movement[2] == piece.FORWARDS_MOVEMENT:
                                desired_position = (desired_pawn.position[0] - 1,
                                    desired_pawn.position[1])
                            # Middle front sideways white 4 & 5 pawn tandem
                            else:
                                desired_position = (desired_pawn.position[0],
                                    10 - int(split_movement[3]) - 1)
                        # Middle front black 4 & 5 pawn tandem
                        else:
                            # Middle front forwards black 4 & 5 pawn tandem
                            if split_movement[2] == piece.FORWARDS_MOVEMENT:
                                desired_position = (desired_pawn.position[0] + 1,
                                    desired_pawn.position[1])
                            # Middle front sideways black 4 & 5 pawn tandem
                            else:
                                desired_position = (desired_pawn.position[0],
                                    int(split_movement[3]) - 1)
                        desired_piece = desired_pawn
                    # Advisor case
                    elif current_piece.get_representation().upper() == \
                        piece.ADVISOR_REPR.upper() and \
                        split_movement[0] == piece.ADVISOR_REPR.upper():
                        if split_movement[2] == piece.FORWARDS_MOVEMENT:
                            if turn_color == piece.WHITE_PIECE:
                                # White forwards advisor
                                desired_position = (current_row - 1, destination_column)
                            else:
                                # Black forwards advisor
                                desired_position = (current_row + 1, destination_column)
                        else:
                            if turn_color == piece.WHITE_PIECE:
                                # White backwards advisor
                                desired_position = (current_row + 1, destination_column)
                            else:
                                # Black backwards advisor
                                desired_position = (current_row - 1, destination_column)
                    # Elephant case
                    elif current_piece.get_representation().upper() == \
                        piece.ELEPHANT_REPR.upper() and \
                        split_movement[0] == piece.ELEPHANT_REPR.upper():
                        if split_movement[2] == piece.FORWARDS_MOVEMENT:
                            if turn_color == piece.WHITE_PIECE:
                                # White forwards elephant
                                desired_position = (current_row - 2, destination_column)
                            else:
                                # Black forwards elephant
                                desired_position = (current_row + 2, destination_column)
                        else:
                            if turn_color == piece.WHITE_PIECE:
                                # White backwards elephant
                                desired_position = (current_row + 2, destination_column)
                            else:
                                # Black backwards elephant
                                desired_position = (current_row - 2, destination_column)
                    # Horse case
                    elif current_piece.get_representation().upper() == \
                        piece.HORSE_REPR.upper() and \
                        split_movement[0] == piece.HORSE_REPR.upper():
                        if split_movement[2] == piece.FORWARDS_MOVEMENT:
                            if turn_color == piece.WHITE_PIECE:
                                if 10-int(split_movement[3])-1 == current_column + 1 or \
                                    10-int(split_movement[3])-1 == current_column - 1:
                                    # White vertical L forwards horse
                                    desired_position = (current_row - 2, destination_column)
                                else:
                                    # White horizontal L forwards horse
                                    desired_position = (current_row - 1, destination_column)
                            else:
                                if int(split_movement[3])-1 == current_column + 1 or \
                                    int(split_movement[3])-1 == current_column - 1:
                                    # Black vertical L forwards horse
                                    desired_position = (current_row + 2, destination_column)
                                else:
                                    # Black horizontal L forwards horse
                                    desired_position = (current_row + 1, destination_column)
                        else:
                            if turn_color == piece.WHITE_PIECE:
                                if 10-int(split_movement[3])-1 == destination_column + 1 or \
                                    10-int(split_movement[3])-1 == destination_column - 1:
                                    # White vertical L backwards horse
                                    desired_position = (current_row + 2, destination_column)
                                else:
                                    # White horizontal L backwards horse
                                    desired_position = (current_row + 1, destination_column)
                            else:
                                if int(split_movement[3])-1 == current_column + 1 or \
                                    int(split_movement[3])-1 == current_column - 1:
                                    # Black vertical L backwards horse
                                    desired_position = (current_row - 2, destination_column)
                                else:
                                    # Black horizontal L backwards horse
                                    desired_position = (current_row - 1, destination_column)
                    # Generic case
                    elif split_movement[0] == piece.KING_REPR.upper() or \
                        split_movement[0] == piece.ROOK_REPR.upper() or \
                        split_movement[0] == piece.CANNON_REPR.upper() or \
                        split_movement[0] == piece.PAWN_REPR.upper() and pawn_counter == 1:
                        if split_movement[2] == piece.FORWARDS_MOVEMENT:
                            if turn_color == piece.WHITE_PIECE:
                                # White forwards piece
                                desired_position = (current_row - int(split_movement[3]),
                                    current_column)
                            else:
                                # Black forwards piece
                                desired_position = (current_row + int(split_movement[3]),
                                    current_column)
                        elif split_movement[2] == piece.BACKWARDS_MOVEMENT:
                            if turn_color == piece.WHITE_PIECE:
                                # White backwards piece
                                desired_position = (current_row + int(split_movement[3]),
                                    current_column)
                            else:
                                # Black backwards piece
                                desired_position = (current_row - int(split_movement[3]),
                                    current_column)
                        # Sideways movement
                        else:
                            desired_position = (current_row, destination_column)
            # X - case
            if split_movement[1] == piece.BACKWARDS_MOVEMENT:
                pieces = board.board[turn_color]
                current_row = 0
                chosen_pawn_white = -1
                chosen_pawn_black = 10

                max_col, pawn_counter = get_max_pawn_col(board, turn_color)

                # Getting middle back pawn in 4 & 5 pawn tandem
                if (pawn_counter == 4 or pawn_counter == 5) and turn_color == piece.WHITE_PIECE and \
                    split_movement[0].upper() == piece.PAWN_REPR.upper():
                    limit = -1
                    destination_column = 8 - max_col

                    pieces = board.board[turn_color]
                    for current_piece in pieces:
                        if current_piece.position[0] > limit and \
                            current_piece.get_representation().upper() == \
                            piece.PAWN_REPR.upper() and \
                            current_piece.position[1] == destination_column:
                            limit = current_piece.position[0]

                    new_limit = -1

                    for current_piece in pieces:
                        if current_piece.position[0] > new_limit and \
                            current_piece.get_representation().upper() == \
                            piece.PAWN_REPR.upper() and \
                            current_piece.position[1] == destination_column and \
                            current_piece.position[0] < limit:
                            new_limit = current_piece.position[0]
                            desired_pawn = current_piece
                elif (pawn_counter == 4 or pawn_counter == 5) and turn_color == piece.BLACK_PIECE and \
                    split_movement[0].upper() == piece.PAWN_REPR.upper():
                    limit = 10
                    destination_column = max_col

                    pieces = board.board[turn_color]
                    for current_piece in pieces:
                        if current_piece.position[0] < limit and \
                            current_piece.get_representation().upper() == \
                            piece.PAWN_REPR.upper() and \
                            current_piece.position[1] == destination_column:
                            limit = current_piece.position[0]

                    new_limit = 10

                    for current_piece in pieces:
                        if current_piece.position[0] < new_limit and \
                            current_piece.get_representation().upper() == \
                            piece.PAWN_REPR.upper() and \
                            current_piece.position[1] == destination_column and \
                            current_piece.position[0] > limit:
                            new_limit = current_piece.position[0]
                            desired_pawn = current_piece
                elif (pawn_counter == 2 or pawn_counter == 3) and turn_color == piece.WHITE_PIECE and \
                    split_movement[0].upper() == piece.PAWN_REPR.upper():
                    limit = -1
                    destination_column = 8 - max_col

                    pieces = board.board[turn_color]
                    for current_piece in pieces:
                        if current_piece.position[0] > limit and \
                            current_piece.get_representation().upper() == \
                            piece.PAWN_REPR.upper() and \
                            current_piece.position[1] == destination_column:
                            limit = current_piece.position[0]
                            desired_pawn = current_piece
                elif (pawn_counter == 2 or pawn_counter == 3) and turn_color == piece.BLACK_PIECE and \
                    split_movement[0].upper() == piece.PAWN_REPR.upper():
                    limit = 10
                    destination_column = max_col

                    pieces = board.board[turn_color]
                    for current_piece in pieces:
                        if current_piece.position[0] < limit and \
                            current_piece.get_representation().upper() == \
                            piece.PAWN_REPR.upper() and \
                            current_piece.position[1] == destination_column:
                            limit = current_piece.position[0]
                            desired_pawn = current_piece

                for current_piece in pieces:
                    if current_piece.get_representation().upper() == split_movement[0].upper():
                        current_column = current_piece.position[1]

                for current_piece in pieces:
                    # Column where the piece is expected to go
                    if turn_color == piece.WHITE_PIECE:
                        destination_column = 10 - int(split_movement[3]) - 1
                    else:
                        destination_column = int(split_movement[3]) - 1

                    if turn_color == piece.WHITE_PIECE:
                        if current_piece.get_representation().upper() == split_movement[0] and \
                            current_piece.position[1] == current_column and \
                            current_piece.position[0] > chosen_pawn_white:
                            desired_piece = current_piece
                            chosen_pawn_white = current_piece.position[0]
                            current_row = current_piece.position[0]
                    else:
                        if current_piece.get_representation().upper() == split_movement[0] and \
                            current_piece.position[1] == current_column and \
                            current_piece.position[0] < chosen_pawn_black:
                            desired_piece = current_piece
                            chosen_pawn_black = current_piece.position[0]
                            current_row = current_piece.position[0]

                    # Middle back 4 & 5 pawn tandem
                    if current_piece.get_representation().upper() == piece.PAWN_REPR.upper() and \
                        pawn_counter > 1 and \
                        split_movement[0] == piece.PAWN_REPR.upper():
                        # Middle back white 4 & 5 pawn tandem
                        if turn_color == piece.WHITE_PIECE:
                            # Middle back forwards white 4 & 5 pawn tandem
                            if split_movement[2] == piece.FORWARDS_MOVEMENT:
                                desired_position = (desired_pawn.position[0] - 1,
                                    desired_pawn.position[1])
                            # Middle back sideways white 4 & 5 pawn tandem
                            else:
                                desired_position = (desired_pawn.position[0],
                                    10 - int(split_movement[3]) - 1)
                        # Middle back black 4 & 5 pawn tandem
                        else:
                            # Middle back forwards black 4 & 5 pawn tandem
                            if split_movement[2] == piece.FORWARDS_MOVEMENT:
                                desired_position = (desired_pawn.position[0] + 1,
                                    desired_pawn.position[1])
                            # Middle back sideways black 4 & 5 pawn tandem
                            else:
                                desired_position = (desired_pawn.position[0],
                                    int(split_movement[3]) - 1)
                        desired_piece = desired_pawn
                    # Advisor case
                    elif current_piece.get_representation().upper() == \
                        piece.ADVISOR_REPR.upper() and \
                        split_movement[0] == piece.ADVISOR_REPR.upper():
                        if split_movement[2] == piece.FORWARDS_MOVEMENT:
                            if turn_color == piece.WHITE_PIECE:
                                # White forwards advisor
                                desired_position = (current_row - 1, destination_column)
                            else:
                                # Black forwards advisor
                                desired_position = (current_row + 1, destination_column)
                        else:
                            if turn_color == piece.WHITE_PIECE:
                                # White backwards advisor
                                desired_position = (current_row + 1, destination_column)
                            else:
                                # Black backwards advisor
                                desired_position = (current_row - 1, destination_column)
                    # Elephant case
                    elif current_piece.get_representation().upper() == \
                        piece.ELEPHANT_REPR.upper() and \
                        split_movement[0] == piece.ELEPHANT_REPR.upper():
                        if split_movement[2] == piece.FORWARDS_MOVEMENT:
                            if turn_color == piece.WHITE_PIECE:
                                # White forwards elephant
                                desired_position = (current_row - 2, destination_column)
                            else:
                                # Black forwards elephant
                                desired_position = (current_row + 2, destination_column)
                        else:
                            if turn_color == piece.WHITE_PIECE:
                                # White backwards elephant
                                desired_position = (current_row + 2, destination_column)
                            else:
                                # Black backwards elephant
                                desired_position = (current_row - 2, destination_column)
                    # Horse case
                    elif current_piece.get_representation().upper() == \
                        piece.HORSE_REPR.upper() and \
                        split_movement[0] == piece.HORSE_REPR.upper():
                        if split_movement[2] == piece.FORWARDS_MOVEMENT:
                            if turn_color == piece.WHITE_PIECE:
                                if int(split_movement[3])-1 == current_column + 1 or \
                                    int(split_movement[3])-1 == current_column - 1:
                                    # White vertical L forwards horse
                                    desired_position = (current_row - 2, destination_column)
                                else:
                                    # White horizontal L forwards horse
                                    desired_position = (current_row - 1, destination_column)
                            else:
                                if int(split_movement[3])-1 == current_column + 1 or \
                                    int(split_movement[3])-1 == current_column - 1:
                                    # Black vertical L forwards horse
                                    desired_position = (current_row + 2, destination_column)
                                else:
                                    # Black horizontal L forwards horse
                                    desired_position = (current_row + 1, destination_column)
                        else:
                            if turn_color == piece.WHITE_PIECE:
                                if int(split_movement[3])-1 == destination_column + 1 or \
                                    int(split_movement[3])-1 == destination_column - 1:
                                    # White vertical L backwards horse
                                    desired_position = (current_row + 2, destination_column)
                                else:
                                    # White horizontal L backwards horse
                                    desired_position = (current_row + 1, destination_column)
                            else:
                                if int(split_movement[3])-1 == current_column + 1 or \
                                    int(split_movement[3])-1 == current_column - 1:
                                    # Black vertical L backwards horse
                                    desired_position = (current_row - 2, destination_column)
                                else:
                                    # Black horizontal L backwards horse
                                    desired_position = (current_row - 1, destination_column)
                    # Generic case
                    elif split_movement[0] == piece.KING_REPR.upper() or \
                        split_movement[0] == piece.ROOK_REPR.upper() or \
                        split_movement[0] == piece.CANNON_REPR.upper() or \
                        split_movement[0] == piece.PAWN_REPR.upper() and pawn_counter == 1:
                        if split_movement[2] == piece.FORWARDS_MOVEMENT:
                            if turn_color == piece.WHITE_PIECE:
                                # White forwards piece
                                desired_position = (current_row - int(split_movement[3]),
                                    current_column)
                            else:
                                # Black forwards piece
                                desired_position = (current_row + int(split_movement[3]),
                                    current_column)
                        elif split_movement[2] == piece.BACKWARDS_MOVEMENT:
                            if turn_color == piece.WHITE_PIECE:
                                # White backwards piece
                                desired_position = (current_row + int(split_movement[3]),
                                    current_column)
                            else:
                                # Black backwards piece
                                desired_position = (current_row - int(split_movement[3]),
                                    current_column)
                        # Sideways movement
                        else:
                            desired_position = (current_row, destination_column)
    # 4 & 5 pawn tandem
    elif split_movement[0] == piece.FORWARDS_MOVEMENT or \
        split_movement[0] == piece.BACKWARDS_MOVEMENT:
        # + case
        if split_movement[0] == piece.FORWARDS_MOVEMENT:
            pieces = board.board[turn_color]

            current_column, pawn_counter = get_max_pawn_col(board, turn_color)

            if turn_color == piece.WHITE_PIECE:
                chosen_pawn = 10
            else:
                chosen_pawn = -1

            for current_piece in pieces:
                if turn_color == piece.WHITE_PIECE:
                    if current_piece.position[1] == (8 - current_column) and \
                        current_piece.position[0] < chosen_pawn and \
                        current_piece.get_representation().upper() == piece.PAWN_REPR.upper():
                        desired_piece = current_piece
                        chosen_pawn = current_piece.position[0]
                        current_row = current_piece.position[0]

                        # Forwards front white pawn
                        if split_movement[2] == piece.FORWARDS_MOVEMENT:
                            desired_position = (current_row - 1,
                                8 - current_column)
                        # Sideways front white pawn
                        else:
                            desired_position = (current_row, 10 - int(split_movement[3]) - 1)
                else:
                    if current_piece.position[1] == current_column and \
                        current_piece.position[0] > chosen_pawn:
                        desired_piece = current_piece
                        chosen_pawn = current_piece.position[0]
                        current_row = current_piece.position[0]

                        # Forwards front black pawn
                        if split_movement[2] == piece.FORWARDS_MOVEMENT:
                            desired_position = (current_row + 1,
                                current_column)
                        # Sideways front black pawn
                        else:
                            desired_position = (current_row, int(split_movement[3]) - 1)
        # - case
        else:
            pieces = board.board[turn_color]

            current_column, pawn_counter = get_max_pawn_col(board, turn_color)

            if turn_color == piece.WHITE_PIECE:
                chosen_pawn = -1
            else:
                chosen_pawn = 10

            for current_piece in pieces:
                if turn_color == piece.WHITE_PIECE:
                    if current_piece.position[1] == (8 - current_column) and \
                        current_piece.position[0] > chosen_pawn and \
                        current_piece.get_representation().upper() == piece.PAWN_REPR.upper():
                        desired_piece = current_piece
                        chosen_pawn = current_piece.position[0]
                        current_row = current_piece.position[0]

                        # Forwards back white pawn
                        if split_movement[2] == piece.FORWARDS_MOVEMENT:
                            desired_position = (current_row - 1,
                                8 - current_column)
                        # Sideways back white pawn
                        else:
                            desired_position = (current_row, 10 - int(split_movement[3]) - 1)
                else:
                    if current_piece.position[1] == current_column and \
                        current_piece.position[0] < chosen_pawn:
                        desired_piece = current_piece
                        chosen_pawn = current_piece.position[0]
                        current_row = current_piece.position[0]

                        # Forwards back black pawn
                        if split_movement[2] == piece.FORWARDS_MOVEMENT:
                            desired_position = (current_row + 1,
                                current_column)
                        # Sideways back black pawn
                        else:
                            desired_position = (current_row, int(split_movement[3]) - 1)
    # Double tandem
    else:
        # 0 + case
        if split_movement[1] == piece.FORWARDS_MOVEMENT:
            # White 0 + case
            if turn_color == piece.WHITE_PIECE:
                destination_column = 10 - int(split_movement[0]) - 1
                desired_piece = None
                desired_position = None
                limit = 10

                posible_sideways = 10 - int(split_movement[3]) - 1

                pieces = board.board[turn_color]
                for current_piece in pieces:
                    if current_piece.position[0] < limit and \
                        current_piece.get_representation().upper() == piece.PAWN_REPR.upper() and \
                        current_piece.position[1] == destination_column:
                        limit = current_piece.position[0]
                        desired_piece = current_piece

                        # White 0 + forwards case
                        if split_movement[2] == piece.FORWARDS_MOVEMENT:
                            desired_position = (current_piece.position[0] - 1,
                                current_piece.position[1])
                        # White 0 - sideways case
                        else:
                            desired_position = (current_piece.position[0], posible_sideways)
            # Black 0 + case
            else:
                destination_column = int(split_movement[0]) - 1
                desired_piece = None
                desired_position = None
                limit = -1

                posible_sideways = int(split_movement[3]) - 1

                pieces = board.board[turn_color]
                for current_piece in pieces:
                    if current_piece.position[0] > limit and \
                        current_piece.get_representation().upper() == piece.PAWN_REPR.upper() and \
                        current_piece.position[1] == destination_column:
                        limit = current_piece.position[0]
                        desired_piece = current_piece

                        # Black 0 + forwards case
                        if split_movement[2] == piece.FORWARDS_MOVEMENT:
                            desired_position = (current_piece.position[0] + 1,
                                current_piece.position[1])
                        # Black 0 + sideways case
                        else:
                            desired_position = (current_piece.position[0], posible_sideways)
        # 0 - case
        elif split_movement[1] == piece.BACKWARDS_MOVEMENT:
            # White 0 - case
            if turn_color == piece.WHITE_PIECE:
                destination_column = 10 - int(split_movement[0]) - 1
                desired_piece = None
                desired_position = None
                limit = -1

                posible_sideways = 10 - int(split_movement[3]) - 1

                pieces = board.board[turn_color]
                for current_piece in pieces:
                    if current_piece.position[0] > limit and \
                        current_piece.get_representation().upper() == piece.PAWN_REPR.upper() and \
                        current_piece.position[1] == destination_column:
                        limit = current_piece.position[0]
                        desired_piece = current_piece

                        # White 0 - forwards case
                        if split_movement[2] == piece.FORWARDS_MOVEMENT:
                            desired_position = (current_piece.position[0] - 1,
                                current_piece.position[1])
                        # White 0 - sideways case
                        else:
                            desired_position = (current_piece.position[0], posible_sideways)
            # Black 0 - case
            else:
                destination_column = int(split_movement[0]) - 1
                desired_piece = None
                desired_position = None
                limit = 10

                posible_sideways = int(split_movement[3]) - 1

                pieces = board.board[turn_color]
                for current_piece in pieces:
                    if current_piece.position[0] < limit and \
                        current_piece.get_representation().upper() == piece.PAWN_REPR.upper() and \
                        current_piece.position[1] == destination_column:
                        limit = current_piece.position[0]
                        desired_piece = current_piece

                        # Black 0 - forwards case
                        if split_movement[2] == piece.FORWARDS_MOVEMENT:
                            desired_position = (current_piece.position[0] + 1,
                                current_piece.position[1])
                        # Black 0 - sideways case
                        else:
                            desired_position = (current_piece.position[0], posible_sideways)
        # 0 0 case
        else:
            limit = -1

            if turn_color == piece.WHITE_PIECE:
                destination_column = 10 - int(split_movement[0]) - 1
            else:
                destination_column = int(split_movement[0]) - 1

            pieces = board.board[turn_color]
            for current_piece in pieces:
                if current_piece.position[0] > limit and \
                    current_piece.get_representation().upper() == piece.PAWN_REPR.upper() and \
                    current_piece.position[1] == destination_column:
                    limit = current_piece.position[0]

            new_limit = -1

            for current_piece in pieces:
                if current_piece.position[0] > new_limit and \
                    current_piece.get_representation().upper() == piece.PAWN_REPR.upper() and \
                    current_piece.position[1] == destination_column and \
                    current_piece.position[0] < limit:
                    new_limit = current_piece.position[0]
                    desired_piece = current_piece

            # 0 0 forwards case
            if split_movement[2] == piece.FORWARDS_MOVEMENT:
                # White 0 0 forwards case
                if turn_color == piece.WHITE_PIECE:
                    desired_position = (desired_piece.position[0] - 1,
                        desired_piece.position[1])
                # Black 0 0 forwards case
                else:
                    desired_position = (desired_piece.position[0] + 1,
                        desired_piece.position[1])
            # 0 0 sideways case
            else:
                # White 0 0 sideways case
                if turn_color == piece.WHITE_PIECE:
                    desired_position = (desired_piece.position[0],
                        10 - int(split_movement[3]) - 1)
                # Black 0 0 sideways case
                else:
                    desired_position = (desired_piece.position[0],
                        int(split_movement[3]) - 1)

    return desired_piece, desired_position


def get_max_pawn_col (board, color):
    '''Returns a the column with the highest number of pawns and this number'''
    pawns = dict.fromkeys([0,1,2,3,4,5,6,7,8],0)

    pieces = board.board[color]
    for current_piece in pieces:
        if current_piece.get_representation().upper() == piece.PAWN_REPR.upper():
            if color == piece.WHITE_PIECE:
                pawns[8 - int(current_piece.position[1])] += 1
            else:
                pawns[int(current_piece.position[1])] += 1

    pawn_counter = 0
    max_col = -1

    for item in pawns.items():
        if item[1] > pawn_counter:
            max_col = item[0]
            pawn_counter = item[1]

    return max_col, pawn_counter
