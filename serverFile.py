import socket
import struct
import random
from random import randint

port = 2470

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

s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_socket.bind(('0.0.0.0', port))

conn1, addr1 = s_socket.accept()
print(f"[+] Player 1 connected: {addr1}, Waiting for Player 2")
conn2, addr2 = s_socket.accept()
print(f"[+] Player 2 connected: {addr2}, Game Starting")

#User Turns
def gameplay():
    player2move = conn2.recv(1024)
    userturn(player2move, )
    player1move = conn1.recv(1024)

#initialize the game
def initializeGame():
    gameboard = [
    [" ", " ", " "],
    [" ", " ", " "],
    [" ", " ", " "]
    ]

    player1 = randint(1,2)
    if player1 == 2:
        player2 = 1
    else :
        player2 = 2

#Check if the user won
def checkWin(gameboard):

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

#add user turn to board
def userturn(playermove, gameboard, player):
    if  (0< playermove < 10) and (playermove%1 == 0):
        if player == 1 :
            char = "x"
        else :
            char = "o"
        position =m[playermove]
        if  gameboard[position[0]][position[1]] == " ":
            gameboard[position[0]][position[1]] = char
        else:
            print(f"Player{player} has made an invalid move {position}")


