import sqlite3
import hashlib

# please let me know what must be fixed/improved

# connect to sqlite database (creates users.db if it doesn't exist)
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# create users table to store username, password, and game stats
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT,
    wins INTEGER DEFAULT 0,
    losses INTEGER DEFAULT 0,
    draws INTEGER DEFAULT 0
)
""")
conn.commit()

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
    username = input("Enter new username: ").strip()

# check if user already exists
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
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
    
    hashed = hash_password(password1)
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
    conn.commit()
    print("Registration successful!")

# Log in for an existing user

def login():
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    hashed = hash_password(password)

    cursor.execute(f"SELECT * FROM users WHERE username = '{username}' AND password = '{hashed}'")
    results = cursor.fetchall()
    if results:
        print("Login successful!")
        for row in results:
            print(row)
        return username  # return username so we know who logged in
    else:
        print("Incorrect username or password.")
        return None

# update stats in the database (for leaderboard)

def update_stats(username, result):
    if result == "win":
        cursor.execute("UPDATE users SET wins = wins + 1 WHERE username = ?", (username,))
    elif result == "loss":
        cursor.execute("UPDATE users SET losses = losses + 1 WHERE username = ?", (username,))
    elif result == "draw":
        cursor.execute("UPDATE users SET draws = draws + 1 WHERE username = ?", (username,))
    conn.commit()

# display the leaderboard

def show_leaderboard():
    print("\n🏆 Leaderboard (sorted by wins):")
    cursor.execute("SELECT username, wins, losses, draws FROM users ORDER BY wins DESC LIMIT 10")
    for rank, row in enumerate(cursor.fetchall(), start=1):
        user, w, l, d = row
        print(f"{rank}. {user} | Wins: {w} | Losses: {l} | Draws: {d}")
