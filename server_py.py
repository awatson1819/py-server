import socket
import sys
import select


def send(file_name):
    i = file_name.rfind('/')  # find index of last / in file destination
    connection.send('send'.encode('UTF-8'))  # alert client
    connection.send(file_name[i+1:])  # send filename without the destination

    file = open(file_name, 'rb')  # opens file and reads it in byte form
    buffer = file.read(2048)  # read 2048 bytes from file to buffer
    while buffer:
        connection.send(buffer)
        buffer = file.read(2048)  # read next 2048 bytes
    file.close()
    connection.send('EOF'.encode('UTF-8'))  # notify that end of file has been reached


# socket initialize
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("socket created")


# reserving port 4444 for incoming connections
port = 4444


s.bind(('', port))
s.listen(1)
print('server started waiting for connections')

while True:
    # waiting for connection
    connection, client_addr = s.accept()
    try:
        print("connection from", client_addr[0])
        while 1:
            # non blocking input read
            while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                msg = sys.stdin.readline()
                if msg:
                    if msg.find('upload') == 0:
                        send(msg[5:])
                    elif msg == 'close\n':
                        connection.close()
                        exit()
                    print('\nsending message: ', msg)
                    connection.sendall(msg.encode('UTF-8'))
            else:  # user has not typed anything
                # checks if value is available for recv
                r, _, _ = select.select([connection], [], [], 0)
                if r:
                    data = connection.recv(2048)
                    if not data: break
                    print(data.decode('UTF-8'))

    except KeyboardInterrupt:
        s.close()
        connection.close()
        exit()


