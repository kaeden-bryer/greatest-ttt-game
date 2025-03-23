## make a ttt game
import socket
import struct

print("Welcome to Tic Tac Toe!")
player1 = input("Enter Player 1 name: ")
print(f"Player 1: {player1}")

player2 = input("Enter Player 2 name: ")
print(f"Player 1: {player2}")


gameState = True
moveNum = 0

gameboard = [
    [" ", " ", " "],
    [" ", " ", " "],
    [" ", " ", " "]
]

port = 2470
ip = "192.168.0.201"
#client connect
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((ip, port))
print(f"Client successfully connected to {ip}:{port}")

def printboard():
        print("-------------")
        print(f"| {gameboard[0][0]} | {gameboard[0][1]} | {gameboard[0][2]} |")
        print("-------------")
        print(f"| {gameboard[1][0]} | {gameboard[1][1]} | {gameboard[1][2]} |")
        print("-------------")
        print(f"| {gameboard[2][0]} | {gameboard[2][1]} | {gameboard[2][2]} |")
        print("-------------")

def checkWin():
    global gameState
    global moveNum
    if (gameboard[0][0] == gameboard[0][1] == gameboard[0][2] != " " or
        gameboard[1][0] == gameboard[1][1] == gameboard[1][2] != " " or 
        gameboard[2][0] == gameboard[2][1] == gameboard[2][2] != " " or
        gameboard[0][0] == gameboard[1][0] == gameboard[2][0] != " " or
        gameboard[0][1] == gameboard[1][1] == gameboard[2][1] != " " or
        gameboard[0][2] == gameboard[1][2] == gameboard[2][2] != " " or
        gameboard[0][0] == gameboard[1][1] == gameboard[2][2] != " " or
        gameboard[0][2] == gameboard[1][1] == gameboard[2][0] != " "):
            printboard()
            if moveNum % 2 == 0:
                print(f"{player2} wins!")
            else:
                print(f"{player1} wins!")
            gameState = False
    # check if board is full but nobody has won
    elif moveNum == 9:
        checkFull()


def checkFull():
    global gameState
    global moveNum
    if moveNum == 9:
        printboard()
        print("Cat's game! It's a tie!")
        redo = input("Play again? (y/n): ")
        while redo.lower() not in ["y", "n"]:
            redo = input("Invalid input. Play again? (y/n): ")
        if redo.lower() == "y":
            for i in range(3):
                for j in range(3):
                    gameboard[i][j] = " "
            moveNum = 0
            print("Starting a new game!")
            gameState = True
        elif redo.lower() == "n":
            gameState = False

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

def updateBoard(num):
    global moveNum
    char = "X" if moveNum % 2 == 0 else "O"

    position = m[num]
    if gameboard[position[0]][position[1]] == " ":
        gameboard[position[0]][position[1]] = char
        moveNum += 1
    else:
        print("Square already taken. Try again.")
        square = input("Enter square number (1-9): ")
        updateBoard(square)

while (gameState):

    #display board
    print("Current board:")
    printboard()

    #Implement making a code to play with ea later..
    server_sent_data = client_socket.recv(8)
    server_sent = struct.unpack('!Q', server_sent_data)
    print("\nSelect which square you would like to place your character (1-9)!")

    square = input("Enter square number (1-9): ")
    #check if input is valid
    while not square.isdigit() or int(square) < 1 or int(square) > 9:
        print("Invalid input. Please enter a number between 1 and 9.")
        square = input("Enter square number (1-9): ")
    client_socket.sendall(struct.pack('!Q', square))
    updateBoard(square)

    #check if player has won
    checkWin()

    

