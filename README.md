PySocket
========

A python socket class to simplify having multiple TCP sockets

See example.py for an example on how to use this class.

PyClient
========
Member Variables:
self.socket - The socket.  

Methods:
constructor accepts three arguments.  The server to connect to, the connection port, and how packets are terminated.  For 
instance, if "hello world#" is a packet, then the termination string will be "#".

cleanup() will handle closing the socket and call on_exit().  

The following can/should be overloaded:

on_connect can be overloaded and is called upon connection

on_disconnect is called upon disconnect.  The socket is closed by the caller.  If you wish to reconnect, you can do so here.

on_exit is called when its time to exit.  Do not attempt to reconnect here.

PyServer
=======
Methods and variables are similarto that of PyClient with the exception of the following:

The following can be overloaded:
on_client_disconnect which is called when a client disconnects

PyServerClient
==============
Similar to PyClient- except this is the class which will be used for any connections PyServer accepts
