# Author: x86asm
# Created: Dec 26, 2014
# Description: A TCP server socket

from pyclient import PyClient

import socket

class PyServer(PyClient):
    def __init__(self, host, port, backlog, pyclientsockcls, termination):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = int(port)
        self.backlog = backlog
        # All clients connected (pyclientsockcls)
        self.clients = []
        # Class to be created for new connections
        self.pyclientsockcls = pyclientsockcls      
        # What terminates packets?
        self.termination = termination

    def listen(self):
        try:
            self.socket.bind( (self.host, self.port) )
            self.socket.listen(self.backlog)
        except Exception:
            return 'error'
        return 'success'
    
    def on_accept(self, sock):
        """Called when a new connection is accepted"""
        client = self.pyclientsockcls(self, sock, self.termination)      
        self.clients.append(sock)
        return client

    def handle_disconnect(self, client):
        try:
            self.clients.remove(client)
        except ValueError:
            pass
        self.on_client_disconnect(client)

    def send_all(self, what):
        for s in self.clients:
            try:
                s.send(what)
            except Exception:
                s.cleanup()

    def cleanup(self):
        for i in self.clients:
            try:
                self.clients.cleanup()
            except:
                pass
        self.socket.close()
        self.on_exit()

    # Methods to overload    
    def on_client_disconnect(self, client):
        """Called when a client disconnects; client is the class instance of our client."""
        pass

    def on_exit(self):
        """Called when its time to exit, socket closed from caller."""
        pass
    
    

