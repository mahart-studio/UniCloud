import asyncio
import threading
import json

class ServerGuy(asyncio.Protocol):

    def connection_made(self, transport):
        self.transport = transport
        print(transport)

    def data_received(self, data):
        if data:
            # data = json.loads(data)
            # print(data)
            # filename =  data['filename']
            # file_data = data['file_data']

            with open('server_file.pdf', 'w+b') as file_obj:
                file_obj.write(data)

        print('file_saved')

    
loop = asyncio.get_event_loop()

coro = loop.create_server(ServerGuy, '0.0.0.0', 5920) # Here you can change the address and the port
server = loop.run_until_complete(coro)

print('Serving on {}'.format(server.sockets[0].getsockname()))

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
