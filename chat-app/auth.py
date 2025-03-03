import json
import os

users_file = "users.json"

if not os.path.exists(users_file):
    with open(users_file, "w") as file:
        json.dump({}, file)

def load_users():
    """ Load user data from JSON """
    with open(users_file, "r") as file:
        return json.load(file)

def save_users(users):
    """ Save user data to JSON """
    with open(users_file, "w") as file:
        json.dump(users, file)

def register(username, password):
    users = load_users()
    if username in users:
        return False, "Username already exists."
    users[username] = password
    save_users(users)
    return True, "Account created successfully!"

def login(username, password):
    users = load_users()
    if username in users and users[username] == password:
        return True, "Login successful!"
    return False, "Invalid credentials."
