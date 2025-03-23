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
    global conn2
    if conn2 is not None:
        conn2.sendall(struct.pack('!B', 1))
        player2move = struct.unpack('!B', conn2.recv(8))[0]
        userTurn(player2move, player1)
        print("[+] Player 1 played")
        printboard()
    else:
        print("[!] Player 1 Error")

def gameplay2():
    global conn1
    if conn1 is not None:
        conn1.sendall(struct.pack('!B', 1))
        player1move = struct.unpack('!B', conn1.recv(8))[0]
        userTurn(player1move, player2)
        print("[+] Player 2 played")
        printboard()
    else:
        print("[!] Player 2 Error")

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
        return True
    else :
        return False

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
    if  (0< playermove < 10) and (playermove%1 == 0):
        if player == 1 :
            char = "x"
        else :
            char = "o"
        position =m[str(playermove)]
        if  gameboard[position[0]][position[1]] == " ":
            gameboard[position[0]][position[1]] = char
        else:
            print(f"[+] Player{player} has made an invalid move {position}")

def sendWin(ttt_winner):
    global conn1, conn2
    if conn1 is not None and conn2 is not None:
        if ttt_winner == 1:
            conn2.sendall(struct.pack('!B', 12))
            conn1.sendall(struct.pack('!B', 11))
        if ttt_winner == 2:
            conn2.sendall(struct.pack('!B', 11))
            conn1.sendall(struct.pack('!B', 12))


#ask both users if they wanna play again
def endOfGame():
    global playagain, conn1, conn2
    print(f"[+] Game Ended")
    print("[+] Asking both users if they want to play again")
    conn1.sendall(struct.pack('!B', 15))
    player1choice = struct.unpack('!B', conn1.recv(8))[0]

    conn2.sendall(struct.pack('!B', 15))
    player2choice = struct.unpack('!B', conn2.recv(8))[0]

    if player2choice == 1 and player1choice == 1:
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
        print(f"[+] Moves Played: {move}")
        gameplay()
        if checkWin():
            print("[+] Player 2 Wins")
            sendWin(2)
            break
        gameplay2()
        if checkWin():
            print("[+] Player 1 Wins")
            sendWin(1)
            break
    endOfGame()

