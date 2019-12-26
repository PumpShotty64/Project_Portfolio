# import modules that are needed
import socket

'''
Reads user input of host and port.
Makes sure inputs are valid.
'''
def read_server():

    while True:
        host = input("Host: ").strip()
        if host != '':
            break
        print("Host left blank. Try again!")

    while True:
        try:
            port = int(input("Port: ").strip())
            if 0 <= port <= 65535:
                return host, port
            else:
                print("Port must be between 0 and 65535")
        except:
            print("Port must be between 0 and 65535")


'''
Connects to the server and creates temp files in order to communicate with client.
'''
def connection(host: str , port: int):

    gameSocket = socket.socket()
    gameSocket.connect((host, port))

    gameInput = gameSocket.makefile("r")
    gameOutput = gameSocket.makefile("w")

    return gameSocket, gameInput, gameOutput


'''
Sends the message to the server to write.
'''
def send_message(connection: "connection", message: str):

    gameSocket, gameInput, gameOutput = connection

    gameOutput.write(message + "\r\n")
    gameOutput.flush()


'''
Sends action to the server to write.
'''
def send_action(connection: "connection", action, col):

    gameSocket, gameInput, gameOutput = connection

    gameOutput.write(f"{action} {col}\r\n")
    gameOutput.flush()


'''
Recieves action and returns message that will be sent to the client.
'''
def recieve_action(connection: "connection"):

    gameSocket, gameInput, gameOutput = connection

    return gameInput.readline()[:-1]


'''
Closes the server connection
'''
def close(connection: "connection"):

    gameSocket, gameInput, gameOutput = connection

    gameInput.close()
    gameOutput.close()
    gameSocket.close()