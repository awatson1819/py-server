import os
from socket import MSG_WAITALL
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
    connection.sendall(encrypter("download\n".encode())) # notify client to wanted service
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
        

