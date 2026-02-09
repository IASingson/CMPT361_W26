# CMPT361 Assignment 1 using the source code from lecture
import socket
import sys

def client():
    # Server Information
    serverName = '127.0.0.1' #'localhost'
    serverPort = 13000
    
    #Create client socket that useing IPv4 and TCP protocols 
    try:
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print('Error in client socket creation:',e)
        sys.exit(1)    
    
    try:
        #Client connect with the server
        clientSocket.connect((serverName,serverPort))
        print("Connected to the server.")

        # Client receives message from server: 'Welcome to our system.\nEnter your username: '
        message = clientSocket.recv(2048).decode('ascii')
        clientUsername = input(message)

        # Client sends username to the server
        clientSocket.send(clientUsername.encode('ascii'))
        
        # Client waits for server response
        serverResponse = clientSocket.recv(2048).decode('ascii')
        errorMessage = 'Incorrect username. Connection Terminated.'

        # If the wrong username is entered print error message and terminate connection to the server
        if serverResponse == errorMessage:
            print(serverResponse)
            clientSocket.close()
        else:
            # If the correct username is entered, print the server menu and send client user choice to server
            clientChoice = input(serverResponse)
            clientSocket.send(clientChoice.encode('ascii'))

        

        # Client terminate connection with the server
        clientSocket.close()
        
    except socket.error as e:
        print('An error occured:',e)
        clientSocket.close()
        sys.exit(1)

#----------
client()
