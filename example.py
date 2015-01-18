from pyhandler import PyHandler
from pyclient import PyClient
from pyserver import PyServer
from pyserverclient import PyServerClient

class MyServer(PyServer):
    def __init__(self, *args):
        super(self.__class__, self).__init__(*args)

    def on_client_disconnect(self, client):
        print 'Client disconnected'

    def on_exit(self):
        print 'Time to exit'

class MyServerClient(PyServerClient):
    def __init__(self, *args):
        super(self.__class__, self).__init__(*args)

    def on_connect(self):
        print 'Received connection'

    def packet_recv(self, packet):
        print 'Recv packet, %s %s' % packet

    def on_exit(self):
        print 'Exited'

class Client(PyClient):
    def __init__(self, *args):
        super(Client, self).__init__(*args)
        
    def on_connect(self):
        print 'connected'
        self.socket.send('GET / HTTP/1.1\r\nHost:yahoo.com\r\n\r\n')       
        
    def on_disconnect(self):
        print 'd/c'
        return 0

    def packet_recv(self, packet):
        print 'Packet: %s' % packet

    def on_exit(self):
        print 'Goodbye...'

# Remember to call connect or listen before or after adding the pycls to the handler

client = Client('yahoo.com', 80, '\n')
handler = PyHandler()

handler.add(client)
client.connect()

server = MyServer('', 9001, 5, MyServerClient, '#')

# This will let us know if everything was successful.  No error handling in this demonstration.
print server.listen()

handler.add(server)

handler.main()
