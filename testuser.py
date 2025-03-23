import socket
import struct

ip = "192.168.0.201"
port = 2470
move = 0


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((ip, port))
print(f"Client successfully connected to {ip}:{port}")

def turn():
    server_sent_data = client_socket.recv(8)
    print(f"Client received {server_sent_data}")
    server_sent = struct.unpack('!Q', server_sent_data)[0]
    print(f"Server sent {server_sent}")
    user_input = int(input("Enter your move: "))
    client_socket.send(struct.pack('!Q', user_input))


while move < 6:
    turn()
    move+=1

