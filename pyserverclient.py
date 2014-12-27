# Author: x86asm
# Created: Dec 26, 2014
# Description: A TCP server socket client

from pyclient import PyClient

import socket

class PyServerClient(PyClient):
    def __init__(self, owner, sock, termination):
        # The instance of the server class who serves this client socket
        self.owner = owner
        self.socket = sock
        self.data = ''
        self.termination = termination

    def on_disconnect(self):
        # The caller will clean everything up
        return 0

    def cleanup(self):
        self.on_exit()        
        self.owner.handle_disconnect(self)
        self.socket.close()

    # Methods to overload
    def on_connect(self):
        """Called right after the server accepts a connection"""
        pass

    def packet_recv(self, packet):
        """Called when a packet is formed."""
        pass

    def on_exit(self):
        """Called when its time to exit, socket closed from caller."""
        pass

