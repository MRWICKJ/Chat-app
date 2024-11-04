import socket
import threading

# Server details
host = '127.0.0.1'  # Localhost
port = 55555

# Create server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []  # List of clients connected to the server
nicknames = []  # List of nicknames of the clients

# Broadcast function to send a message to all clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Function to handle individual client communication
def handle_client(client):
    while True:
        try:
            # Receive and broadcast messages
            message = client.recv(1024)
            broadcast(message)
        except:
            # Remove and close the client if it disconnects
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!'.encode('utf-8'))
            nicknames.remove(nickname)
            break

# Function to receive new clients
def receive():
    while True:
        # Accept new connections
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        # Request and store nickname
        client.send("Welcome To Chat-Mop".encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        # Notify others and start handling thread
        print(f"Nickname is {nickname}")
        broadcast(f"{nickname} joined the chat!".encode('utf-8'))
        client.send("Connected to the server!".encode('utf-8'))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

print("Server is listening...")
receive()
