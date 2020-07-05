import socket
import threading
import os


class Client:
    """This client is designed for sending files vie tcp sockets"""

    FIRST_MESSAGE_SIZE = 1024  # size of the package for specifying the size of the message sent after this one
    FORMAT = 'utf-8'  # format of the messages sent
    DISCONNECT_MESSAGE = "DISCONNECT_COMMAND".encode(FORMAT)
    PORT = 5050  # was chosen because ports' numbers above 5000 are usually unused

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to_server(self):

        try:
            SERVER = input('Enter the ip address of the server you want to connect to: ')
            ADDR = (SERVER, self.PORT)
            self.client.connect(ADDR)
        except:
            print(f'It looks like the address [{SERVER}] you provided is not valid, please enter a valid one.')
            self.connect_to_server()

    def send_file(self, file_path, where_to_store):

        file_name = file_path.split('\\')[-1]

        with open(file_path, 'rb') as f:
            contents = f.read()

        message = f'{where_to_store} {file_name} {contents}'.encode(self.FORMAT)

        message_len = str(len(message)).encode(self.FORMAT)
        message_len += b' ' * (self.FIRST_MESSAGE_SIZE - len(message_len))

        self.client.send(message_len)
        self.client.send(message)

        print(self.client.recv(self.FIRST_MESSAGE_SIZE).decode(self.FORMAT))

    def disconnect(self):
        DISCONNECT_MESSAGE = self.DISCONNECT_MESSAGE + b' ' * (self.FIRST_MESSAGE_SIZE - len(self.DISCONNECT_MESSAGE))
        self.client.send(DISCONNECT_MESSAGE)


def request_info():
    file_path = input('Where is the file you want to send located? ')
    where_to_store = input('Where on the server should your file be stored? ')

    try:
        with open(file_path) as f:
            pass
    except FileExistsError:
        print('The path you specified is an invalid one')
        return request_info()

    return file_path, where_to_store
