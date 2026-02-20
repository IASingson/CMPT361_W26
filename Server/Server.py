# CMPT361 Assignment 1 using source code from lecture

import socket
import sys
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
        try:
            # Server accepts client connection
            connectionSocket, addr = serverSocket.accept()
            print(addr,'   ',connectionSocket)
            print("Client is connected to the server") # delete before submitting

            # Send client welcome message and ask for username
            msgToClient = 'Welcome to our system. \nEnter your username: '.encode('ascii')
            connectionSocket.send(msgToClient)

            # Receive client username
            msgFromClient = connectionSocket.recv(2048).decode('ascii')

            # If client is NOT user1, terminate the connection
            if msgFromClient != 'user1':
                msgToClient = 'Incorrect username. Connection terminated'.encode('ascii')
                connectionSocket.send(msgToClient)
                connectionSocket.close()
            else:
                serverMenu = "\n\nPlease select the operation:\n1) View uploaded files' information\n2) Upload a file \
                \n3) Terminate the connection\nChoice: ".encode('ascii')
                connectionSocket.send(serverMenu)
            
            while True:

                msgFromClient = connectionSocket.recv(2048).decode('ascii')
                
                # If client chooses 1, send database information
                if msgFromClient == '1':
                    # Read from Database.json
                    # If file already exists
                    try:

                        with open('Server\\Database.json', 'r') as file:
                            data = json.load(file)
                            msgToServer = '\nName\t\t\t\tSize (Bytes)\t\t\t\tUpload Date and Time\n'
                            for key in data:
                                filename = key
                                fileSize = data[key]['size']
                                dateTimeUploaded = data[key]['dateTimeUploaded']
                                newline = '\n'
                                msgToServer += f'{filename:<32}{str(fileSize):<40}{dateTimeUploaded}{newline}'
                            
                        
                        # Get size of text and then send size to client
                        size = str(len(msgToServer))
                        connectionSocket.send(size.encode('ascii')) 

                        # Send the current database to client
                        connectionSocket.send(msgToServer.encode('ascii'))

                        # Send server menu to client
                        connectionSocket.send(serverMenu)

                    except:
                        connectionSocket.send('Name\tSize (Bytes)\tUpload Date and Time'.encode('ascii'))

                        connectionSocket.send(serverMenu)
                
                # If client chooses 2, start file upload subprotocol
                elif msgFromClient == '2':
                    
                    # Get file name
                    msgToClient = 'Please provide the filename: '.encode('ascii')
                    connectionSocket.send(msgToClient)

                    # Upon receiving file information, send confirmation message
                    msgFromClient = connectionSocket.recv(2048).decode('ascii')
                    fileInformation = msgFromClient.split('\n')
                    filename = fileInformation[0]
                    fileSize = int(fileInformation[1])

                    msgToClient = f'Ok {fileSize}'
                    connectionSocket.send(msgToClient.encode('ascii'))

                    # Copy file to server folder
                    fileBytes = 0
                    with open('Server\\'+filename, 'wb') as file:
                        while True: 
                            if fileBytes == fileSize:
                                break
                            data = connectionSocket.recv(2048)
                            file.write(data)
                            fileBytes += len(data)
                    
                    dateTimeUploaded = str(datetime.datetime.now())

                    # Format file metada

                    fileMetaData = {
                        filename: 
                        {'size': fileSize, 
                         'dateTimeUploaded': dateTimeUploaded
                        }
                    }
                  
                    # Store file metada in database
                    try:
                        # If database file already exists

                        # Read file and add new data to existing data
                        with open('Server\\Database.json', 'r') as file:
                            data = json.load(file)
                        data.update(fileMetaData)
                        
                        # Write existing data + new data back to the file 
                        with open('Server\\Database.json', 'w') as file:
                            json.dump(data, file, indent = 2)

                    # If no database file exists, make a new one and add data
                    except: 
                        with open('Server\\Database.json', 'w') as file:
                            json.dump(fileMetaData, file, indent = 2)

                    # Send server menu to client again
                    connectionSocket.send(serverMenu)

                # When client chooses option 3 or inputs anything else
                else:
                    break


            connectionSocket.close()     
            
        except socket.error as e:
            print('An error occured:',e)
            serverSocket.close() 
            sys.exit(1)        
        except:
            print('Goodbye')
            serverSocket.close() 
            sys.exit(0)
                   
#-----------------------------------
server()
