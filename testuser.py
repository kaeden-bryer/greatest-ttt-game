import socket
import struct
from peterr import register, login, show_leaderboard

ip = "44.201.187.226" #Change to device that's hosting the serverFile.py
port = 2470
move = 0
Menu = True
client_socket = None

gameboard = [
    [" ", " ", " "],
    [" ", " ", " "],
    [" ", " ", " "]
]
m = {
    "1": (0, 0),
    "2": (0, 1),
    "3": (0, 2),
    "4": (1, 0),
    "5": (1, 1),
    "6": (1, 2),
    "7": (2, 0),
    "8": (2, 1),
    "9": (2, 2)
}

def printboard():
    global gameboard

    print("-------------")
    print(f"| {gameboard[0][0]} | {gameboard[0][1]} | {gameboard[0][2]} |")
    print("-------------")
    print(f"| {gameboard[1][0]} | {gameboard[1][1]} | {gameboard[1][2]} |")
    print("-------------")
    print(f"| {gameboard[2][0]} | {gameboard[2][1]} | {gameboard[2][2]} |")
    print("-------------")

def updateBoard(num):
    global move
    global gameboard

    char = "X" if move % 4 == 0 else "O"
    print(f"Char = {char}")

    position = m[str(num)]
    if gameboard[position[0]][position[1]] == " ":
        gameboard[position[0]][position[1]] = char
        move += 1
        print(f"move = {move}")
    else:
        print("Square already taken. Try again.")
        square = input("Enter square number (1-9): ")
        updateBoard(square)

def menu():
    global Menu
    global client_socket
    print("\n1. Register")
    print("2. Login")
    print("3. View Leaderboard")
    print("4. Exit")
    print("5. Play Game")

    choice = input("Choose: ")

    # If the user chooses 1, it will have them register
    if choice == "1":
        register()

    # If user chooses 2, it will have them login
    elif choice == "2":
        user = login()
        if user:
            print(f"Welcome, {user}! You are now logged in.")
    
    # If the user chooses 3, it will display the leaderboard
    elif choice == "3":
        # we gotta figure out how to get the leaderboard from the server. Right now the leaderboard is local
        show_leaderboard()

    # If the user chooses 4, it will exit them out the program
    elif choice == "4":
        print("Goodbye!")
        exit()
    
    elif choice == "5":
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip, port))
        print(f"Client successfully connected to {ip}:{port}")
        print("Starting Game")
        Menu = False

    # If user enters anything other than 1–4
    else:
        print("Invalid choice.")

def turn():

    server_sent_data = client_socket.recv(8)
    print(f"Client received {server_sent_data}")
    server_sent = struct.unpack('!B', server_sent_data)[0]
    print(f"Server sent {server_sent}")
    #depending on server response client side will react accordingly

    if 1 <= server_sent <= 9:
        print(f"Other player played: {server_sent}")
        updateBoard(server_sent)
        printboard()
    if server_sent == 10:
        user_input = int(input("Enter your move: "))
        client_socket.send(struct.pack('!B', user_input))
        updateBoard(user_input)
        printboard()
    if server_sent == 11: #W
        print("You Win!!!")
        return 0
    if server_sent == 12: #F
        print("You Lose!!!")
        return 0
    if server_sent == 13:
        user_input = int(input("Invalid choice... Please go again: "))
        client_socket.send(struct.pack('!B', user_input))
    if server_sent == 14:
        print("It's a Draw!!!")
        return 0
    if server_sent == 15:
        print("Would you like to play again?")
        user_input = int(input("Enter 1 for Yes or 2 for No: "))
    else:
        print("Server send an invalid code")

while True:
    if Menu == True:
        menu()
    else:
        turn()
        move+=1
        print(f"Move {move}")