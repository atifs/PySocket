# Author: x86asm
# Created: Dec 24, 2014
# Description: A TCP client socket which connects to a remote server

import socket

class PyClient(object):
    def __init__(self, server, port, termination):
        self.server = server
        self.port = int(port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # What terminates packets
        self.termination = termination
        # Data waiting to be turned into a packet
        self.data = ''

    def connect(self):
        """Connect to the objects specified server"""
        try:
            self.socket.connect( (self.server, self.port) )
        except socket.error:
            return 'error'
        except socket.timeout:
            return 'timeout'
        except Exception:
            return 'unknown_exception'
        self.on_connect()

    def data_recv(self, data):
        self.data += data
        tmp = self.data.split(self.termination)
        if tmp[-1] == '':
            if len(tmp) > 1:
                # Every split is a packet
                self.data = ''
                for i in tmp:
                    self.packet_recv(i)
        else:
            if len(tmp) > 1:
                # Every split except the last is a packet
                self.data = tmp.pop()
                for i in tmp:
                    self.packet_recv(i)

    def cleanup(self):
        """Called when its time to cleanup/exit"""
        self.on_exit()
        self.socket.close()        

    # Methods to overload
    def on_connect(self):
        """Called upon successful connection."""
        pass

    def on_disconnect(self):
        """
        Called upon disconnect by the handler. 
        Additionally, return 1 if we have reconnected.  Return 0 to
        remove the PyClient from the list of sockets
        """
        pass

    def packet_recv(self, packet):
        """Called when a packet is formed."""
        pass

    def on_exit(self):
        """Called when its time to exit, socket closed from caller."""
        pass
