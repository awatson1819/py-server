import os
from _socket import MSG_WAITALL
from encryption import decrypter, encrypter

DEFAULT_BUFF = 128  # goto buffer size
MAX_READ = 112


def send(file_name, connection):  # send files to client
    connection.sendall(encrypter('send\n'.encode()))  # alert client
    print('sent')
    i = file_name.rfind('/')  # find index of last / in file destination
    connection.sendall(encrypter(file_name[i + 1:].encode()))  # send filename without the destination
    ack = connection.recv(1)  # recive acknowledge

    totalbytes = os.path.getsize(file_name)
    connection.sendall(encrypter(str(totalbytes).encode())) # sends file size to expect to client
    response = connection.recv(1).decode()  # wait for ack

    if response == 'K':
        file = open(file_name, 'rb')  # opens file and reads it in byte form
        # read must be smaller than sent buffer to allow for adding of padding details
        buffer = file.read(MAX_READ)
        while buffer:
            connection.sendall(encrypter(buffer))  # encrypt buff and send
            # # read must be smaller than sent buffer to allow for adding of padding details
            buffer = file.read(MAX_READ)  # read next BUF LEN bytes
        file.close()
    response = connection.recv(1).decode()
    if response == 'K':
        print('File uploaded successfully')


def download(file_path, connection):  # upload files from client to server
    #  figures out file name in windows path
    file_name = (file_path[file_path.rfind('\\') + 1:])

    # notify client to command
    connection.sendall(encrypter('download\n'.encode()))

    connection.sendall(encrypter(file_path.encode('UTF-8')))  # alert client to wanted file
    response = connection.recv(1).decode('UTF-8')  # wait for client ack

    # correct ack if file found
    if response == 'K':
        # strip extra empty bytes and decode
        str_size = decrypter(connection.recv(16).strip(b'\00')).decode()  # file size sent by client
        # remove any extra /0 from C send value and turns to int
        size = int(str_size)

        # for troubleshooting
        print('file size: ', size)

        connection.sendall('K'.encode('UTF-8'))  # no need to encrypt

        file = open(file_name, 'wb')  # open file in write binary mode

        amt_recv = 0
        while amt_recv < size:
            # recv message and strip any extra \00's of unused space
            buffer = connection.recv(DEFAULT_BUFF)

            decrypted = decrypter(buffer)

            # increment amount recv by size of plaintext
            amt_recv += len(decrypted)
            file.write(decrypted)
        file.close()
        print("fill successfully downloaded")
