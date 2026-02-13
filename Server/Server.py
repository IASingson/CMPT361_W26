# CMPT361 Assignment 1 using source code from lecture

import socket
import sys
import os 
import json
import datetime

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
        serverMenu = "\n\nPlease select the operation:\n1) View uploaded files' information\n2) Upload a file \
                \n3) Terminate the connection\nChoice: ".encode('ascii')
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
                connectionSocket.send(serverMenu)

            # Otherwise, send an error message and terminate the connection
            else:
                errorMessage = 'Incorrect username. Connection Terminated'.encode('ascii')
                connectionSocket.send(errorMessage)
                connectionSocket.close()

            # Server receives client user choice
            menuOption = connectionSocket.recv(2048).decode('ascii')

            # As long as the client does not choose 3, keep the connection
            while menuOption != '3':

                # If client chooses option 1, perform file metadata viewing protocol
                if menuOption == '1':
                    
                    # Get information of files from Database.json

                    # Convert data to formatted string

                    # Send to client 
                    pass

                # If client chooses option 2, perform file upload protocol 
                elif menuOption == '2':
                    
                    # Send client message 'Please provide the file name: '
                    message = 'Please provide the filename: '.encode('ascii')
                    connectionSocket.send(message)
                

                    # Get file information
                    message = connectionSocket.recv(2048).decode('ascii')
                    clientFile = message.split('\n')
                    fileName = clientFile[0]
                    fileSize = clientFile[1]
                    
                    # Send confirmation message 'Ok [filesize] to client'
                    confirmationMessage = f'Ok {fileSize}'.encode('ascii')
                    connectionSocket.send(confirmationMessage)

                    '''
                    # Uploading file information to database
                    fileInfo = {
                        "Name": fileName,
                        "fileSize": fileSize,
                        "dateAndTimeUploaded": datetime.datetime.now()
                    }

                    # Convert to JSON
                    toUpload = json.dumps(fileInfo)
                    print(toUpload)
                    print("hello")
                    '''
                    
                    # Send client server menu again
                    connectionSocket.send(serverMenu)


                    
           
           # If the client chooses option 3, terminate connection
            connectionSocket.send('Connection Terminated'.encode('ascii'))

            
           
            
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
