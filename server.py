import socket
import threading

# Setup the server socket
server = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
server.bind(("F8:16:54:A5:2D:18", 4))  # Replace with the server's MAC Address
server.listen(2)  # Allow up to 2 simultaneous connections (assuming two clients)

print("Waiting for connections...")

clients = {}  # Track clients as {client_id: (socket, active_state)}

# Function to forward a message to the other client
def forward_message(sender_id, message):
    for client_id, (client_socket, active) in clients.items():
        if client_id != sender_id:  # Send only to the other client
            try:
                client_socket.send(message)
            except OSError:
                client_socket.close()
                del clients[client_id]
                break

# Function to receive messages from a client
def receive_messages(client_socket, client_id):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            
            message = data.decode('utf-8')
            print(f"Received from {client_id}: {message}")
            
            if message.lower() == 'over':
                # Mark this client as inactive and notify the other client
                clients[client_id] = (client_socket, False)
                forward_message(client_id, f"{client_id} is inactive. You may now send a message.".encode('utf-8'))
            
            else:
                # Forward the message to the other client if this client is active
                if clients[client_id][1]:  # Check if the client is active
                    forward_message(client_id, f"{client_id}: {message}".encode('utf-8'))
        
        except OSError:
            break

    print(f"Client {client_id} disconnected.")
    del clients[client_id]
    client_socket.close()

# Function to handle each client connection
def handle_client(client_socket):
    client_id = threading.current_thread().name
    clients[client_id] = (client_socket, True)  # Start with client active
    print(f"Client {client_id} connected.")

    # Start the thread to handle incoming messages
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket, client_id))
    receive_thread.start()

# Main server loop to accept incoming connections
while True:
    client_socket, addr = server.accept()
    
    # Check if only 2 clients are allowed to connect
    if len(clients) < 2:
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()
    else:
        print("Maximum client connections reached. Connection refused.")
        client_socket.close()

server.close()
