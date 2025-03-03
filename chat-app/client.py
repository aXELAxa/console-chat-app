import socket
import threading
from auth import register, login

HOST = '127.0.0.1'
PORT = 5555

def receive_messages(client):
    """ Receive messages from the server. """
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if not message:
                break
            print(message)
        except:
            break

def authenticate_user():
    """ Handles user login and signup """
    while True:
        print("\n1. Login")
        print("2. Sign Up")
        choice = input("Choose an option: ")

        username = input("Enter your username: ")
        password = input("Enter your password: ")

        if choice == "1":
            success, message = login(username, password)
        elif choice == "2":
            success, message = register(username, password)
        else:
            print("Invalid option. Try again.")
            continue

        print(message)
        if success:
            return username

def start_client():
    """ Handles client connection. """
    username = authenticate_user()
    
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))
        print("Connected to the server!")

        client.send(username.encode('utf-8'))  # Send username first
        threading.Thread(target=receive_messages, args=(client,), daemon=True).start()

        while True:
            message = input()

            if message.lower() == "/exit":
                client.send(message.encode('utf-8'))
                break
            elif message.startswith("/selfdestruct"):
                client.send(message.encode('utf-8'))
            elif message.startswith("/pm"):
                client.send(message.encode('utf-8'))
            else:
                client.send(message.encode('utf-8'))

    except ConnectionRefusedError:
        print("❌ ERROR: Could not connect to the server.")
    finally:
        client.close()
        print("Disconnected from the server.")

if __name__ == "__main__":
    start_client()
