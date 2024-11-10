
import socket
import threading

client = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
client.connect(("F8:16:54:A5:2D:18", 4))  # Replace with the server's MAC Address

print("Connected to the server!")

# Global flag to control whether the client can send messages
can_send = True

# Function to receive messages from the server and control send permission
def receive_messages():
    global can_send
    while True:
        try:
            data = client.recv(1024)
            if not data:
                break
            message = data.decode('utf-8')
            print(f"Received: {message}")

            # Allow this client to send messages when it receives any message
            can_send = True
            print("You can now send messages. Type 'over' to stop sending.")
        except OSError:
            break

# Function to send messages to the server
def send_messages():
    global can_send
    while True:
        if can_send:
            message = input("Enter message: ")
            if message.lower() == 'over':
                # Stop sending and wait for the next message from the other device
                can_send = False
                print("Waiting for the other device to send a message...")
            else:
                # Send the entered message to the server
                client.send(message.encode('utf-8'))

# Start the thread for receiving messages
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# Start the main loop for sending messages
send_messages()

print("Disconnected from the server.")
client.close()
