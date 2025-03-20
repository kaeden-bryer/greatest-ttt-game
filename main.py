## make a ttt game

print("Welcome to Tic Tac Toe!")
username = input("Enter your name: ")
print(f"Player 1: {username}")

gameState = True
moveNum = 0

gameboard = [
    [" ", " ", " "],
    [" ", " ", " "],
    [" ", " ", " "]
]

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
    if (gameboard[0][0] == gameboard[0][1] == gameboard[0][2] != " " or
        gameboard[1][0] == gameboard[1][1] == gameboard[1][2] != " " or 
        gameboard[2][0] == gameboard[2][1] == gameboard[2][2] != " " or
        gameboard[0][0] == gameboard[1][0] == gameboard[2][0] != " " or
        gameboard[0][1] == gameboard[1][1] == gameboard[2][1] != " " or
        gameboard[0][2] == gameboard[1][2] == gameboard[2][2] != " " or
        gameboard[0][0] == gameboard[1][1] == gameboard[2][2] != " " or
        gameboard[0][2] == gameboard[1][1] == gameboard[2][0] != " "):
            printboard()
            print("You win!")
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

    print("\nSelect which square you would like to place your character (1-9)!")

    square = input("Enter square number (1-9): ")
    #check if input is valid
    while not square.isdigit() or int(square) < 1 or int(square) > 9:
        print("Invalid input. Please enter a number between 1 and 9.")
        square = input("Enter square number (1-9): ")

    updateBoard(square)

    #check if player has won
    checkWin()

    

