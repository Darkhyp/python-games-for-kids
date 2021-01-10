"""
run server for the "game red contre yellow" (rougejaune)
"""
import pickle
import socket
import sys
from _thread import *

from common.common import is_valid_ip
from rougejaune.CONFIGS import SERVER_ADDRESS, SERVER_PORT
from rougejaune import Players


def threaded_client(connection, current_player, game):
    """
    threaded function to exchange with client
    :param connection:      connection parameters
    :param current_player:  current player identification
    :param game:            game parameters
    :return: None
    """
    connection.send(str.encode(str(current_player)))

    # listening to the client
    while True:
        try:
            # receive the data from connection
            data = connection.recv(2048 * 2).decode()
            if not data:
                print(f'No response from player {current_player}')
                break
            else:
                # there is a response from the player
                if data == 'reset':
                    game.reset_moves()
                elif data.isdigit():
                    print('Player {} makes a turn at column {}'.format(current_player, int(data)))
                    game.set_move(current_player, int(data))

                connection.sendall(pickle.dumps(game))
        except Exception as e:
            print(e)
            break

    print(f'Disconnecting the player {current_player}')
    connection.close()
    game.set_connection(current_player, False)


class Server:
    """
    class to create the server
    """
    is_server_run = False
    currentPlayer = 0
    connected = set()
    id_game = 0
    game = [Players(0)]
    idCount = -1

    def __init__(self, address):
        # init socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.bind(address)
            self.is_server_run = True
        except socket.error as e:
            print(f'{e}. Could not start server at {address}!')
            return
        self.socket.listen(2)
        print('Server is started. Waiting for connection...')

    def start(self):
        """
        start the server: listen on the port and establish a connection with the client
        :return: None
        """
        while self.is_server_run:
            connection, address = self.socket.accept()
            print(address, ' is connected')
            self.idCount += 1

            # create a new game
            if self.game[self.id_game].connected():
                self.game.append(Players(self.id_game))
                self.id_game += 1
                print(f'Create a new game {self.id_game}')

            # add a new player
            if not self.game[self.id_game].get_connection(0):
                current_player = 0
                print(f'Create a new game {self.id_game}')
            else:
                current_player = 1
            self.game[self.id_game].set_connection(current_player, True)
            print(f'add a player {current_player}')

            # start listening to the client
            start_new_thread(threaded_client, (connection, current_player, self.game[self.id_game]))


if __name__ == '__main__':
    # Get full command-line arguments
    full_cmd_arguments = sys.argv

    # find IP v4 address in the command-line arguments
    server_address = next((arg for arg in full_cmd_arguments if is_valid_ip(arg)), None)
    server_port = SERVER_PORT
    if server_address is None:
        server_address = SERVER_ADDRESS
        print(f"IP not found in command line arguments. Use default!")
    else:
        print(f"IP found in command line arguments")
        # port number in the command-line arguments
        ind = full_cmd_arguments.index(server_address)
        if ind+1 < len(full_cmd_arguments):
            if str.isdecimal(full_cmd_arguments[ind+1]):
                print(f"port found in command line arguments")
                server_port = int(full_cmd_arguments[ind+1])
    print(f"Server IP is {server_address}:{server_port}")

    # create and start server
    s = Server((server_address, server_port))
    s.start()
