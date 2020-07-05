import socket
import threading
import os


FIRST_MESSAGE_SIZE = 1024  # size of the package for specifying the size of the message sent after this one
FORMAT = 'utf-8'  # format of the messages sent
DISCONNECT_MESSAGE = "DISCONNECT_COMMAND"
PORT = 5050  # was chosen because ports' numbers above 5000 are usually unused


def parse_request(request):
    # path to the file on the server / name of the file / contents
    path, file_name, contents = request.split()
    return path, file_name, contents


def process_connection(connection, addr):

    print(f'A client located at {addr} has connected.')

    connected = True
    while connected:
        msg_length = connection.recv(FIRST_MESSAGE_SIZE).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            request = connection.recv(msg_length).decode(FORMAT)

            if request == DISCONNECT_MESSAGE:
                break

            path, file_name, contents = parse_request(request)

            os.makedirs(path)
            os.chdir(path)
            with open(file_name, 'w') as f:
                f.write(contents)

            connection.send(f"Your file named {file_name} at location {path} was successfully stored.".encode(FORMAT))

    connection.close()


def run_server():

    network = input('Are you intending to run this server on a local network? (Y / N) ')
    if network.lower() == 'y':
        SERVER = socket.gethostbyname(socket.gethostname())
    else:
        SERVER = input('Please, enter your public ip address: ')

    print('The server is successfully running.')

    ADDR = (SERVER, PORT)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()

    while True:
        connection, addr = server.accept()
        threading.Thread(target=process_connection, args=(connection, addr)).start()
