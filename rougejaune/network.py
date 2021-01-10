"""
Test network connection
"""
import pickle
import socket


class Network:
    """
    Establish network connection
    """
    def __init__(self, address):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = address  # (server_address, server_port)

        self.player = self.connect()
        print("Player {} is connected".format(self.player))

    def get_player(self):
        return self.player

    def connect(self):
        try:
            self.socket.connect(self.address)
            return self.socket.recv(2048).decode('utf-8')
        except socket.error as e:
            print(e)

    def send(self, data):
        try:
            self.socket.send(str.encode(data))
            # return self.socket.recv(2048*2).decode('utf-8')
            return pickle.loads(self.socket.recv(2048 * 2))
        except socket.error as e:
            print(e)
