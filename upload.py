import os
from socket import MSG_WAITALL
from encryption import decrypter, encrypter

DEFAULT_BUFF = 128  # goto buffer size
MAX_READ = 112


def send(file_name, connection):  # send files to client
    connection.sendall(encrypter('send\n'.encode()))  # alert client

    print('sent')
    i = file_name.rfind('/')  # find index of last / in file destination
    encryption = encrypter(file_name[i + 1:].encode())

    # send filename len and name

    length = (str(len(encryption)))
    length+'\0'  # add trailing end char
    connection.sendall(length.zfill(4).encode())
    connection.sendall(encryption)

    f = open(file_name, 'rb')

    buff = f.read(MAX_READ)
    encrypted = encrypter(buff)  # encrypt read data

    # send size of buffer to be sent as well as padding to ensure length of 4
    length = (str(len(encrypted)))
    length + '\0'  # add trailing end char
    connection.sendall(length.zfill(4).encode())
    connection.sendall(encrypted)

    # send actual data
    connection.sendall(encrypted)

    while len(buff) == MAX_READ:  # if read size less than max read than EOF
        buff = f.read(MAX_READ)
        encrypted = encrypter(buff)  # encrypt read data

        # send size of buffer to be sent as well as padding to ensure length of 4
        length = (str(len(encrypted)))
        length + '\0'  # add trailing end char
        connection.sendall(length.zfill(4).encode())
        connection.sendall(encrypted)

        # send actual data
        connection.sendall(encrypted)

    # close file
    f.close()


def download(file_path, connection):  # upload files from client to server
    #  figures out file name in windows path
    connection.sendall(encrypter("download\n".encode()))  # notify client to wanted service
    # alert client to wanted file
    connection.sendall(encrypter(file_path.encode()))

    file_name = (file_path[file_path.rfind('\\') + 1:])
    file = open(file_name, 'wb')
    while True:
        size = connection.recv(4, MSG_WAITALL).strip(b'\00').decode()  # client sends size
        size = int(size)  # convert sent str to proper int
        #  wait for specified amount of data
        data = decrypter(connection.recv(size, MSG_WAITALL))
        file.write(data)  # write recv data to file

        # once data of max length is sent it means file end has been reached
        if len(data) < MAX_READ:
            break
    file.close()
