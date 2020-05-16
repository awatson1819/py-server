import socket
import sys
import select
import os
import upload

'''
def send(file_name):
    connection.sendall('send\n'.encode('UTF-8'))  # alert client
    print('sent')
    i = file_name.rfind('/')  # find index of last / in file destination
    connection.sendall(file_name[i+1:].encode('UTF-8'))  # send filename without the destination
    connection.recv(1)  # wait for ack

    totalbytes = os.path.getsize(file_name)
    connection.sendall(str(totalbytes).encode('UTF-8'))
    response = connection.recv(1).decode('UTF-8')  # wait for ack

    if response == 'K':
        file = open(file_name, 'rb')  # opens file and reads it in byte form
        buffer = file.read(2048)  # read 2048 bytes from file to buffer
        while buffer:
            connection.sendall(buffer)
            buffer = file.read(2048)  # read next 2048 bytes
            print("sending......", buffer)
        file.close()
    response = connection.recv(1).decode('UTF-8')
    if response == 'K':
        print('File uploaded successfully')
'''

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
                        upload.send(msg[7:].replace('\n', ''), connection)
                    elif msg == 'close\n':
                        connection.close()
                        exit()

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


