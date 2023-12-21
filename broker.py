''' Implements the broker for the DB '''


import sqlite3
import piece


DATABASE = r'db/xiangqi.db'
TEST_DATABASE = r'db/test.db'


class Broker(object):
    '''Broker of the used db'''

    def __init__(self):
        self.connection = None
        self.cursor = None


    def connect(self):
        '''Creates a cursor connected to the db'''
        self.connection = sqlite3.connect(TEST_DATABASE)
        self.cursor = self.connection.cursor()


    def disconnect(self):
        '''Commits changes and disconnects from the db'''
        self.connection.commit()

        self.connection.close()
        self.connection = None
        self.cursor = None


    def create_tables(self):
        '''Creates the necessary tables for the db functioning'''
        self.connect()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS player (user text, password text,
            email text, elo integer, winned_matches integer, drawn_matches integer,
            lost_matches integer, UNIQUE (user), PRIMARY KEY (email))''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS match (player1 text, player2 text,
            name text, id_match text, result text, PRIMARY KEY (id_match))''')

        self.disconnect()


    def add_user(self, user, password, email):
        '''Adds an user to the db'''
        self.connect()

        self.cursor.execute('''INSERT OR IGNORE INTO player VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (user, password, email, 1000, 0, 0, 0))

        self.disconnect()


    def boolean_add_user(self, user, password, email):
        '''Adds an user to the db, and, if possible, returns True'''
        possible_user = self.select_user_by_email(email)

        if possible_user is not None:
            return False

        possible_user = self.select_user_by_password(user, password)

        if possible_user is not None:
            return False

        possible_user = self.select_user_by_name(user)

        if possible_user is not None:
            return False

        self.connect()

        self.cursor.execute('''INSERT OR IGNORE INTO player VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (user, password, email, 1000, 0, 0, 0))

        self.disconnect()

        return True


    def select_user_by_password(self, user, password):
        '''Returns an user from the db given its user and password'''
        self.connect()

        desired_player = self.cursor.execute('''SELECT * FROM player WHERE user == ?
            AND password == ?''', (user, password)).fetchone()

        self.disconnect()

        return desired_player


    def select_user_by_name(self, user):
        '''Returns an user from the db given its name'''
        self.connect()

        desired_player = self.cursor.execute('''SELECT * FROM player WHERE user == ?''',
            (user,)).fetchone()

        self.disconnect()

        return desired_player


    def select_user_by_email(self, email):
        '''Returns an user from the db given its email'''
        self.connect()

        desired_player = self.cursor.execute('''SELECT * FROM player WHERE email == ?''',
            (email,)).fetchone()

        self.disconnect()

        return desired_player


    def delete_user_by_nick(self, user):
        '''Removes an user from the db given its username'''
        self.connect()

        self.cursor.execute('''DELETE FROM player WHERE user == ?''', (user,))

        self.disconnect()


    def boolean_delete_user_by_nick(self, user, password):
        '''Removes an user from the db given its username, and returns True, if possible'''
        possible_user = self.select_user_by_password(user, password)

        if possible_user is None:
            return False

        self.connect()

        self.cursor.execute('''DELETE FROM player WHERE user == ?''', (user,))

        self.disconnect()

        return True


    def delete_user_by_email(self, email):
        '''Removes an user from the db given its email'''
        self.connect()

        self.cursor.execute('''DELETE FROM player WHERE email == ?''', (email,))

        self.disconnect()


    def boolean_delete_user_by_email(self, email):
        '''Removes an user from the db given its email, and returns True, if possible'''
        possible_user = self.select_user_by_email(email)

        if possible_user is None:
            return False

        self.connect()

        self.cursor.execute('''DELETE FROM player WHERE email == ?''', (email,))

        self.disconnect()

        return True


    def update_user(self, user, password, email):
        '''Updates an user information'''
        self.connect()

        self.cursor.execute('''UPDATE player SET user = ?, password = ? WHERE email == ?''',
            (user,password,email))

        self.disconnect()


    def boolean_update_user(self, user, password, email):
        '''Updates an user information, and returns True, if possible'''
        possible_user = self.select_user_by_email(email)

        if possible_user is None:
            return False

        if possible_user[0] == user and possible_user[1] == password and \
            possible_user[2] == email:
            return False

        self.connect()

        self.cursor.execute('''UPDATE player SET user = ?, password = ? WHERE email == ?''',
            (user,password,email))

        self.disconnect()

        return True


    def update_win_loser(self, winner, loser, board, winner_color):
        '''Updated the points for the winner and loser of a match'''
        self.connect()

        elo_winner = self.cursor.execute('''SELECT elo FROM player WHERE user == ?''',
            (winner,)).fetchone()
        wins = self.cursor.execute('''SELECT winned_matches FROM player WHERE user == ?''',
            (winner,)).fetchone()

        elo_loser = self.cursor.execute('''SELECT elo FROM player WHERE user == ?''',
            (loser,)).fetchone()
        losses = self.cursor.execute('''SELECT lost_matches FROM player WHERE user == ?''',
            (loser,)).fetchone()

        wins = wins[0] + 1
        losses = losses[0] + 1

        elo_ratio = elo_loser[0] / elo_winner[0]

        new_elo_winner = elo_winner[0]
        new_elo_loser = elo_loser[0]

        pieces = board.board[winner_color]
        for i in range(len(pieces)):
            new_elo_winner += 2 * elo_ratio
            new_elo_loser -= 2 * elo_ratio

        new_elo_winner += 15
        new_elo_loser -= 15

        new_elo_loser = max(new_elo_loser,0)

        self.cursor.execute('''UPDATE player SET elo = ?, winned_matches = ? WHERE user == ?''',
            (int(new_elo_winner),wins,winner))
        self.cursor.execute('''UPDATE player SET elo = ?, lost_matches = ? WHERE user == ?''',
            (int(new_elo_loser),losses,loser))

        self.disconnect()


    def update_draw(self, player1, player2, board, player1_color):
        '''Updated the points in case of a draw'''
        self.connect()

        elo_p1 = self.cursor.execute('''SELECT elo FROM player WHERE user == ?''',
            (player1,)).fetchone()
        draws_p1 = self.cursor.execute('''SELECT drawn_matches FROM player WHERE user == ?''',
            (player1,)).fetchone()

        elo_p2 = self.cursor.execute('''SELECT elo FROM player WHERE user == ?''',
            (player2,)).fetchone()
        draws_p2 = self.cursor.execute('''SELECT drawn_matches FROM player WHERE user == ?''',
            (player2,)).fetchone()

        draws_p1 = draws_p1[0] + 1
        draws_p2 = draws_p2[0] + 1

        if player1_color == piece.WHITE_PIECE:
            new_color = piece.BLACK_PIECE
        else:
            new_color = piece.WHITE_PIECE

        new_elo_p1 = elo_p1[0]
        new_elo_p2 = elo_p2[0]

        pieces = board.board[new_color]
        for i in range(len(pieces)):
            new_elo_p1 -= 1

        pieces = board.board[player1_color]
        for i in range(len(pieces)):
            new_elo_p2 -= 1

        new_elo_p1 = max(new_elo_p1,0)
        new_elo_p2 = max(new_elo_p2,0)

        self.cursor.execute('''UPDATE player SET elo = ?, drawn_matches = ? WHERE user == ?''',
            (new_elo_p1,draws_p1,player1))
        self.cursor.execute('''UPDATE player SET elo = ?, drawn_matches = ? WHERE user == ?''',
            (new_elo_p2,draws_p2,player2))

        self.disconnect()


    def select_all_users(self):
        '''Returns every player from the db'''
        self.connect()

        players = self.cursor.execute('''SELECT * FROM player''').fetchall()

        self.disconnect()

        return players


    def add_match(self, player1, player2, name, id_match, result):
        '''Adds a match to the db'''
        self.connect()

        self.cursor.execute('''INSERT OR IGNORE INTO match VALUES (?, ?, ?, ?, ?)''',
            (player1, player2, name, id_match, result))

        self.disconnect()


    def select_match(self, id_match):
        '''Returns a match from the db given its id'''
        self.connect()

        desired_match = self.cursor.execute('''SELECT * FROM match WHERE id_match == ?''',
            (id_match,)).fetchone()

        self.disconnect()

        return desired_match


    def select_all_matches(self):
        '''Returns every match from the db'''
        self.connect()

        matches = self.cursor.execute('''SELECT * FROM match''').fetchall()

        self.disconnect()

        return matches
