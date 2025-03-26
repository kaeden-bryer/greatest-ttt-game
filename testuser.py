import socket
import struct

ip = "44.201.187.226" #Change to device that's hosting the serverFile.py
port = 2470
move = 0

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
    if server_sent == 13:
        user_input = int(input("Invalid choice... Please go again: "))
    if server_sent == 14:
        print("It's a Draw!!!")
        return 0
    if server_sent == 15:
        print("Would you like to play again?")
        user_input = int(input("Enter 1 for Yes or 2 for No: "))
    else:
        user_input = int(input("Enter your move: "))
    client_socket.send(struct.pack('!B', user_input))



while True:
    turn()
    move+=1
    print(f"Move {move}")

