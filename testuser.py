import socket
import struct

ip = "44.201.187.226" #Change to device that's hosting the serverFile.py
port = 2470
move = 0

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((ip, port))
print(f"Client successfully connected to {ip}:{port}")

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
    turn()
    move+=1
    print(f"Move {move}")

# i hate my life