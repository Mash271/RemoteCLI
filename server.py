import socket
import threading

# 1. Connection Config
host = '127.0.0.1'
port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# 2. List to keep track of connected friends
clients = []

# 3. Function to send a message to EVERYONE connected
def broadcast(message, sender_socket):
    for client in clients:
        # Don't send the message back to the person who sent it!
        if client != sender_socket:
            try:
                client.send(message)
            except:
                # If sending fails, assume they disconnected and remove them
                client.close()
                clients.remove(client)

# 4. Function to handle a single client's connection
def handle_client(client_socket):
    while True:
        try:
            # Wait for a message from this specific client
            message = client_socket.recv(1024)
            if message:
                # Send it to everyone else
                broadcast(message, client_socket)
            else:
                # Empty message means they disconnected
                remove(client_socket)
                break
        except:
            continue

def remove(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)

# 5. The Main Loop (The "Doorman")
print("Server is running... waiting for connections.")
while True:
    # Accept a new connection
    client_socket, address = server.accept()
    print(f"New connection from {address}")
    
    # Add them to our list
    clients.append(client_socket)
    
    # Start a new thread just for this client
    thread = threading.Thread(target=handle_client, args=(client_socket,))
    thread.start()