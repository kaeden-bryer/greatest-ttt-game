import socket
import struct
import random
from random import randint

#Initialize all
port = 2470
player1 = 1
player2 = 2
move = 0
conn1 = None
conn2 = None
addr1 = None
addr2 = None
game = True
playagain = False


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

#Get user connections
def connectUsers():
    global conn1, conn2, addr1, addr2, game
    s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_socket.bind(('0.0.0.0', port))
    s_socket.listen()

    conn1, addr1 = s_socket.accept()
    print(f"[+] Player 1 connected: {addr1}, Waiting for Player 2")
    conn2, addr2 = s_socket.accept()
    print(f"[+] Player 2 connected: {addr2}, Game Starting")
    game = True

#Disconnects the users and waits for new players
def disconnectUsers():
    global conn1, conn2
    if conn1 is not None and conn2 is not None:
        conn1.close()
        conn2.close()

#User Turns
def gameplay():
    global conn1, conn2
    if conn1 is not None and conn2 is not None:
        conn2.sendall(struct.pack('!Q', 1))
        player2move = conn2.recv(1024)
        userTurn(player2move, player1)
        print("[+] Player 2 played")
        conn1.sendall(struct.pack('!Q', 1))
        player1move = conn1.recv(1024)
        userTurn(player1move, player2)
        print("[+] Player 1 played")
    else:
        print("[!] Error")

#initialize the game
def resetGame():
    global gameboard, player1, player2, move
    gameboard = [
    [" ", " ", " "],
    [" ", " ", " "],
    [" ", " ", " "]
    ]

    move = 0
    player1 = randint(1,2)
    if player1 == 2:
        player2 = 1
    else :
        player2 = 2

#Check if the user won
def checkWin():

    if (gameboard[0][0] == gameboard[0][1] == gameboard[0][2] != " " or
        gameboard[1][0] == gameboard[1][1] == gameboard[1][2] != " " or
        gameboard[2][0] == gameboard[2][1] == gameboard[2][2] != " " or
        gameboard[0][0] == gameboard[1][0] == gameboard[2][0] != " " or
        gameboard[0][1] == gameboard[1][1] == gameboard[2][1] != " " or
        gameboard[0][2] == gameboard[1][2] == gameboard[2][2] != " " or
        gameboard[0][0] == gameboard[1][1] == gameboard[2][2] != " " or
        gameboard[0][2] == gameboard[1][1] == gameboard[2][0] != " "):
        return False
    else :
        return True

#To keep track of game in console
def printboard():
    print("-------------")
    print(f"| {gameboard[0][0]} | {gameboard[0][1]} | {gameboard[0][2]} |")
    print("-------------")
    print(f"| {gameboard[1][0]} | {gameboard[1][1]} | {gameboard[1][2]} |")
    print("-------------")
    print(f"| {gameboard[2][0]} | {gameboard[2][1]} | {gameboard[2][2]} |")
    print("-------------")

#add user turn to board
def userTurn(playermove, player):
    global move
    if  (0< playermove < 10) and (playermove%1 == 0):
        if player == 1 :
            char = "x"
        else :
            char = "o"
        position =m[playermove]
        if  gameboard[position[0]][position[1]] == " ":
            gameboard[position[0]][position[1]] = char
        else:
            print(f"[+] Player{player} has made an invalid move {position}")
        move =+ 1

#ask both users if they wanna play again
def endOfGame():
    global playagain
    print(f"[+] Game Ended")
    print("[+] Asking both users if they want to play again")
    conn1.sendall(struct.pack('!Q', 1))
    player1response_data = conn1.recv(8)
    player1response = struct.unpack('!Q', player1response_data)[0]

    conn2.sendall(struct.pack('!Q', 1))
    player2response_data = conn2.recv(8)
    player2response = struct.unpack('!Q', player2response_data)[0]

    if player1response == 1 and player2response == 1:
        playagain = True
    else:
        playagain = False


#Run server
while game:
    print(f"[+] Game Starting")
    if playagain:
        continue
    else:
        disconnectUsers()
        connectUsers()
    print(f"[+] Player 1 {player1} Connected, Player 2 {player2} Connected")
    print("[+] Beginning...")
    while True:
        printboard()
        print(f"[+] Moves Played: {move}")
        gameplay()
        if move > 5:
            if checkWin():
                break

