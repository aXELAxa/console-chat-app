import socket
import threading
import time
import json
import os

HOST = '127.0.0.1'
PORT = 5555

clients = {}  # {client_socket: {"username": username, "room": room}}
rooms = {}    # {room_name: [client_sockets]}
private_chats = {}  # {username: client_socket}
message_logs = "message_logs/"

if not os.path.exists(message_logs):
    os.makedirs(message_logs)

def log_message(room, message):
    """Logs messages in a text file"""
    with open(f"{message_logs}{room}.txt", "a") as file:
        file.write(message + "\n")

def broadcast(message, room, sender_socket=None):
    """Send a message to all clients in a room"""
    log_message(room, message)
    for client in rooms.get(room, []):
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                remove_client(client)

def private_message(sender, receiver, message):
    """Send a private message"""
    if receiver in private_chats:
        receiver_socket = private_chats[receiver]
        try:
            receiver_socket.send(f"[PRIVATE] {sender}: {message}".encode('utf-8'))
        except:
            del private_chats[receiver]

def delete_message(msg_id, room):
    """Deletes a message after a certain time"""
    time.sleep(10)
    broadcast(f"Message {msg_id} has been deleted.", room)

def remove_client(client):
    """Remove a client from the chat"""
    if client in clients:
        room = clients[client]["room"]
        rooms[room].remove(client)
        username = clients[client]["username"]
        del clients[client]
        del private_chats[username]
        client.close()
        broadcast(f"{username} has left the chat.", room)

def handle_client(client):
    """Handles communication with a client"""
    try:
        client.send("Enter chat room name: ".encode('utf-8'))
        room = client.recv(1024).decode('utf-8').strip()
        
        client.send("Enter username: ".encode('utf-8'))
        username = client.recv(1024).decode('utf-8').strip()

        if room not in rooms:
            rooms[room] = []
        rooms[room].append(client)
        clients[client] = {"username": username, "room": room}
        private_chats[username] = client

        broadcast(f"{username} has joined the chat!", room, client)
        print(f"{username} joined {room}")

        while True:
            message = client.recv(1024).decode('utf-8')
            if message.lower() == "/exit":
                break
            elif message.startswith("/selfdestruct"):
                _, duration, msg_text = message.split(" ", 2)
                duration = int(duration)
                msg_id = len(rooms[room])
                broadcast(f"{username} (self-destruct in {duration}s): {msg_text}", room, client)
                threading.Thread(target=delete_message, args=(msg_id, room)).start()
            elif message.startswith("/pm"):
                _, recipient, msg_text = message.split(" ", 2)
                private_message(username, recipient, msg_text)
            else:
                broadcast(f"{username}: {message}", room, client)
    except:
        pass
    finally:
        remove_client(client)

def start_server():
    """Start the chat server"""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server listening on {HOST}:{PORT}")

    while True:
        client, _ = server.accept()
        threading.Thread(target=handle_client, args=(client,)).start()

start_server()
