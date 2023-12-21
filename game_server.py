''' Module for game server '''

import socket
import threading

from game import Game
from broker import Broker
from protocol import *

DEFAULT_PORT = 9999
DEFAULT_HOST = ''

class GameServer():
    ''' Class implementation for a game server '''
    def __init__(self):
        ''' Constructor method for the game server '''
        self.current_games = []
        self.gameserver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.gameserver_socket.bind((DEFAULT_HOST, DEFAULT_PORT))
        self.broker = Broker()

    def create_game(self, user_socket, game_name):
        ''' Method to create a new game instance '''
        username = game_name.split(PROTOCOL_SEPARATOR)[1]
        game_name = game_name.split(PROTOCOL_SEPARATOR)[0]
        for game_to_play in self.current_games:
            if game_to_play.name == game_name:
                self.gameserver_socket.sendto(ERROR_ADDING_GAME.encode(), user_socket)
                return
        game = Game(player1= user_socket, name = game_name, game_server = self, username1=username)
        self.current_games.append(game)
        
        self.gameserver_socket.sendto(REPLY_ADD_GAME.encode(), user_socket)

    def get_unprepared_games(self, user_socket):
        ''' Method to get list of to-play games '''
        game_list = REPLY_GAME_LIST

        for to_play_game in self.current_games:
            game_list = game_list + to_play_game.name + PROTOCOL_SEPARATOR

        self.gameserver_socket.sendto(game_list.encode(), user_socket)


    def add_player_to_game(self, user_socket, game_name):
        ''' Method that tries to add a player to a to-play game '''
        username = game_name.split(PROTOCOL_SEPARATOR)[1]
        game_name = game_name.split(PROTOCOL_SEPARATOR)[0]
        for game_to_play in self.current_games:
            if game_to_play.name == game_name:
                if game_to_play.insert_player(user_socket):
                    game_to_play.username2 = username
                    self.gameserver_socket.sendto(REPLY_ADD_PLAYER_TO_GAME.encode(), user_socket)
                    self.current_games.remove(game_to_play)
                    threading.Thread(
                        target = game_to_play.play,
                        args=()
                    ).start()
                    return

        self.gameserver_socket.sendto(ERROR_ADDING_PLAYER_TO_GAME.encode(), user_socket)


    def add_user(self, user_socket, username, password, email):
        ''' Method that adds a user to the DB as requested by a client '''
        if self.broker.boolean_add_user(username, password, email):
            self.gameserver_socket.sendto(REPLY_ADD_USER.encode(), user_socket)
        else:
            self.gameserver_socket.sendto(ERROR_ADDING_USER.encode(), user_socket)


    def remove_user(self, user_socket, email, password):
        ''' Method that removes user from DB as requested by a client '''
        if self.broker.boolean_delete_user_by_email(email):
            self.gameserver_socket.sendto(REPLY_REMOVE_USER.encode(), user_socket)
        else:
            self.gameserver_socket.sendto(ERROR_REMOVING_USER.encode(), user_socket)

    def update_user(self, user_socket, username, password, email):
        ''' Method that updates a user from DB as requested by a client '''
        if self.broker.boolean_update_user(username, password, email):
            self.gameserver_socket.sendto(REPLY_UPDATE_USER.encode(), user_socket)
        else:
            self.gameserver_socket.sendto(ERROR_UPDATING_USER.encode(), user_socket)


    def login(self, user_socket, username, password, email):
        users = self.broker.select_user_by_email(email)
        if users == None:
            self.gameserver_socket.sendto(ERROR_LOGIN.encode(), user_socket) 
        else:
            if users[0] == username and users[1] == password:
                self.gameserver_socket.sendto(REPLY_LOGIN.encode(), user_socket)
            else:
                self.gameserver_socket.sendto(ERROR_LOGIN.encode(), user_socket)         


    def update_elo(self, result, player1, player2, final_board, color_first):
        if result == IDENTIFIER_TIE:
            self.broker.update_draw(player1, player2, final_board, color_first)
        else:
            self.broker.update_win_loser(player1,player2, final_board, color_first)

    def run(self):
        ''' Method that models the infinite loop of the game server '''
        while True:
            request, client_socket = self.gameserver_socket.recvfrom(1024)
            try:
                request = request.decode()
                self.manage_request(request , client_socket)
            except Exception as ex:
                print(f"Exception: {ex}")

    def manage_request(self, request, client_socket):
        # Must identify the requests depending on data that was sent
        request_id = request[IDENTIFIER_BEGIN : IDENTIFIER_END]
        request_data = request[IDENTIFIER_END:]

        if request_id == REQUEST_ADD_GAME:
            self.create_game(client_socket, request_data)
        elif request_id == REQUEST_ADD_PLAYER_TO_GAME:
            self.add_player_to_game(client_socket, request_data)
        elif request_id == REQUEST_GAME_LIST:
            self.get_unprepared_games(client_socket)
        elif request_id == REQUEST_ADD_USER:
            user_data = request_data.split(PROTOCOL_SEPARATOR)
            self.add_user(client_socket, user_data[0], user_data[1], user_data[2])
        elif request_id == REQUEST_REMOVE_USER:
            user_data = request_data.split(PROTOCOL_SEPARATOR)
            self.remove_user(client_socket, user_data[0])
        elif request_id == REQUEST_UPDATE_USER:
            user_data = request_data.split(PROTOCOL_SEPARATOR)
            self.update_user(client_socket, user_data[0], user_data[1], user_data[2])
        elif request_id == REQUEST_LOGIN:
            user_data = request_data.split(PROTOCOL_SEPARATOR)
            self.login(client_socket, user_data[0], user_data[1], user_data[2])
                                    #USUARIO        CONTRASEÑA      MAIL



''' PROCESS MAIN LOOP '''

if __name__ == '__main__':
    try:
        server = GameServer()
        print('[GAME-SERVER]: Created', flush=True)
        server.run()
    except Exception as e:
        print(e)
        print('[GAME-SERVER]: Finished')
