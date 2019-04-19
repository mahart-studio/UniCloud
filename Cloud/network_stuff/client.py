import asyncore
import socket
import json
import threading

server_address = ("127.0.0.1", 5920)

class Client(asyncore.dispatcher):
    def __init__(self):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect(server_address)

    def handle_read(self):
        data = self.recv(8192)
        print(data)

client = Client()
client_thread = threading.Thread(target=asyncore.loop)
client_thread.setDaemon = False
client_thread.start()

filename = 'pdf_file.pdf'

with open(filename, 'r+b') as fp:
    # data = {'filename': filename, 'file_data': fp.read()}
    client.send(fp.read())

