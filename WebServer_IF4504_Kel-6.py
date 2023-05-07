from socket import *
import sys 

serverHost = socket(AF_INET, SOCK_STREAM)
serverPort = 3275

serverHost.bind(('', serverPort))
serverHost.listen(1)

while True:
    #Establish the connection
    print('Server is Ready')
    
    connectionSocket, addr = serverHost.accept()
    try:
        name = connectionSocket.recv(1024)
        filename = name.split()[1]
        print(filename)
        if filename == b'/':
            raise Exception
        f = open(filename[1:], "rb")
        outputdata = f.read()
        
        #Send one HTTP header line into socket
        header = '\nHTTP/1.1 200 OK\n\n'
        connectionSocket.send(header.encode())
   
        #Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i:i+1])
        connectionSocket.send(b'\r\n\r\n')
        print('Response done, waiting for server...\n')

        connectionSocket.close()
    
    except IOError:
        #Send response name for file not found
        filename = b'/NotFoundPage.html'
        f = open(filename[1:], "rb")
        outputdata = f.read()
        header = '\nHTTP/1.1 404 Not Found\n\n'
        connectionSocket.send(header.encode())
        
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i:i+1])
        connectionSocket.send(b'\r\n\r\n')

        connectionSocket.close()
        print('Response done, waiting for server...\n')

        #Close client socket
        connectionSocket.close()
    
    except Exception:
        #Send response name for file not found
        filename = b'/WelcomePage.html'
        f = open(filename[1:], "rb")
        outputdata = f.read()
        header = '\nHTTP/1.1 200 OK\n\n'
        connectionSocket.send(header.encode())

        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i:i+1])
        connectionSocket.send(b'\r\n\r\n')

        connectionSocket.close()
        print('Response done, waiting for server...\n')

        #Close client socket
        connectionSocket.close()
    
serverHost.close()
sys.exit()#Terminate the program after sending the corresponding data 