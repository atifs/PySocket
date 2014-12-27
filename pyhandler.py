# Author: x86asm
# Created: Dec 24, 2014
# Description: Handles multiple PyServer and PyClient sockets
# Note: Respective classes will handle closing their own sockets and cleaning up

import socket
import select

from pyclient import PyClient
from pyserver import PyServer
from pyserverclient import PyServerClient


class PyHandler:
    def __init__(self):
        # A list of PyClient/PyServer
        self.input = []
        # main() will execute while True
        self.running = True
        # The size of data to read
        self.size = 1024

    def add(self, pyclass):
        if isinstance(pyclass, PyClient):
            self.input.append(pyclass)
        else:
            print('add(self, pyclass) error in PyHandler, pyclass is not of class PyClient or PyServer')

    def remove(self, pyclass):
        try:
            self.input.remove(pyclass)
        except ValueError:
            print('remove(self, pyclass) error in PyHandler, pyclass is not in list of client/servers.')
            return        

    def find_pycls_by_sock(self, sock):
        """Find a PyClient or PyServer by socket"""
        for i in self.input:
            if i.socket == sock:
                return i
        return None

    def get_pysocket_type(self, cls):
        """Tells us what type of PySocket cls is"""
        if isinstance(cls, PyClient):
            if isinstance(cls, PyServer):
                return 'PyServer'
            elif isinstance(cls, PyServerClient):
                return 'PyServerClient'
            else:
                return 'PyClient'
        else:
            return None

    def main(self):
        """Call to start PyHandler, will block until exit."""
        socketlist = list(map(lambda py: py.socket, self.input))
        while self.running and len(socketlist) > 0:
            inputready, outputready, exceptready = select.select(socketlist, [], [])

            for s in inputready:
                pycls = self.find_pycls_by_sock(s)

                if not pycls:
                    self.remove(pycls)
                    s.close()
                    continue

                pysocktype = self.get_pysocket_type(pycls)
                
                # Handle PyClient and PyServerClient            
                if pysocktype == 'PyClient' or pysocktype == 'PyServerClient':                 
                    try:
                        data = s.recv(self.size)
                    except:
                        # Connection closed by peer exception for Windows
                        self.remove(pycls)
                        socketlist.remove(s)
                        pycls.cleanup()
                        
                    if data:
                        pycls.data_recv(data)
                    else:                        
                        if pycls.on_disconnect() == 0:
                            # Remove from list                        
                            self.remove(pycls)
                            socketlist.remove(s)
                            pycls.cleanup()
                    
                elif pysocktype == 'PyServer':
                    # Accept a new connection
                    sock, addr = s.accept()
                    socketlist.append(sock)
                    newpycls = pycls.on_accept(sock)
                    self.input.append(newpycls)
                    

        for i in self.input:
            i.cleanup()
                
