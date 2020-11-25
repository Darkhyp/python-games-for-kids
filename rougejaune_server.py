"""
Game server
"""
import pickle
import socket
from _thread import *

from rougejaune.CONFIGS import SERVER_ADDR, SERVER_PORT
from rougejaune import Players


def threaded_client(conn,p,players):
    conn.send(str.encode(str(p)))

    while True:
        try:
            data = conn.recv(2048*2).decode()
            if not data:
                print(f'No response from player {p}')
                break
            else:
                if data=='reset':
                    players.reset_moves()
                elif data.isdigit():
                    print('Player {} makes a turn at column {}'.format(p,int(data)))
                    players.set_move(p,int(data))

                conn.sendall(pickle.dumps(players))
        except Exception as e:
            print(e)
            break

    print(f'Disconnecting player {p}')
    conn.close()
    players.set_connection(p,False)


class Server:
    currentPlayer = 0
    connected = set()
    id_game = 0
    game = [Players(0)]
    idCount = -1

    def __init__(self,addr):
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            self.socket.bind(addr)
        except socket.error as e:
            str(e)
        self.socket.listen(2)
        print('Server is started. Waiting for connection...')

    def start(self):
        while True:
            conn,addr = self.socket.accept()
            print(addr, ' is connected')
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
            self.game[self.id_game].set_connection(current_player,True)
            print(f'add a player {current_player}')

            # start listening of client
            start_new_thread(threaded_client, (conn,current_player,self.game[self.id_game]))


# run server
if __name__ == '__main__':
    s = Server((SERVER_ADDR,SERVER_PORT))
    s.start()
