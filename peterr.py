import hashlib
import os
import json

# please let me know what must be fixed/improved

FILENAME = "users.txt"

# load users from the database

def load_users():
    if not os.path.exists(FILENAME):
        return {}
    with open(FILENAME, "r") as f:
        return json.load(f)
    
# save users to the file

def save_users(users):
    with open(FILENAME, "w") as f:
        json.dump(users, f)

# ensure their password meets our security requirements

def valid_password(password):
    return (
        len(password) >= 8 and
        any(char.isdigit() for char in password) and
        any(char in "!@#$%^&*()-_=+" for char in password)
    )

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# register a new user

def register():
    users = load_users()

    username = input("Enter new username: ").strip()
    if username in users:
        print("Username is taken, please enter a different one.")
        return
    while True:
        password1 = input("Enter a password: ")
        password2 = input("Confirm password: ")
        
        if password1 != password2:
            print("Passwords do not match, try again.")
            continue
        if not valid_password(password1):
            print("Password must be 8+ characters, with a number and a symbol.")
            continue
        break
    
    users[username] = hash_password(password1)
    save_users(users)
    print("Registration successful!")

# Log in for an existing user

def login():
    users = load_users()
    username = input("Enter username: ")
    password = input("Enter password: ")

    if username not in users:
        print("Username not found.")
        return False
    
    if users[username] == hash_password(password):
        print("Login successful!")
        return True
    
    else: 
        print("Incorrect password.")
        return False