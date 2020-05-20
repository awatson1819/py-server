import socket
import sys
import select
import upload

def shell():
    connection.sendall('shell\n'.encode('UTF-8'))
    while True:
        while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            shellmsg = sys.stdin.readline()
            connection.sendall(shellmsg.encode('UTF-8'))
        else:  # user has not typed anything
            # checks if value is available for recv
            r, _, _ = select.select([connection], [], [], 0)
            if r:
                data = connection.recv(2048)
                if not data: break  # breaks from while True loop
                print(data.decode('UTF-8'))


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
            msg = sys.stdin.readline()
            if msg:
                if msg.find('upload') == 0:
                    upload.send(msg[7:].replace('\n', ''), connection)
                elif msg == 'close\n':
                    connection.sendall('conend'.encode('UTF-8'))
                    connection.close()
                    exit()
                elif msg.find('download') == 0:
                    upload.download(msg[9:].replace('\n', ''), connection)
                elif msg == 'shell\n':
                    shell()
    except KeyboardInterrupt:
        s.close()
        connection.close()
        exit()
