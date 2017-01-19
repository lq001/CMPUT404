#!/usr/bin/env python

import socket

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# AF_INET means that we want an IPv4 socket
# SOCK_STREAM means that we want a TCP socket

clientSocket.connect(("www.google.com", 80)) 
# note that there is no http://
# port 80 is standard http port

request = "GET / HTTP/1.0\r\n\r\n" 
#location + two blank lines

clientSocket.sendall(request)
#send it to remote server

response = bytearray()
#get response back from google

while True:
    part = clientSocket.recv(1024)
    if (part):
        response.extend(part)
    else:
        break

print response




