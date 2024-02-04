import socket
import select
import errno
import sys

HEADER_LENGTH = 10

# 127.0.0.1
# online "DO staff" ip: 10.151.40.77
IP = "127.0.0.1"
PORT = 1909
my_username = input("Username: ")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((IP, PORT))

client_socket.setblocking(False)

# Send the username to the server
username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)

while True:
    try:
        # Wait for user to input a message
        message = input(f'{my_username} > ')

        if message:
            # Encode message to bytes, prepare header and convert to bytes, then send
            message = message.encode('utf-8')
            message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
            client_socket.send(message_header + message)

        # Handle incoming messages from the server
        while True:
            username_header = client_socket.recv(HEADER_LENGTH)

            if not len(username_header):
                print('Connection closed by the server')
                sys.exit()

            username_length = int(username_header.decode('utf-8').strip())
            username = client_socket.recv(username_length).decode('utf-8')

            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')

            print(f'{username} > {message}')

    except IOError as e:
        # Handle non-blocking socket
        if e.errno == errno.EAGAIN or e.errno == errno.EWOULDBLOCK:
            continue
        else:
            print('Reading error: {}'.format(str(e)))
            sys.exit()

    except Exception as e:
        # Any other exception - something happened, exit
        print('Error: {}'.format(str(e)))
        sys.exit()
