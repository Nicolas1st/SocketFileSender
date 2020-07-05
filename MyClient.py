import client_stuff
import socket


client = client_stuff.Client()
client.connect_to_server()

working = True
while working:
    file_path, where_to_store = client_stuff.request_info()

    client.send_file(file_path, where_to_store)



