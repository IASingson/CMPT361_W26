# CMPT361 Assignment 1 using source code from lecture

import socket
import sys

def server():
    # Server port
    serverPort = 13000
    
    # Create server socket that uses IPv4 and TCP protocols 
    try:
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print('Error in server socket creation:',e)
        sys.exit(1)
    
    # Associate 13000 port number to the server socket
    try:
        serverSocket.bind(('', serverPort))
    except socket.error as e:
        print('Error in server socket binding:',e)
        sys.exit(1)        
        
    print('The server is ready to accept connections')
        
    # The server can only have one connection in its queue waiting for acceptance
    serverSocket.listen(1)
        
    while 1:
        try:
            # Server accepts client connection
            connectionSocket, addr = serverSocket.accept()
            print(addr,'   ',connectionSocket)
            print("Client is connected to the server") # delete before submitting

            # Server sends client a message
            message = 'Welcome to our system.\nEnter your username: '.encode('ascii')
            connectionSocket.send(message)

            # Server recieved client username
            clientUsername = connectionSocket.recv(2048).decode('ascii')
            authUser = 'user1'

            # If the username is correct, send the client the menu
            if clientUsername == authUser:
                serverMenu = "\n\nPlease select the operation:\n1) View uploaded files' information\n2) Upload a file \
                \n3) Terminate the connection\nChoice: ".encode('ascii')

                connectionSocket.send(serverMenu)

            # Otherwise, send an error message and terminate the connection
            else:
                errorMessage = 'Incorrect username. Connection Terminated'.encode('ascii')
                connectionSocket.send(errorMessage)
                connectionSocket.close()

            # Server receives client user choice
            menuOption = connectionSocket.recv(2048).decode('ascii')

            
           
            
            #Server terminates client connection
            connectionSocket.close()
            
        except socket.error as e:
            print('An error occured:',e)
            serverSocket.close() 
            sys.exit(1)        
        except:
            print('Goodbye')
            serverSocket.close() 
            sys.exit(0)
            
        
#-------
server()
