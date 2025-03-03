from cryptography.fernet import Fernet

# Generate a key (Run this ONCE and keep it safe)
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

# Load the saved encryption key
def load_key():
    return open("secret.key", "rb").read()

# Encrypt a message
def encrypt_message(message):
    key = load_key()
    cipher = Fernet(key)
    return cipher.encrypt(message.encode()).decode()

# Decrypt a message
def decrypt_message(encrypted_message):
    key = load_key()
    cipher = Fernet(key)
    return cipher.decrypt(encrypted_message.encode()).decode()

# Uncomment the line below and RUN this file ONCE to generate a key:
# generate_key()
