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
    
    server_sent_data = client_socket.recv(8)
    print(f"Client received {server_sent_data}")
    server_sent = struct.unpack('!B', server_sent_data)[0]
    print(f"Server sent {server_sent}")
    #depending on server response client side will react accordingly

    if server_sent == 11: #W
        print("You Win!!!")
        return 0
    if server_sent == 12: #F
        print("You Lose!!!")
        return 0
    if server_sent == 15:
        print("Would you like to play again?")
        user_input = int(input("Enter 1 for Yes or 2 for No: "))
    # I've changed it so that 10 is the signal that it is the users turn. If the user receives nums 1-9, that is the server
    # sending the opponents move (board number) to the user.
    if server_sent == 10:
        print("Current board:")
        printboard(gameboard)
        # checking whether this is valid doesn't need to be handled by the server if each user holds a copy of the gameboard. I'll fix this
        user_input = int(input("Enter your move: "))
        # update gameboard. updateBoard now returns the updated gameboard
        gameboard = updateBoard(gameboard, user_input)
        move += 1
        client_socket.send(struct.pack('!B', user_input))

        # testing
        print("Updated board")
        printboard(gameboard)

    else:
        char = "X" if move % 2 == 0 else "O"
        position = m[server_sent]
        gameboard[position[0]][position[1]] = char

while True:
    turn()
    move+=1
    print(f"Move {move}")

