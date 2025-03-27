import socket
import struct
import pickle
# importing gamefunctions to make everything work
from gamefunctions import printboard, checkWin, updateBoard

ip = "44.201.187.226" #Change to device that's hosting the serverFile.py
port = 2470
move = 0

#each user needs to have a copy of gameboard
gameboard = [
    [" ", " ", " "],
    [" ", " ", " "],
    [" ", " ", " "]
]
# map to convert numbers to coordinates
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

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((ip, port))
print(f"Client successfully connected to {ip}:{port}")

def turn():
    global move
    global gameboard
    user_input = 0
    
    try:
        server_sent_data = client_socket.recv(1)
        if not server_sent_data:
            print("Connection closed by server.")
            return 0

        server_sent = struct.unpack('!B', server_sent_data)[0]
        print(f"Number sent by server: {server_sent}")

        if server_sent == 11:  # W
            print("You Win!!!")
            return 0
        elif server_sent == 12:  # F
            print("You Lose!!!")
            return 0
        elif server_sent == 15:
            print("Would you like to play again?")
            user_input = int(input("Enter 1 for Yes or 2 for No: "))
        elif server_sent == 10:
            print("Current board:")
            printboard(gameboard)
            user_input = int(input("Enter your move: "))
            print("user_input", user_input)
            gameboard = updateBoard(gameboard, str(user_input))
            move += 1
            print("Updated board:")
            printboard(gameboard)
        else:
            char = "X" if move % 2 == 0 else "O"
            position = m[str(server_sent)]
            gameboard[position[0]][position[1]] = char

        client_socket.send(struct.pack('!B', user_input))
        print(f"Sent {user_input} to server")

    except (socket.error, struct.error) as e:
        print(f"Socket error: {e}")
        return 0

while True:
    if turn() == 0:
        break
    move+=1
    print(f"Move {move}")

