# CMPT361 Assignment 1 using the source code from lecture
import socket
import sys
import os

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
        # Client connect with the server
        clientSocket.connect((serverName,serverPort))
        print('Connected to the server.') # DELETE BEFORE SUBMITTING

        # Welcome message from server
        msgFromServer = clientSocket.recv(2048).decode('ascii')
        
        # Get client username and send to server
        msgToServer = input(msgFromServer)
        clientSocket.send(msgToServer.encode('ascii'))

        # Receive response from server regarding username
        msgFromServer = clientSocket.recv(2048).decode('ascii')

        # If wrong username, terminate connection
        if msgFromServer == 'Incorrect username. Connection terminated':
            print(msgFromServer)
            clientSocket.close()
        else:
            # Get user input on server menu
            msgToServer = input(msgFromServer)
            clientSocket.send(msgToServer.encode('ascii'))

        # Loop while client does not choose option 3
        while True:

            msgFromServer = clientSocket.recv(2048).decode('ascii')

            #clientSocket.send(msgToServer.encode('ascii'))
            if msgFromServer == 'Please provide the filename: ':
                # Ask client user for filename to upload 
                filename = input(msgFromServer)
                
                # Get file size, send in formatted string to server
                filePath = os.path.abspath(filename)
                fileSize = os.path.getsize(filePath)

                # Send file information to server in formatted string
                msgToServer = f"{filename}\n{fileSize}"
                clientSocket.send(msgToServer.encode('ascii'))

                # Get confirmation message and print to client user
                msgFromServer = clientSocket.recv(2048).decode('ascii')
                print(msgFromServer)

                # Send file data to server

                with open(filename, 'rb') as file:
                    while True:
                        data = file.read(2048)
                        if not data:
                            break
                        clientSocket.send(data)
                    

               

                print('Upload process completed')

                # Client receives server menu again 
                msgFromServer = clientSocket.recv(2048).decode('ascii')
                msgToServer = input(msgFromServer)

            # If server terminates connection
            elif msgFromServer == '':
                print('Connection terminated')
                clientSocket.close()

            # If sent database information
            else:
                print(msgFromServer)







        
    except socket.error as e:
        print('An error occured:',e)
        clientSocket.close()
        sys.exit(1)

#----------
client()
