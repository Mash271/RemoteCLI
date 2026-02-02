import socket
import threading

# 1. Setup the connection
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 9999))

# 2. Define the "Background Ear" function
def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode()
            if message:
                print(f"\n[Friend]: {message}")
                print("Type your message: ", end="") # Keep the prompt visible
            else:
                break
        except:
            print("Disconnected from server.")
            break

# 3. Start the "Background Ear" thread
# This tells the computer: "Run receive_messages() while I move to the next line"
thread = threading.Thread(target=receive_messages)
thread.daemon = True  # This makes the thread close when you close the app
thread.start()

# 4. The Main Thread (The "Mouth")
print("Connection established. Start chatting!")
while True:
    msg = input("Type your message: ")
    client.send(msg.encode())