#!/usr/bin/env python

import socket, os, sys, errno, select

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

serverSocket.bind(("0.0.0.0", 8000)) 
#We are not root and only root users can use ports less than 1000
#We are instructing to listen on port 8000
#The 0.0.0.0 part is instructing to listen on all IP addresses for this machine
serverSocket.listen(5)

while True:
	(incomingSocket, address) = serverSocket.accept()
	
	print "Got a connection from %s" % (repr(address))
	try:
		reaped = os.waitpid(0, os.WNOHANG)
	
	except OSError, e:
		if e.errno == errno.ECHILD:
			pass
		else:
			raise
	else:
		print "Reaped %s" % (repr(reaped))
	
	if (os.fork() != 0):
		continue
	 

	clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# AF_INET means that we want an IPv4 socket
	# SOCK_STREAM means that we want a TCP socket

	clientSocket.connect(("www.google.com", 80))

	incomingSocket.setblocking(0)
	clientSocket.setblocking(0)
	while True:
		request = bytearray()
		while True:
			try:
				part = incomingSocket.recv(1014)
			except IOError, e:
				if e.errno == socket.errno.EAGAIN:
					break
				else:
					raise
			if (part):
				request.extend(part)
				clientSocket.sendall(part)
			else:
				sys.exit(0)
			if len(request) > 0:
				print(request)
			
			
			response = bytearray()
		while True:
			try:
				part = clientSocket.recv(1014)
			except IOError, e:
				if e.errno == socket.errno.EAGAIN:
					break
				else:
					raise
			if (part):
				response.extend(part)
				incomingSocket.sendall(part)
			else:
				sys.exit(0) #quit the program
			if len(response) > 0:
				print(response)
			select.select(
    			[incomingSocket, clientSocket], # read
            		[],                             # write
            		[incomingSocket, clientSocket], # exceptions
            		1.0)			        # timeout


