import hashlib
import os
import json

# please let me know what must be fixed/improved

FILENAME = "users.txt"

# load users from the database

def load_users():
    if not os.path.exists(FILENAME):
        reutrn {}
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
def hash_passsword(password):
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